"""
MIPS 16-bit Simulator - Core Package
Backend components for CPU simulation
"""

from .cpu import PipelinedCPU
from .assembler import Assembler

__all__ = ['PipelinedCPU', 'Assembler']
