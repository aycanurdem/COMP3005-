"""
Main Window GUI for MIPS Simulator
Contains the main application window and layout
"""

import tkinter as tk
from tkinter import ttk, messagebox
from .code_editor import CodeEditor
from .stats_panel import StatsPanel
from .registers_panel import RegistersPanel
from .pipeline_panel import PipelinePanel
from .memory_panel import MemoryPanel

class MainWindow:
    """Main application window"""
    
    def __init__(self, root, cpu, assembler):
        self.root = root
        self.cpu = cpu
        self.assembler = assembler
        
        # Configure window
        self.root.title("16-bit MIPS Pipelined Simulator")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Create main layout
        self._create_layout()
        
        # Load default program
        self._load_default_program()
    
    def _create_layout(self):
        """Create main window layout"""
        # Main container
        main_container = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel (Code Editor)
        left_panel = ttk.Frame(main_container, width=450)
        main_container.add(left_panel, weight=1)
        
        # Right panel (Info displays)
        right_panel = ttk.Frame(main_container)
        main_container.add(right_panel, weight=2)
        
        # Create components
        self._create_left_panel(left_panel)
        self._create_right_panel(right_panel)
    
    def _create_left_panel(self, parent):
        """Create left panel with code editor and controls"""
        # Title
        title_label = ttk.Label(parent, text="Assembly Code Editor",
                               font=("Arial", 12, "bold"))
        title_label.pack(pady=5)
        
        # Code Editor
        self.code_editor = CodeEditor(parent, self.assembler)
        self.code_editor.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Control buttons
        self._create_control_buttons(parent)
        
        # Instruction reference
        self._create_instruction_reference(parent)
    
    def _create_control_buttons(self, parent):
        """Create control buttons"""
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Button style
        style = ttk.Style()
        style.configure('Action.TButton', font=('Arial', 10, 'bold'))
        
        # Load Code button
        load_btn = ttk.Button(btn_frame, text="📝 Load Code",
                             command=self.load_code,
                             style='Action.TButton')
        load_btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        
        # Step button
        step_btn = ttk.Button(btn_frame, text="▶️ Step",
                             command=self.step,
                             style='Action.TButton')
        step_btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        
        # Run All button
        run_btn = ttk.Button(btn_frame, text="⏩ Run All",
                            command=self.run_all,
                            style='Action.TButton')
        run_btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        
        # Reset button
        reset_btn = ttk.Button(btn_frame, text="🔄 Reset",
                              command=self.reset,
                              style='Action.TButton')
        reset_btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
    
    def _create_instruction_reference(self, parent):
        """Create instruction reference section"""
        ref_frame = ttk.LabelFrame(parent, text="Quick Reference", padding=5)
        ref_frame.pack(fill=tk.BOTH, padx=5, pady=5)
        
        ref_text = tk.Text(ref_frame, height=8, font=("Courier", 9),
                          bg="#f5f5f5", relief=tk.FLAT)
        ref_text.pack(fill=tk.BOTH, expand=True)
        
        reference = """R-Type: ADD, SUB, AND, OR, SLT, JR
I-Type: ADDI, ANDI, ORI, LW, SW, BEQ, BNE
J-Type: J, JAL
Special: NOP

Examples:
  ADDI r1, r0, 10    # r1 = 10 (0-63 only!)
  ADD r3, r1, r2     # r3 = r1 + r2
  SW r1, 5(r0)       # MEM[5] = r1
  BEQ r1, r2, 3      # if r1==r2, skip 3"""
        
        ref_text.insert("1.0", reference)
        ref_text.config(state=tk.DISABLED)
    
    def _create_right_panel(self, parent):
        """Create right panel with all info displays"""
        # Create notebook for tabs
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Execution View
        exec_tab = ttk.Frame(notebook)
        notebook.add(exec_tab, text="Execution")
        self._create_execution_tab(exec_tab)
        
        # Tab 2: Memory View
        mem_tab = ttk.Frame(notebook)
        notebook.add(mem_tab, text="Memory & Instructions")
        self._create_memory_tab(mem_tab)
    
    def _create_execution_tab(self, parent):
        """Create execution tab with stats, registers, pipeline"""
        # Top: Statistics
        self.stats_panel = StatsPanel(parent, self.cpu)
        self.stats_panel.pack(fill=tk.X, padx=5, pady=5)
        
        # Middle: Registers and Pipeline
        middle_frame = ttk.Frame(parent)
        middle_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Registers (left)
        self.registers_panel = RegistersPanel(middle_frame, self.cpu)
        self.registers_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Pipeline (right)
        self.pipeline_panel = PipelinePanel(middle_frame, self.cpu, self.assembler)
        self.pipeline_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    def _create_memory_tab(self, parent):
        """Create memory tab with instruction and data memory"""
        self.memory_panel = MemoryPanel(parent, self.cpu, self.assembler)
        self.memory_panel.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def _load_default_program(self):
        """Load default example program"""
        default_code = """# Simple Addition Example
# 6-bit immediate range: 0-63

ADDI r1, r0, 15     # r1 = 15
NOP
NOP
ADDI r2, r0, 25     # r2 = 25
NOP
NOP
ADD r3, r1, r2      # r3 = 15 + 25 = 40
NOP
NOP
SW r3, 0(r0)        # MEM[0] = 40
NOP
NOP
NOP"""
        
        self.code_editor.set_text(default_code)
    
    def load_code(self):
        """Load code from editor into CPU"""
        try:
            code = self.code_editor.get_text()
            instructions = self.assembler.assemble(code)
            
            if not instructions:
                messagebox.showwarning("Warning", "No valid instructions found!")
                return
            
            self.cpu.load_program(instructions)
            self.update_display()
            
            messagebox.showinfo("Success", 
                              f"Loaded {len(instructions)} instructions successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load code:\n{str(e)}")
    
    def step(self):
        """Execute one cycle"""
        if self.cpu.is_program_complete():
            messagebox.showinfo("Complete", "✓ Program execution completed!")
            return
        
        self.cpu.step()
        self.update_display()
        self.code_editor.highlight_current_line(self.cpu.pc)
    
    def run_all(self):
        """Execute until program completes"""
        max_cycles = 1000
        initial_cycle = self.cpu.cycle
        
        while not self.cpu.is_program_complete() and self.cpu.cycle - initial_cycle < max_cycles:
            self.cpu.step()
        
        self.update_display()
        self.code_editor.highlight_current_line(self.cpu.pc)
        
        stats = self.cpu.get_stats()
        
        if self.cpu.is_program_complete():
            messagebox.showinfo("Complete", 
                              f"✓ Program completed!\n\n"
                              f"Cycles: {stats['cycles']}\n"
                              f"Instructions: {stats['instructions']}\n"
                              f"CPI: {stats['cpi']:.2f}")
        else:
            messagebox.showwarning("Timeout", 
                                 f"Execution stopped after {max_cycles} cycles\n"
                                 f"(possible infinite loop)")
    
    def reset(self):
        """Reset CPU and reload code"""
        self.cpu.reset()
        # Initialize some test values in memory
        self.cpu.memory[0] = 100
        self.cpu.memory[1] = 200
        self.cpu.memory[2] = 50
        self.update_display()
        self.code_editor.clear_highlight()
    
    def update_display(self):
        """Update all display panels"""
        self.stats_panel.update()
        self.registers_panel.update()
        self.pipeline_panel.update()
        self.memory_panel.update()
