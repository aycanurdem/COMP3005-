"""
Memory Panel Component
Displays instruction memory and data memory
"""

import tkinter as tk
from tkinter import ttk

class MemoryPanel(ttk.Frame):
    """Panel displaying memory contents"""
    
    def __init__(self, parent, cpu, assembler):
        super().__init__(parent)
        self.cpu = cpu
        self.assembler = assembler
        
        self._create_memory_display()
    
    def _create_memory_display(self):
        """Create memory displays"""
        # Create two columns: Instruction Memory and Data Memory
        
        # Instruction Memory (left)
        instr_frame = ttk.LabelFrame(self, text="Instruction Memory", padding=10)
        instr_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        columns = ('Address', 'Binary', 'Assembly')
        self.instr_tree = ttk.Treeview(instr_frame, columns=columns, show='headings', height=25)
        
        self.instr_tree.heading('Address', text='Addr')
        self.instr_tree.heading('Binary', text='Binary')
        self.instr_tree.heading('Assembly', text='Assembly')
        
        self.instr_tree.column('Address', width=50)
        self.instr_tree.column('Binary', width=120)
        self.instr_tree.column('Assembly', width=200)
        
        instr_scroll = ttk.Scrollbar(instr_frame, orient=tk.VERTICAL, command=self.instr_tree.yview)
        self.instr_tree.configure(yscrollcommand=instr_scroll.set)
        
        self.instr_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        instr_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.instr_tree.tag_configure("current", background="#ffeb3b")
        
        # Data Memory (right)
        data_frame = ttk.LabelFrame(self, text="Data Memory", padding=10)
        data_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        columns = ('Address', 'Decimal', 'Hex')
        self.data_tree = ttk.Treeview(data_frame, columns=columns, show='headings', height=25)
        
        self.data_tree.heading('Address', text='Address')
        self.data_tree.heading('Decimal', text='Decimal')
        self.data_tree.heading('Hex', text='Hex')
        
        self.data_tree.column('Address', width=80)
        self.data_tree.column('Decimal', width=80)
        self.data_tree.column('Hex', width=100)
        
        data_scroll = ttk.Scrollbar(data_frame, orient=tk.VERTICAL, command=self.data_tree.yview)
        self.data_tree.configure(yscrollcommand=data_scroll.set)
        
        self.data_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        data_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    
    def update(self):
        """Update memory displays"""
        self._update_instruction_memory()
        self._update_data_memory()
    
    def _update_instruction_memory(self):
        """Update instruction memory display"""
        # Clear existing
        for item in self.instr_tree.get_children():
            self.instr_tree.delete(item)
        
        # Add instructions
        for i, instr in enumerate(self.cpu.instr_mem):
            asm = self.assembler.disassemble(instr)
            tag = "current" if i == self.cpu.pc else ""
            self.instr_tree.insert("", "end", values=(i, instr, asm), tags=(tag,))
    
    def _update_data_memory(self):
        """Update data memory display"""
        # Clear existing
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
        
        # Add memory values (show first 32 locations)
        for i in range(min(32, len(self.cpu.memory))):
            val = self.cpu.memory[i]
            self.data_tree.insert("", "end", values=(i, val, f'0x{val:04X}'))
