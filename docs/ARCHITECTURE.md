# MIPS Simulator - Proje Mimarisi

## 📁 Proje Yapısı

```
mips_simulator_project/
│
├── main.py                     # 🚀 Ana uygulama giriş noktası
│
├── core/                       # 🔧 Backend (Arka Yüz)
│   ├── __init__.py            # Package tanımı
│   ├── cpu.py                 # CPU core implementation
│   └── assembler.py           # Assembly → Binary çevirici
│
├── gui/                        # 🎨 Frontend (Ön Yüz)
│   ├── __init__.py            # Package tanımı
│   ├── main_window.py         # Ana pencere ve layout
│   ├── code_editor.py         # Kod editörü komponenti
│   ├── stats_panel.py         # İstatistik paneli
│   ├── registers_panel.py     # Register görüntüleme
│   ├── pipeline_panel.py      # Pipeline görselleştirme
│   └── memory_panel.py        # Memory görüntüleme
│
├── examples/                   # 📝 Örnek programlar
│   ├── simple_addition.asm    # Basit toplama örneği
│   ├── fibonacci.asm          # Fibonacci dizisi
│   └── all_instructions.asm   # Tüm instruction'lar
│
├── tests/                      # 🧪 Test dosyaları
│   └── (birim testler buraya)
│
├── docs/                       # 📚 Dökümanlar
│   └── (detaylı dökümanlar buraya)
│
└── README.md                   # 📖 Proje açıklaması
```

---

## 🔧 Backend (core/)

### 1. cpu.py - CPU Core
**Sorumluluk:** CPU simülasyonu ve pipeline execution

**Ana Sınıf:** `PipelinedCPU`

**Özellikler:**
- 5-aşamalı pipeline (IF, ID, EX, MEM, WB)
- 8 register (R0-R7)
- 64 word data memory
- Hazard detection
- Data forwarding
- Branch handling

**Önemli Metodlar:**
```python
def step()                      # Bir cycle çalıştır
def reset()                     # CPU'yu sıfırla
def load_program(instructions)  # Program yükle
def detect_load_use_hazard()   # Load-use hazard tespit
def get_forwarding_values()    # Forwarding değerleri al
def get_stats()                # İstatistikleri al
```

**Pipeline Aşamaları:**
```python
def _fetch_stage()      # IF: Instruction fetch
def _decode_stage()     # ID: Decode & register read
def _execute_stage()    # EX: ALU operations
def _memory_stage()     # MEM: Memory access
def _writeback_stage()  # WB: Register write
```

---

### 2. assembler.py - Assembler
**Sorumluluk:** Assembly kodunu binary'e çevirmek

**Ana Sınıf:** `Assembler`

**Önemli Metodlar:**
```python
def assemble(code_text)         # Assembly → Binary listesi
def disassemble(binary_str)     # Binary → Assembly string
def _encode_instruction()       # Tek instruction encode
def _parse_register()           # Register string parse
```

**Encoding Formatları:**
- **R-Type:** `[Op:4b][Rs:3b][Rt:3b][Rd:3b][Func:3b]`
- **I-Type:** `[Op:4b][Rs:3b][Rt:3b][Imm:6b]`
- **J-Type:** `[Op:4b][Address:12b]`

---

## 🎨 Frontend (gui/)

### 1. main_window.py - Ana Pencere
**Sorumluluk:** Uygulama ana penceresi ve layout yönetimi

**Ana Sınıf:** `MainWindow`

**Layout Yapısı:**
```
┌─────────────────────────────────────────┐
│         16-bit MIPS Simulator           │
├──────────────┬──────────────────────────┤
│              │                          │
│  Code Editor │   Stats Panel            │
│  (Sol)       │   Registers Panel        │
│              │   Pipeline Panel         │
│  Control     │   Memory Panel (tabs)    │
│  Buttons     │                          │
│              │                          │
└──────────────┴──────────────────────────┘
```

**Önemli Metodlar:**
```python
def load_code()        # Kodu yükle
def step()             # Bir adım çalıştır
def run_all()          # Tümünü çalıştır
def reset()            # Sıfırla
def update_display()   # Ekranı güncelle
```

---

### 2. code_editor.py - Kod Editörü
**Sorumluluk:** Assembly kod yazma ve düzenleme

**Özellikler:**
- Satır numaraları
- Mevcut satır vurgulama
- Scroll senkronizasyonu
- Syntax highlighting (gelecekte)

**Önemli Metodlar:**
```python
def get_text()                  # Editör metnini al
def set_text(text)              # Editör metnini set et
def highlight_current_line(pc)  # PC'deki satırı vurgula
def clear_highlight()           # Vurgulamayı temizle
```

---

### 3. stats_panel.py - İstatistik Paneli
**Sorumluluk:** Execution istatistiklerini gösterme

**Gösterilen Bilgiler:**
- Cycle sayısı
- PC (Program Counter)
- Instruction sayısı
- Stall sayısı
- Flush sayısı
- Forward sayısı
- Hazard durumu (renkli)
- Forwarding durumu

---

### 4. registers_panel.py - Register Paneli
**Sorumluluk:** Register değerlerini gösterme

**Gösterim Formatı:**
| Register | Decimal | Hex |
|----------|---------|-----|
| R0 | 0 | 0x0000 |
| R1 | 15 | 0x000F |
| ... | ... | ... |

---

### 5. pipeline_panel.py - Pipeline Paneli
**Sorumluluk:** Pipeline aşamalarını görselleştirme

**Görsel Tasarım:**
```
IF  [ADDI r1, r0, 15]  (Mavi)
ID  [ADD]              (Turuncu)
EX  [SUB]              (Mor)
MEM [LW]               (Yeşil)
WB  [NOP]              (Kırmızı)
```

---

### 6. memory_panel.py - Memory Paneli
**Sorumluluk:** Instruction ve Data memory gösterme

**İki Bölüm:**
1. **Instruction Memory**
   - Address
   - Binary kod
   - Assembly kod
   - Mevcut instruction vurgulanır

2. **Data Memory**
   - Address
   - Decimal değer
   - Hex değer
   - İlk 32 lokasyon gösterilir

---

## 🔄 Veri Akışı

### Program Yükleme
```
User Code (Editor)
    ↓
Assembler.assemble()
    ↓
Binary Instructions
    ↓
CPU.load_program()
    ↓
Instruction Memory
```

### Execution Cycle
```
MainWindow.step()
    ↓
CPU.step()
    ├→ Hazard Detection
    ├→ Pipeline Execution (IF→ID→EX→MEM→WB)
    ├→ Forwarding
    └→ Statistics Update
    ↓
MainWindow.update_display()
    ├→ StatsPanel.update()
    ├→ RegistersPanel.update()
    ├→ PipelinePanel.update()
    └→ MemoryPanel.update()
```

---

## 🎯 Tasarım Prensipleri

### 1. Separation of Concerns
- **Backend (core/):** CPU logic, no GUI dependencies
- **Frontend (gui/):** Display only, no CPU logic
- **Clean Interface:** CPU ve GUI bağımsız çalışabilir

### 2. Modularity
- Her component kendi dosyasında
- Her class tek sorumluluk
- Kolay test edilebilir

### 3. Extensibility
- Yeni instruction eklemek kolay (cpu.py'de bir method)
- Yeni GUI component eklemek kolay (gui/'de yeni panel)
- Backend değişikliği frontend'i etkilemez

---

## 🔌 Bağımlılıklar

### Backend Dependencies
```
core/
  - Python standard library only
  - No external packages
  - No GUI dependencies
```

### Frontend Dependencies
```
gui/
  - tkinter (Python standard)
  - core package (backend)
```

### Main Application
```
main.py
  - tkinter
  - core (backend)
  - gui (frontend)
```

---

## 🚀 Kullanım Senaryoları

### Senaryo 1: CLI Kullanımı (Backend Only)
```python
from core import PipelinedCPU, Assembler

cpu = PipelinedCPU()
asm = Assembler()

code = "ADDI r1, r0, 10\nNOP"
instructions = asm.assemble(code)
cpu.load_program(instructions)

while not cpu.is_program_complete():
    cpu.step()
    print(f"Cycle {cpu.cycle}: R1 = {cpu.registers[1]}")
```

### Senaryo 2: GUI Kullanımı
```python
python main.py
```

### Senaryo 3: Test Yazma
```python
import pytest
from core import PipelinedCPU, Assembler

def test_add_instruction():
    cpu = PipelinedCPU()
    asm = Assembler()
    
    code = """
    ADDI r1, r0, 5
    NOP
    NOP
    ADDI r2, r0, 3
    NOP
    NOP
    ADD r3, r1, r2
    NOP
    """
    
    cpu.load_program(asm.assemble(code))
    
    # Run until complete
    for _ in range(50):
        cpu.step()
        if cpu.is_program_complete():
            break
    
    assert cpu.registers[3] == 8
```

---

## 📝 Yeni Özellik Ekleme

### Backend'e Yeni Instruction Eklemek

1. **cpu.py'de OPCODES'a ekle:**
```python
self.OPCODES['MYNEW'] = 0b0101
```

2. **_execute_stage() metoduna logic ekle:**
```python
elif opcode == self.OPCODES['MYNEW']:
    alu_result = # hesaplama
    rd = self.ID_EX['rd']
    write_reg = True
```

3. **assembler.py'de encoding ekle:**
```python
elif op_name == 'MYNEW':
    # encoding logic
    return binary_string
```

### Frontend'e Yeni Panel Eklemek

1. **Yeni panel dosyası oluştur:**
```python
# gui/my_new_panel.py
class MyNewPanel(ttk.Frame):
    def __init__(self, parent, cpu):
        # implementation
```

2. **main_window.py'de kullan:**
```python
from .my_new_panel import MyNewPanel

# Layout'a ekle
self.new_panel = MyNewPanel(parent, self.cpu)
```

---

## 🎓 Eğitim Amaçlı Kullanım

### Öğrenme Hedefleri
1. ✅ Pipeline nasıl çalışır
2. ✅ Hazard'lar nasıl tespit edilir
3. ✅ Forwarding nasıl çalışır
4. ✅ Assembly → Machine code
5. ✅ CPU architecture

### Demo Senaryoları
1. **Load-Use Hazard:** LW + ADD sequence
2. **Branch Hazard:** BEQ instruction
3. **Data Forwarding:** ADD + ADD sequence
4. **Pipeline Efficiency:** CPI hesaplama

---

## 📞 Destek

Sorular için:
- README.md dosyasına bakın
- docs/ klasöründeki dökümanları inceleyin
- Kod içindeki docstring'leri okuyun

---

## ✅ Özet

**Backend (core/):**
- Bağımsız, test edilebilir
- CPU simülasyonu
- Assembly çevirimi

**Frontend (gui/):**
- Modüler componentler
- Responsive layout
- Real-time görselleştirme

**Birlikte:**
- Profesyonel mimari
- Kolay bakım
- Genişletilebilir

Başarılı projeler! 🚀
