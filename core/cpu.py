"""
MIPS 16-bit Pipelined CPU Core
Main execution engine with 5-stage pipeline
"""

class PipelinedCPU:
    """
    16-bit MIPS Pipelined CPU Implementation
    
    Pipeline Stages:
    1. IF (Instruction Fetch)
    2. ID (Instruction Decode)
    3. EX (Execute)
    4. MEM (Memory Access)
    5. WB (Write Back)
    """
    
    def __init__(self):
        # Hardware Components
        self.registers = [0] * 8  # R0-R7 (R0 always 0)
        self.memory = [0] * 64    # 64 words of data memory
        self.instr_mem = []       # Instruction memory
        self.pc = 0               # Program counter
        
        # Pipeline Registers
        self.IF_ID = None
        self.ID_EX = None
        self.EX_MEM = None
        self.MEM_WB = None
        
        # Control Signals
        self.stall = False
        self.flush = False
        
        # Statistics
        self.cycle = 0
        self.total_cycles = 0
        self.total_instructions = 0
        self.total_stalls = 0
        self.total_flushes = 0
        self.forwarding_ex_mem = 0
        self.forwarding_mem_wb = 0
        
        # Status Messages
        self.hazard_msg = "No Hazard"
        self.forwarding_msg = "No Forwarding"
        
        # Instruction Set (Opcodes)
        self.OPCODES = {
            'ADD':  0b0000,
            'SUB':  0b0001,
            'AND':  0b0010,
            'OR':   0b0011,
            'SLT':  0b0100,
            'ADDI': 0b0101,
            'ANDI': 0b0110,
            'ORI':  0b0111,
            'LW':   0b1000,
            'SW':   0b1001,
            'BEQ':  0b1010,
            'BNE':  0b1011,
            'J':    0b1100,
            'JAL':  0b1101,
            'JR':   0b1110,
            'NOP':  0b1111
        }
        
        # Reverse mapping for disassembly
        self.OPCODE_NAMES = {v: k for k, v in self.OPCODES.items()}
    
    def reset(self):
        """Reset CPU to initial state"""
        self.registers = [0] * 8
        self.memory = [0] * 64
        self.pc = 0
        self.cycle = 0
        
        # Clear pipeline
        self.IF_ID = None
        self.ID_EX = None
        self.EX_MEM = None
        self.MEM_WB = None
        
        # Reset statistics
        self.total_cycles = 0
        self.total_instructions = 0
        self.total_stalls = 0
        self.total_flushes = 0
        self.forwarding_ex_mem = 0
        self.forwarding_mem_wb = 0
        
        self.hazard_msg = "No Hazard"
        self.forwarding_msg = "No Forwarding"
    
    def load_program(self, instructions):
        """Load program into instruction memory"""
        self.instr_mem = instructions.copy()
        self.reset()
    
    def step(self):
        """Execute one clock cycle"""
        self.cycle += 1
        self.total_cycles += 1
        
        # Reset per-cycle status
        self.hazard_msg = "No Hazard"
        self.forwarding_msg = "No Forwarding"
        self.stall = False
        self.flush = False
        
        # Check for load-use hazard
        if self.detect_load_use_hazard():
            self._handle_stall()
            return
        
        # Execute pipeline stages (reverse order)
        self._writeback_stage()
        self._memory_stage()
        self._execute_stage()
        self._decode_stage()
        self._fetch_stage()
        
        # Ensure R0 is always 0
        self.registers[0] = 0
    
    def _handle_stall(self):
        """Handle pipeline stall"""
        self.stall = True
        self.total_stalls += 1
        self.hazard_msg = "⚠️ LOAD-USE HAZARD: Pipeline Stalled"
        
        # WB and MEM continue
        self._writeback_stage()
        self._memory_stage()
        
        # Insert bubble in EX
        self.EX_MEM = None
        
        # Keep IF and ID frozen (don't update)
    
    def _writeback_stage(self):
        """WB Stage: Write result to register file"""
        if self.MEM_WB and self.MEM_WB['write_reg']:
            if self.MEM_WB['rd'] != 0:
                self.registers[self.MEM_WB['rd']] = self.MEM_WB['write_data'] & 0xFFFF
    
    def _memory_stage(self):
        """MEM Stage: Access data memory"""
        new_MEM_WB = None
        
        if self.EX_MEM:
            opcode = self.EX_MEM['opcode']
            write_data = self.EX_MEM['alu_result']
            write_reg = self.EX_MEM['write_reg']
            rd = self.EX_MEM['rd']
            
            # Load Word
            if opcode == self.OPCODES['LW']:
                addr = self.EX_MEM['alu_result'] % 64
                write_data = self.memory[addr]
                write_reg = True
            
            # Store Word
            elif opcode == self.OPCODES['SW']:
                addr = self.EX_MEM['alu_result'] % 64
                self.memory[addr] = self.EX_MEM['rt_value'] & 0xFFFF
                write_reg = False
            
            new_MEM_WB = {
                'rd': rd,
                'write_dest': rd,
                'write_data': write_data,
                'write_reg': write_reg,
                'opcode': opcode
            }
        
        self.MEM_WB = new_MEM_WB
    
    def _execute_stage(self):
        """EX Stage: Execute operation"""
        new_EX_MEM = None
        
        if self.ID_EX:
            # Get forwarded values
            forward_rs, forward_rt, fwd_rs_src, fwd_rt_src = self.get_forwarding_values()
            
            rs_value = forward_rs if forward_rs is not None else self.ID_EX['rs_value']
            rt_value = forward_rt if forward_rt is not None else self.ID_EX['rt_value']
            
            # Update forwarding message
            if forward_rs is not None or forward_rt is not None:
                fwd_msg = []
                if forward_rs is not None:
                    fwd_msg.append(f"R{self.ID_EX['rs']} from {fwd_rs_src}")
                if forward_rt is not None:
                    fwd_msg.append(f"R{self.ID_EX['rt']} from {fwd_rt_src}")
                self.forwarding_msg = "✓ Forwarding: " + ", ".join(fwd_msg)
            
            opcode = self.ID_EX['opcode']
            alu_result = 0
            write_reg = False
            rd = 0
            branch_taken = False
            target_pc = 0
            
            # Execute based on opcode
            if opcode == self.OPCODES['ADD']:
                alu_result = (rs_value + rt_value) & 0xFFFF
                rd = self.ID_EX['rd']
                write_reg = True
            
            elif opcode == self.OPCODES['SUB']:
                alu_result = (rs_value - rt_value) & 0xFFFF
                rd = self.ID_EX['rd']
                write_reg = True
            
            elif opcode == self.OPCODES['AND']:
                alu_result = (rs_value & rt_value) & 0xFFFF
                rd = self.ID_EX['rd']
                write_reg = True
            
            elif opcode == self.OPCODES['OR']:
                alu_result = (rs_value | rt_value) & 0xFFFF
                rd = self.ID_EX['rd']
                write_reg = True
            
            elif opcode == self.OPCODES['SLT']:
                alu_result = 1 if rs_value < rt_value else 0
                rd = self.ID_EX['rd']
                write_reg = True
            
            elif opcode == self.OPCODES['ADDI']:
                imm = self.ID_EX['imm']  # Use as unsigned (0-63)
                alu_result = (rs_value + imm) & 0xFFFF
                rd = self.ID_EX['rt']
                write_reg = True
            
            elif opcode == self.OPCODES['ANDI']:
                alu_result = (rs_value & self.ID_EX['imm']) & 0xFFFF
                rd = self.ID_EX['rt']
                write_reg = True
            
            elif opcode == self.OPCODES['ORI']:
                alu_result = (rs_value | self.ID_EX['imm']) & 0xFFFF
                rd = self.ID_EX['rt']
                write_reg = True
            
            elif opcode == self.OPCODES['LW']:
                imm = self._sign_extend(self.ID_EX['imm'], 6)
                alu_result = (rs_value + imm) & 0xFFFF
                rd = self.ID_EX['rt']
                write_reg = True
            
            elif opcode == self.OPCODES['SW']:
                imm = self._sign_extend(self.ID_EX['imm'], 6)
                alu_result = (rs_value + imm) & 0xFFFF
                rd = 0
                write_reg = False
            
            elif opcode == self.OPCODES['BEQ']:
                if rs_value == rt_value:
                    offset = self._sign_extend(self.ID_EX['imm'], 6)
                    target_pc = (self.ID_EX['pc'] + 1 + offset) & 0xFFF
                    branch_taken = True
            
            elif opcode == self.OPCODES['BNE']:
                if rs_value != rt_value:
                    offset = self._sign_extend(self.ID_EX['imm'], 6)
                    target_pc = (self.ID_EX['pc'] + 1 + offset) & 0xFFF
                    branch_taken = True
            
            elif opcode == self.OPCODES['J']:
                target_pc = self.ID_EX['addr'] & 0xFFF
                branch_taken = True
            
            elif opcode == self.OPCODES['JAL']:
                self.registers[7] = (self.ID_EX['pc'] + 1) & 0xFFF
                target_pc = self.ID_EX['addr'] & 0xFFF
                branch_taken = True
            
            elif opcode == self.OPCODES['JR']:
                target_pc = rs_value & 0xFFF
                branch_taken = True
            
            # Handle branches
            if branch_taken:
                self.pc = target_pc
                self.flush = True
                self.total_flushes += 1
                self.hazard_msg = "⚡ CONTROL HAZARD: Branch Taken (Flushed)"
            
            new_EX_MEM = {
                'opcode': opcode,
                'alu_result': alu_result,
                'rt_value': rt_value,
                'rd': rd,
                'write_dest': rd,
                'write_reg': write_reg
            }
        
        self.EX_MEM = new_EX_MEM
    
    def _decode_stage(self):
        """ID Stage: Decode instruction and read registers"""
        new_ID_EX = None
        
        if self.IF_ID and not self.flush:
            instr = self.IF_ID['instr']
            pc = self.IF_ID['pc']
            
            # Decode instruction fields
            opcode = int(instr[0:4], 2)
            rs = int(instr[4:7], 2)
            rt = int(instr[7:10], 2)
            rd = int(instr[10:13], 2)
            imm = int(instr[10:16], 2)
            addr = int(instr[4:16], 2)
            
            # Read registers
            rs_value = self.registers[rs]
            rt_value = self.registers[rt]
            
            new_ID_EX = {
                'opcode': opcode,
                'pc': pc,
                'rs': rs,
                'rt': rt,
                'rd': rd,
                'rs_value': rs_value,
                'rt_value': rt_value,
                'imm': imm,
                'addr': addr
            }
            
            self.total_instructions += 1
        
        self.ID_EX = new_ID_EX
    
    def _fetch_stage(self):
        """IF Stage: Fetch instruction from memory"""
        new_IF_ID = None
        
        if not self.flush and self.pc < len(self.instr_mem):
            new_IF_ID = {
                'instr': self.instr_mem[self.pc],
                'pc': self.pc
            }
            self.pc = (self.pc + 1) & 0xFFF
        
        self.IF_ID = new_IF_ID
    
    def detect_load_use_hazard(self):
        """Detect load-use hazard (LW followed by dependent instruction)"""
        if not self.ID_EX or not self.IF_ID:
            return False
        
        # Check if EX stage has LW
        if self.ID_EX['opcode'] != self.OPCODES['LW']:
            return False
        
        # Decode IF_ID instruction
        instr = self.IF_ID['instr']
        opcode = int(instr[0:4], 2)
        rs = int(instr[4:7], 2)
        rt = int(instr[7:10], 2)
        
        lw_dest = self.ID_EX['rt']
        
        # Check if instruction uses LW destination
        if opcode in [self.OPCODES['ADD'], self.OPCODES['SUB'], self.OPCODES['AND'], 
                      self.OPCODES['OR'], self.OPCODES['SLT']]:
            if rs == lw_dest or rt == lw_dest:
                return True
        
        elif opcode in [self.OPCODES['ADDI'], self.OPCODES['ANDI'], self.OPCODES['ORI']]:
            if rs == lw_dest:
                return True
        
        elif opcode in [self.OPCODES['SW'], self.OPCODES['BEQ'], self.OPCODES['BNE']]:
            if rs == lw_dest or rt == lw_dest:
                return True
        
        return False
    
    def get_forwarding_values(self):
        """Determine forwarding values from EX/MEM and MEM/WB stages"""
        if not self.ID_EX:
            return None, None, None, None
        
        forward_rs = None
        forward_rt = None
        forward_rs_source = None
        forward_rt_source = None
        
        rs = self.ID_EX['rs']
        rt = self.ID_EX['rt']
        
        # EX/MEM Forwarding (higher priority)
        if self.EX_MEM and self.EX_MEM.get('write_reg') and self.EX_MEM.get('write_dest', 0) != 0:
            if self.EX_MEM['write_dest'] == rs:
                forward_rs = self.EX_MEM['alu_result']
                forward_rs_source = 'EX/MEM'
                self.forwarding_ex_mem += 1
            
            if self.EX_MEM['write_dest'] == rt:
                forward_rt = self.EX_MEM['alu_result']
                forward_rt_source = 'EX/MEM'
                self.forwarding_ex_mem += 1
        
        # MEM/WB Forwarding (lower priority)
        if self.MEM_WB and self.MEM_WB.get('write_reg') and self.MEM_WB.get('write_dest', 0) != 0:
            if forward_rs is None and self.MEM_WB['write_dest'] == rs:
                forward_rs = self.MEM_WB['write_data']
                forward_rs_source = 'MEM/WB'
                self.forwarding_mem_wb += 1
            
            if forward_rt is None and self.MEM_WB['write_dest'] == rt:
                forward_rt = self.MEM_WB['write_data']
                forward_rt_source = 'MEM/WB'
                self.forwarding_mem_wb += 1
        
        return forward_rs, forward_rt, forward_rs_source, forward_rt_source
    
    def _sign_extend(self, value, bits):
        """Sign extend a value from 'bits' to 16 bits"""
        sign_bit = 1 << (bits - 1)
        if value & sign_bit:
            mask = (1 << bits) - 1
            return value | (~mask & 0xFFFF)
        return value
    
    def is_pipeline_empty(self):
        """Check if pipeline is empty"""
        return not any([self.IF_ID, self.ID_EX, self.EX_MEM, self.MEM_WB])
    
    def is_program_complete(self):
        """Check if program execution is complete"""
        return self.pc >= len(self.instr_mem) and self.is_pipeline_empty()
    
    def get_stats(self):
        """Get execution statistics"""
        total_fwd = self.forwarding_ex_mem + self.forwarding_mem_wb
        cpi = self.cycle / max(self.total_instructions, 1)
        
        return {
            'cycles': self.cycle,
            'instructions': self.total_instructions,
            'stalls': self.total_stalls,
            'flushes': self.total_flushes,
            'forwards': total_fwd,
            'cpi': cpi
        }
