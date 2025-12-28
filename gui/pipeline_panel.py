"""
Pipeline Panel Component
Displays current state of all 5 pipeline stages
"""

import tkinter as tk
from tkinter import ttk

class PipelinePanel(ttk.LabelFrame):
    """Panel displaying pipeline stages"""
    
    def __init__(self, parent, cpu, assembler):
        super().__init__(parent, text="Pipeline Stages", padding=10)
        self.cpu = cpu
        self.assembler = assembler
        
        self._create_pipeline_display()
    
    def _create_pipeline_display(self):
        """Create pipeline stages display"""
        # Stage colors
        colors = {
            'IF': '#2196f3',   # Blue
            'ID': '#ff9800',   # Orange  
            'EX': '#9c27b0',   # Purple
            'MEM': '#4caf50',  # Green
            'WB': '#f44336'    # Red
        }
        
        self.stage_frames = {}
        
        for stage_name in ['IF', 'ID', 'EX', 'MEM', 'WB']:
            # Stage frame
            frame = ttk.Frame(self, relief=tk.RIDGE, borderwidth=2)
            frame.pack(fill=tk.X, pady=3)
            
            # Stage label
            label = tk.Label(frame, text=stage_name, bg=colors[stage_name],
                           fg='white', font=('Arial', 10, 'bold'),
                           width=8, anchor=tk.W, padx=5)
            label.pack(side=tk.LEFT)
            
            # Content label
            content = ttk.Label(frame, text="NOP", font=('Courier', 9),
                              anchor=tk.W, padding=5)
            content.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            self.stage_frames[stage_name] = (frame, content)
    
    def update(self):
        """Update pipeline display"""
        self._update_stage("IF", self.cpu.IF_ID)
        self._update_stage("ID", self.cpu.ID_EX)
        self._update_stage("EX", self.cpu.EX_MEM)
        self._update_stage("MEM", self.cpu.MEM_WB)
        self._update_stage("WB", self.cpu.MEM_WB)
    
    def _update_stage(self, stage_name, stage_data):
        """Update individual pipeline stage"""
        frame, content_lbl = self.stage_frames[stage_name]
        
        if stage_data is None:
            content_lbl.config(text="NOP")
            return
        
        if stage_name == "IF" and 'instr' in stage_data:
            asm = self.assembler.disassemble(stage_data['instr'])
            content_lbl.config(text=asm)
        
        elif stage_name in ["ID", "EX"] and 'opcode' in stage_data:
            opcode = stage_data['opcode']
            opcode_names = {v: k for k, v in self.cpu.OPCODES.items()}
            op_name = opcode_names.get(opcode, "UNK")
            content_lbl.config(text=op_name)
        
        elif stage_name in ["MEM", "WB"] and 'opcode' in stage_data:
            opcode = stage_data['opcode']
            opcode_names = {v: k for k, v in self.cpu.OPCODES.items()}
            op_name = opcode_names.get(opcode, "UNK")
            
            if 'write_data' in stage_data:
                content_lbl.config(text=f"{op_name} (→R{stage_data.get('rd', 0)}={stage_data['write_data']})")
            else:
                content_lbl.config(text=op_name)
