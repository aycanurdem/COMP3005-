# 16-bit MIPS Pipelined CPU Simulator

A comprehensive educational simulator for a 16-bit MIPS pipelined CPU with hazard detection and forwarding.

## Features

- ✅ **5-Stage Pipeline**: IF → ID → EX → MEM → WB
- ✅ **16 Instructions**: Full MIPS instruction set (ADD, SUB, AND, OR, SLT, ADDI, ANDI, ORI, LW, SW, BEQ, BNE, J, JAL, JR, NOP)
- ✅ **Hazard Detection**: Load-use hazards with automatic stalling
- ✅ **Data Forwarding**: EX/MEM and MEM/WB forwarding paths
- ✅ **Control Hazards**: Branch/jump handling with pipeline flush
- ✅ **Real-time Visualization**: Live pipeline stage display
- ✅ **Code Editor**: Built-in assembly editor with line numbers
- ✅ **Statistics**: Cycles, CPI, stalls, flushes, forwards tracking

## Project Structure

```
mips_simulator_project/
├── main.py                 # Application entry point
├── core/                   # Backend (CPU logic)
│   ├── __init__.py
│   ├── cpu.py             # CPU core implementation
│   └── assembler.py       # Assembly to binary converter
├── gui/                    # Frontend (User interface)
│   ├── __init__.py
│   ├── main_window.py     # Main application window
│   ├── code_editor.py     # Code editor component
│   ├── stats_panel.py     # Statistics display
│   ├── registers_panel.py # Register file display
│   ├── pipeline_panel.py  # Pipeline visualization
│   └── memory_panel.py    # Memory displays
├── examples/               # Example programs
├── tests/                  # Unit tests
└── docs/                   # Documentation
```

## Installation

### Requirements
- Python 3.7 or higher
- Tkinter (usually comes with Python)

### Quick Start

```bash
# Clone or download the project
cd mips_simulator_project

# Run the simulator
python main.py
```

## Usage

### 1. Write Assembly Code
Use the code editor on the left to write your assembly program.

**Example:**
```assembly
# Simple addition
ADDI r1, r0, 15    # r1 = 15
NOP
NOP
ADDI r2, r0, 25    # r2 = 25  
NOP
NOP
ADD r3, r1, r2     # r3 = 40
NOP
NOP
SW r3, 0(r0)       # MEM[0] = 40
NOP
```

### 2. Load Code
Click the **"📝 Load Code"** button to assemble and load your program into the CPU.

### 3. Execute
- **▶️ Step**: Execute one clock cycle
- **⏩ Run All**: Execute until program completes
- **🔄 Reset**: Reset CPU and reload code

### 4. Monitor Execution
Watch the real-time updates in:
- **Execution Tab**: Statistics, registers, pipeline stages
- **Memory Tab**: Instruction memory and data memory

## Instruction Set

### R-Type Instructions
| Instruction | Format | Description |
|-------------|--------|-------------|
| ADD | `ADD rd, rs, rt` | rd = rs + rt |
| SUB | `SUB rd, rs, rt` | rd = rs - rt |
| AND | `AND rd, rs, rt` | rd = rs & rt |
| OR | `OR rd, rs, rt` | rd = rs \| rt |
| SLT | `SLT rd, rs, rt` | rd = (rs < rt) ? 1 : 0 |
| JR | `JR rs` | PC = rs |

### I-Type Instructions
| Instruction | Format | Description |
|-------------|--------|-------------|
| ADDI | `ADDI rt, rs, imm` | rt = rs + imm (0-63) |
| ANDI | `ANDI rt, rs, imm` | rt = rs & imm |
| ORI | `ORI rt, rs, imm` | rt = rs \| imm |
| LW | `LW rt, imm(rs)` | rt = MEM[rs + imm] |
| SW | `SW rt, imm(rs)` | MEM[rs + imm] = rt |
| BEQ | `BEQ rs, rt, offset` | if (rs == rt) PC += offset |
| BNE | `BNE rs, rt, offset` | if (rs != rt) PC += offset |

### J-Type Instructions
| Instruction | Format | Description |
|-------------|--------|-------------|
| J | `J address` | PC = address |
| JAL | `JAL address` | R7 = PC+1, PC = address |

### Special
| Instruction | Format | Description |
|-------------|--------|-------------|
| NOP | `NOP` | No operation |

## Important Notes

### 6-Bit Immediate Limitation
⚠️ **CRITICAL**: All immediate values are limited to 6 bits (0-63)

```assembly
# CORRECT ✓
ADDI r1, r0, 10    # ✓ 10 is in range
ADDI r2, r0, 63    # ✓ 63 is max value

# INCORRECT ✗
ADDI r1, r0, 99    # ✗ 99 > 63, will cause errors!
ADDI r2, r0, 100   # ✗ 100 > 63, will cause errors!
```

### Pipeline Hazards
To avoid data hazards, add **2 NOPs** after instructions that write to registers:

```assembly
ADDI r1, r0, 10    # Writes to r1
NOP                # Wait
NOP                # Wait
ADD r2, r1, r0     # Now safe to use r1
```

### Load-Use Hazard
The simulator automatically stalls on load-use hazards, but adding NOPs improves performance:

```assembly
LW r1, 0(r0)       # Load from memory
NOP                # Recommended
NOP                # Recommended
ADD r2, r1, r0     # Use loaded value
```

## Example Programs

See the `examples/` directory for sample programs:
- `simple_addition.asm` - Basic arithmetic
- `fibonacci.asm` - Fibonacci sequence
- `array_sum.asm` - Array summation
- `all_instructions.asm` - Test all instructions

## Architecture Details

### CPU Components
- **8 Registers**: R0-R7 (R0 is hardwired to 0)
- **64 Words Data Memory**: 16-bit words
- **Instruction Memory**: Dynamic size
- **16-bit Instructions**: Compact encoding
- **5-Stage Pipeline**: IF, ID, EX, MEM, WB

### Pipeline Stages
1. **IF (Instruction Fetch)**: Fetch instruction from memory
2. **ID (Instruction Decode)**: Decode and read registers
3. **EX (Execute)**: ALU operations, branch calculation
4. **MEM (Memory Access)**: Load/store operations
5. **WB (Write Back)**: Write result to register file

### Hazard Handling
- **Load-Use Hazard**: Automatic pipeline stall
- **Data Hazard**: Forwarding from EX/MEM and MEM/WB
- **Control Hazard**: Pipeline flush on branch/jump

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Adding New Features
1. **Backend (CPU Logic)**: Modify files in `core/`
2. **Frontend (GUI)**: Modify files in `gui/`
3. **Keep Separation**: Backend should not import GUI

## License

Educational use only.

## Contributors

Computer Organization Course Project

## Support

For questions or issues, refer to the documentation in the `docs/` directory.
