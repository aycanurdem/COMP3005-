"""
Code Editor Component
Text editor with line numbers and syntax highlighting
"""

import tkinter as tk
from tkinter import ttk

class CodeEditor(ttk.Frame):
    """Code editor with line numbers"""
    
    def __init__(self, parent, assembler):
        super().__init__(parent)
        self.assembler = assembler
        
        # Create editor
        self._create_editor()
    
    def _create_editor(self):
        """Create text editor with line numbers"""
        # Container for line numbers and text
        editor_container = ttk.Frame(self)
        editor_container.pack(fill=tk.BOTH, expand=True)
        
        # Line numbers
        self.line_numbers = tk.Text(editor_container, width=4,
                                   font=("Courier", 10),
                                   bg="#e0e0e0", fg="#666666",
                                   state=tk.DISABLED,
                                   relief=tk.FLAT)
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        # Text editor
        self.text_widget = tk.Text(editor_container,
                                  font=("Courier", 10),
                                  bg="white",
                                  relief=tk.SUNKEN,
                                  undo=True,
                                  wrap=tk.NONE)
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(editor_container, command=self._on_scroll)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure text widget scrolling
        self.text_widget.config(yscrollcommand=scrollbar.set)
        self.line_numbers.config(yscrollcommand=scrollbar.set)
        
        # Bind events
        self.text_widget.bind('<KeyRelease>', lambda e: self._update_line_numbers())
        self.text_widget.bind('<MouseWheel>', self._sync_scroll)
        
        # Configure tags for highlighting
        self.text_widget.tag_config("current_line", background="#ffeb3b")
    
    def _on_scroll(self, *args):
        """Handle scrollbar movement"""
        self.text_widget.yview(*args)
        self.line_numbers.yview(*args)
    
    def _sync_scroll(self, event):
        """Synchronize line numbers with text scroll"""
        self.line_numbers.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"
    
    def _update_line_numbers(self):
        """Update line numbers"""
        line_count = int(self.text_widget.index('end-1c').split('.')[0])
        
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete('1.0', tk.END)
        
        line_numbers_text = '\n'.join(str(i) for i in range(1, line_count + 1))
        self.line_numbers.insert('1.0', line_numbers_text)
        
        self.line_numbers.config(state=tk.DISABLED)
    
    def get_text(self):
        """Get editor text"""
        return self.text_widget.get('1.0', tk.END)
    
    def set_text(self, text):
        """Set editor text"""
        self.text_widget.delete('1.0', tk.END)
        self.text_widget.insert('1.0', text)
        self._update_line_numbers()
    
    def highlight_current_line(self, pc):
        """Highlight current instruction line"""
        self.text_widget.tag_remove("current_line", '1.0', tk.END)
        
        # Find actual code line (skip comments and empty lines)
        code_lines = []
        for i, line in enumerate(self.get_text().split('\n'), 1):
            clean_line = line.split('#')[0].strip()
            if clean_line:
                code_lines.append(i)
        
        if pc < len(code_lines):
            actual_line = code_lines[pc]
            self.text_widget.tag_add("current_line", f"{actual_line}.0", f"{actual_line}.end")
            self.text_widget.see(f"{actual_line}.0")
    
    def clear_highlight(self):
        """Clear line highlighting"""
        self.text_widget.tag_remove("current_line", '1.0', tk.END)
