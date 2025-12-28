#!/usr/bin/env python3
"""
16-bit MIPS Pipelined Simulator
Main application entry point
"""

import tkinter as tk
from core import PipelinedCPU, Assembler
from gui import MainWindow

def main():
    """Main application function"""
    # Create root window
    root = tk.Tk()
    
    # Create CPU and Assembler
    cpu = PipelinedCPU()
    assembler = Assembler()
    
    # Create main window
    app = MainWindow(root, cpu, assembler)
    
    # Start application
    root.mainloop()

if __name__ == "__main__":
    main()
