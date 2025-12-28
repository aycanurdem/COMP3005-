"""
Registers Panel Component
Displays register values in decimal and hexadecimal
"""

import tkinter as tk
from tkinter import ttk

class RegistersPanel(ttk.LabelFrame):
    """Panel displaying register values"""
    
    def __init__(self, parent, cpu):
        super().__init__(parent, text="Registers", padding=10)
        self.cpu = cpu
        
        self._create_registers_display()
    
    def _create_registers_display(self):
        """Create registers display"""
        # Create treeview for registers
        columns = ('Register', 'Decimal', 'Hex')
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=8)
        
        # Configure columns
        self.tree.heading('Register', text='Register')
        self.tree.heading('Decimal', text='Decimal')
        self.tree.heading('Hex', text='Hex')
        
        self.tree.column('Register', width=80, anchor=tk.W)
        self.tree.column('Decimal', width=80, anchor=tk.E)
        self.tree.column('Hex', width=80, anchor=tk.E)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Initialize with registers
        for i in range(8):
            self.tree.insert('', 'end', values=(f'R{i}', '0', '0x0000'))
    
    def update(self):
        """Update register display"""
        for i, item in enumerate(self.tree.get_children()):
            val = self.cpu.registers[i]
            self.tree.item(item, values=(f'R{i}', str(val), f'0x{val:04X}'))
