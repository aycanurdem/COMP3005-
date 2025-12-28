"""
MIPS 16-bit Assembler
Converts assembly code to binary machine code
"""

class Assembler:
    """
    Assembler for 16-bit MIPS
    Supports all 16 instructions with 16-bit encoding
    """
    
    def __init__(self):
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
    
    def assemble(self, code_text):
        """
        Assemble assembly code to binary instructions
        
        Args:
            code_text: String containing assembly code
            
        Returns:
            List of binary instruction strings
        """
        instructions = []
        lines = code_text.strip().split('\n')
        
        for line_num, line in enumerate(lines, 1):
            try:
                # Remove comments
                line = line.split('#')[0].strip()
                
                if not line:
                    continue
                
                # Tokenize
                parts = line.replace(',', ' ').replace('(', ' ').replace(')', ' ').split()
                
                if not parts:
                    continue
                
                op_name = parts[0].upper()
                
                # Check if valid instruction
                if op_name not in self.OPCODES:
                    print(f"Warning: Unknown instruction '{op_name}' at line {line_num}, inserting NOP")
                    instructions.append("1111000000000000")
                    continue
                
                # Encode instruction
                binary = self._encode_instruction(op_name, parts[1:])
                instructions.append(binary)
                
            except Exception as e:
                print(f"Error at line {line_num}: {e}")
                instructions.append("1111000000000000")  # NOP on error
        
        return instructions
    
    def _encode_instruction(self, op_name, operands):
        """Encode a single instruction"""
        opcode = self.OPCODES[op_name]
        
        # R-Type: ADD, SUB, AND, OR, SLT
        if op_name in ['ADD', 'SUB', 'AND', 'OR', 'SLT']:
            rd = self._parse_register(operands[0])
            rs = self._parse_register(operands[1])
            rt = self._parse_register(operands[2])
            return f"{opcode:04b}{rs:03b}{rt:03b}{rd:03b}000"
        
        # R-Type: JR
        elif op_name == 'JR':
            rs = self._parse_register(operands[0])
            return f"{opcode:04b}{rs:03b}000000000"
        
        # I-Type: ADDI, ANDI, ORI
        elif op_name in ['ADDI', 'ANDI', 'ORI']:
            rt = self._parse_register(operands[0])
            rs = self._parse_register(operands[1])
            imm = int(operands[2]) & 0x3F  # 6-bit immediate
            return f"{opcode:04b}{rs:03b}{rt:03b}{imm:06b}"
        
        # I-Type: LW, SW (format: LW rt, imm(rs))
        elif op_name in ['LW', 'SW']:
            rt = self._parse_register(operands[0])
            imm = int(operands[1]) & 0x3F  # 6-bit immediate
            rs = self._parse_register(operands[2]) if len(operands) > 2 else 0
            return f"{opcode:04b}{rs:03b}{rt:03b}{imm:06b}"
        
        # I-Type: BEQ, BNE
        elif op_name in ['BEQ', 'BNE']:
            rs = self._parse_register(operands[0])
            rt = self._parse_register(operands[1])
            imm = int(operands[2]) & 0x3F  # 6-bit immediate (offset)
            return f"{opcode:04b}{rs:03b}{rt:03b}{imm:06b}"
        
        # J-Type: J, JAL
        elif op_name in ['J', 'JAL']:
            addr = int(operands[0]) & 0xFFF  # 12-bit address
            return f"{opcode:04b}{addr:012b}"
        
        # NOP
        elif op_name == 'NOP':
            return "1111000000000000"
        
        else:
            return "1111000000000000"  # Default NOP
    
    def _parse_register(self, reg_str):
        """Parse register string (r1, R1, $1) to register number"""
        reg_str = reg_str.strip().lower()
        
        # Remove $ or r prefix
        if reg_str.startswith('$'):
            reg_str = reg_str[1:]
        elif reg_str.startswith('r'):
            reg_str = reg_str[1:]
        
        return int(reg_str) & 0x7  # 3-bit register (0-7)
    
    def disassemble(self, binary_str):
        """
        Disassemble binary instruction to assembly
        
        Args:
            binary_str: 16-bit binary string
            
        Returns:
            Assembly instruction string
        """
        if len(binary_str) != 16:
            return "INVALID"
        
        opcode = int(binary_str[0:4], 2)
        
        # Find instruction name
        opcode_names = {v: k for k, v in self.OPCODES.items()}
        op_name = opcode_names.get(opcode, "UNKNOWN")
        
        if op_name == 'NOP':
            return "NOP"
        
        # Decode fields
        rs = int(binary_str[4:7], 2)
        rt = int(binary_str[7:10], 2)
        rd = int(binary_str[10:13], 2)
        imm = int(binary_str[10:16], 2)
        addr = int(binary_str[4:16], 2)
        
        # R-Type
        if op_name in ['ADD', 'SUB', 'AND', 'OR', 'SLT']:
            return f"{op_name} r{rd}, r{rs}, r{rt}"
        
        elif op_name == 'JR':
            return f"JR r{rs}"
        
        # I-Type
        elif op_name in ['ADDI', 'ANDI', 'ORI']:
            return f"{op_name} r{rt}, r{rs}, {imm}"
        
        elif op_name in ['LW', 'SW']:
            return f"{op_name} r{rt}, {imm}(r{rs})"
        
        elif op_name in ['BEQ', 'BNE']:
            return f"{op_name} r{rs}, r{rt}, {imm}"
        
        # J-Type
        elif op_name in ['J', 'JAL']:
            return f"{op_name} {addr}"
        
        return "UNKNOWN"
