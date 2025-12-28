"""
Statistics Panel Component
Displays CPU execution statistics and hazard information
"""

import tkinter as tk
from tkinter import ttk

class StatsPanel(ttk.LabelFrame):
    """Panel displaying CPU statistics"""
    
    def __init__(self, parent, cpu):
        super().__init__(parent, text="Execution Statistics", padding=10)
        self.cpu = cpu
        
        self._create_stats_display()
    
    def _create_stats_display(self):
        """Create statistics display"""
        # Stats grid
        stats_frame = ttk.Frame(self)
        stats_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid
        for i in range(3):
            stats_frame.columnconfigure(i, weight=1)
        
        # Row 1: Cycle, PC, Instructions
        ttk.Label(stats_frame, text="Cycle:", font=("Arial", 10, "bold")).grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.cycle_lbl = ttk.Label(stats_frame, text="0", font=("Arial", 10))
        self.cycle_lbl.grid(row=0, column=0, sticky=tk.E, padx=5, pady=2)
        
        ttk.Label(stats_frame, text="PC:", font=("Arial", 10, "bold")).grid(
            row=0, column=1, sticky=tk.W, padx=5, pady=2)
        self.pc_lbl = ttk.Label(stats_frame, text="0", font=("Arial", 10))
        self.pc_lbl.grid(row=0, column=1, sticky=tk.E, padx=5, pady=2)
        
        ttk.Label(stats_frame, text="Instructions:", font=("Arial", 10, "bold")).grid(
            row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.instr_lbl = ttk.Label(stats_frame, text="0", font=("Arial", 10))
        self.instr_lbl.grid(row=0, column=2, sticky=tk.E, padx=5, pady=2)
        
        # Row 2: Stalls, Flushes, Forwards
        ttk.Label(stats_frame, text="Stalls:", font=("Arial", 10, "bold")).grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.stall_lbl = ttk.Label(stats_frame, text="0", font=("Arial", 10))
        self.stall_lbl.grid(row=1, column=0, sticky=tk.E, padx=5, pady=2)
        
        ttk.Label(stats_frame, text="Flushes:", font=("Arial", 10, "bold")).grid(
            row=1, column=1, sticky=tk.W, padx=5, pady=2)
        self.flush_lbl = ttk.Label(stats_frame, text="0", font=("Arial", 10))
        self.flush_lbl.grid(row=1, column=1, sticky=tk.E, padx=5, pady=2)
        
        ttk.Label(stats_frame, text="Forwards:", font=("Arial", 10, "bold")).grid(
            row=1, column=2, sticky=tk.W, padx=5, pady=2)
        self.fwd_lbl = ttk.Label(stats_frame, text="0", font=("Arial", 10))
        self.fwd_lbl.grid(row=1, column=2, sticky=tk.E, padx=5, pady=2)
        
        # Hazard status
        hazard_frame = ttk.Frame(stats_frame)
        hazard_frame.grid(row=2, column=0, columnspan=3, sticky=tk.EW, pady=10)
        
        ttk.Label(hazard_frame, text="Hazard Status:", 
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        self.hazard_status = ttk.Label(hazard_frame, text="No Hazard",
                                      font=("Arial", 10), foreground="#2e7d32")
        self.hazard_status.pack(side=tk.LEFT, padx=5)
        
        # Forwarding status
        forward_frame = ttk.Frame(stats_frame)
        forward_frame.grid(row=3, column=0, columnspan=3, sticky=tk.EW)
        
        ttk.Label(forward_frame, text="Forwarding:", 
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        self.forward_status = ttk.Label(forward_frame, text="No Forwarding",
                                       font=("Arial", 10), foreground="#666666")
        self.forward_status.pack(side=tk.LEFT, padx=5)
    
    def update(self):
        """Update statistics display"""
        stats = self.cpu.get_stats()
        
        self.cycle_lbl.config(text=str(self.cpu.cycle))
        self.pc_lbl.config(text=str(self.cpu.pc))
        self.instr_lbl.config(text=str(stats['instructions']))
        self.stall_lbl.config(text=str(stats['stalls']))
        self.flush_lbl.config(text=str(stats['flushes']))
        self.fwd_lbl.config(text=str(stats['forwards']))
        
        # Update hazard status with color
        if "STALL" in self.cpu.hazard_msg:
            self.hazard_status.config(text=self.cpu.hazard_msg, foreground="#d32f2f")
        elif "CONTROL" in self.cpu.hazard_msg:
            self.hazard_status.config(text=self.cpu.hazard_msg, foreground="#f57c00")
        else:
            self.hazard_status.config(text=self.cpu.hazard_msg, foreground="#2e7d32")
        
        self.forward_status.config(text=self.cpu.forwarding_msg)
