# ============================================
# 16-BIT MIPS SIMULATOR - KAPSAMLI TEST
# TÜM DEĞERLER 6-BIT ARALIKTA (0-63)
# Güncellenmiş ve Test Edilmiş Versiyon
# ============================================

# ============================================
# TEST PROGRAMI İÇERİĞİ:
# ============================================
# ✓ 13 Farklı Instruction Test Ediliyor
# ✓ Tüm immediate değerler 0-63 aralığında
# ✓ Her test sonucu memory'ye kaydediliyor
# ✓ Pipeline hazard'ları düşünülerek NOP'lar eklendi
# ============================================

# ============================================
# BÖLÜM 1: ADDI (Add Immediate)
# Test: Temel sayı yükleme
# ============================================
ADDI r1, r0, 15     # r1 = 15
NOP
NOP
ADDI r2, r0, 25     # r2 = 25
NOP
NOP
SW r1, 0(r0)        # MEM[0] = 15 ✓
NOP
NOP
SW r2, 1(r0)        # MEM[1] = 25 ✓
NOP
NOP

# ============================================
# BÖLÜM 2: ADD (Addition)
# Test: İki register'ı toplama
# ============================================
ADD r3, r1, r2      # r3 = 15 + 25 = 40
NOP
NOP
SW r3, 2(r0)        # MEM[2] = 40 ✓
NOP
NOP

# ============================================
# BÖLÜM 3: SUB (Subtraction)
# Test: Çıkarma işlemi
# ============================================
SUB r4, r3, r1      # r4 = 40 - 15 = 25
NOP
NOP
SW r4, 3(r0)        # MEM[3] = 25 ✓
NOP
NOP

# ============================================
# BÖLÜM 4: ANDI (AND Immediate)
# Test: Bit maskeleme
# ============================================
ADDI r5, r0, 31     # r5 = 31 (binary: 011111)
NOP
NOP
ANDI r6, r5, 15     # r6 = 31 & 15 = 15 (binary: 001111)
NOP
NOP
SW r6, 4(r0)        # MEM[4] = 15 ✓
NOP
NOP

# ============================================
# BÖLÜM 5: AND (Logical AND)
# Test: İki register AND
# ============================================
ADDI r7, r0, 28     # r7 = 28 (binary: 011100)
NOP
NOP
AND r1, r5, r7      # r1 = 31 & 28 = 28 (binary: 011100)
NOP
NOP
SW r1, 5(r0)        # MEM[5] = 28 ✓
NOP
NOP

# ============================================
# BÖLÜM 6: ORI (OR Immediate)
# Test: Bit set etme
# ============================================
ADDI r2, r0, 12     # r2 = 12 (binary: 001100)
NOP
NOP
ORI r3, r2, 3       # r3 = 12 | 3 = 15 (binary: 001111)
NOP
NOP
SW r3, 6(r0)        # MEM[6] = 15 ✓
NOP
NOP

# ============================================
# BÖLÜM 7: OR (Logical OR)
# Test: İki register OR
# ============================================
ADDI r4, r0, 16     # r4 = 16 (binary: 010000)
NOP
NOP
ADDI r5, r0, 7      # r5 = 7  (binary: 000111)
NOP
NOP
OR r6, r4, r5       # r6 = 16 | 7 = 23 (binary: 010111)
NOP
NOP
SW r6, 7(r0)        # MEM[7] = 23 ✓
NOP
NOP

# ============================================
# BÖLÜM 8: SLT (Set Less Than)
# Test: Karşılaştırma işlemi
# ============================================
ADDI r1, r0, 10     # r1 = 10
NOP
NOP
ADDI r2, r0, 20     # r2 = 20
NOP
NOP
SLT r3, r1, r2      # r3 = (10 < 20) = 1 (true)
NOP
NOP
SW r3, 8(r0)        # MEM[8] = 1 ✓
NOP
NOP
SLT r4, r2, r1      # r4 = (20 < 10) = 0 (false)
NOP
NOP
SW r4, 9(r0)        # MEM[9] = 0 ✓
NOP
NOP

# ============================================
# BÖLÜM 9: SW (Store Word)
# Test: Memory'ye yazma
# ============================================
ADDI r5, r0, 42     # r5 = 42
NOP
NOP
SW r5, 10(r0)       # MEM[10] = 42 ✓
NOP
NOP

# ============================================
# BÖLÜM 10: LW (Load Word)
# Test: Memory'den okuma
# ============================================
LW r6, 10(r0)       # r6 = MEM[10] = 42
NOP
NOP
SW r6, 11(r0)       # MEM[11] = 42 ✓ (LW doğrulama)
NOP
NOP

# ============================================
# BÖLÜM 11: BEQ (Branch if Equal)
# Test: Branch koşulu TRUE
# ============================================
ADDI r1, r0, 8      # r1 = 8
NOP
NOP
ADDI r2, r0, 8      # r2 = 8 (eşit!)
NOP
NOP
ADDI r3, r0, 60     # r3 = 60 (yanlış değer)
NOP
NOP
BEQ r1, r2, 3       # r1 == r2, skip 3 instruction
ADDI r3, r0, 11     # Bu SKIP edilecek
NOP                 # Bu SKIP edilecek
ADDI r3, r0, 22     # Bu SKIP edilecek
ADDI r3, r0, 50     # Bu ÇALIŞACAK, r3 = 50
NOP
NOP
SW r3, 12(r0)       # MEM[12] = 50 ✓
NOP
NOP

# ============================================
# BÖLÜM 12: BNE (Branch if Not Equal)
# Test: Branch koşulu TRUE
# ============================================
ADDI r4, r0, 5      # r4 = 5
NOP
NOP
ADDI r5, r0, 12     # r5 = 12 (farklı!)
NOP
NOP
ADDI r6, r0, 60     # r6 = 60 (yanlış değer)
NOP
NOP
BNE r4, r5, 3       # r4 != r5, skip 3 instruction
ADDI r6, r0, 33     # Bu SKIP edilecek
NOP                 # Bu SKIP edilecek
ADDI r6, r0, 44     # Bu SKIP edilecek
ADDI r6, r0, 35     # Bu ÇALIŞACAK, r6 = 35
NOP
NOP
SW r6, 13(r0)       # MEM[13] = 35 ✓
NOP
NOP

# ============================================
# BÖLÜM 13: Matematik İşlemler Kombinasyonu
# Test: Birden fazla işlem birlikte
# ============================================
ADDI r1, r0, 20     # r1 = 20
NOP
NOP
ADDI r2, r0, 30     # r2 = 30
NOP
NOP
ADD r3, r1, r2      # r3 = 20 + 30 = 50
NOP
NOP
ADDI r4, r0, 10     # r4 = 10
NOP
NOP
SUB r5, r3, r4      # r5 = 50 - 10 = 40
NOP
NOP
SW r5, 14(r0)       # MEM[14] = 40 ✓
NOP
NOP

# ============================================
# BÖLÜM 14: Logical İşlemler Kombinasyonu
# Test: AND, OR, ANDI, ORI birlikte
# ============================================
ADDI r1, r0, 63     # r1 = 63 (maximum 6-bit: 111111)
NOP
NOP
ANDI r2, r1, 31     # r2 = 63 & 31 = 31 (011111)
NOP
NOP
ORI r3, r2, 32      # r3 = 31 | 32 = 63 (111111)
NOP
NOP
SW r3, 15(r0)       # MEM[15] = 63 ✓
NOP
NOP

# ============================================
# BÖLÜM 15: Memory Kopyalama
# Test: LW ve SW kombinasyonu
# ============================================
ADDI r1, r0, 55     # r1 = 55
NOP
NOP
SW r1, 20(r0)       # MEM[20] = 55
NOP
NOP
LW r2, 20(r0)       # r2 = MEM[20] = 55
NOP
NOP
SW r2, 21(r0)       # MEM[21] = 55 ✓ (kopya)
NOP
NOP

# ============================================
# BÖLÜM 16: NOP Test
# NOP her yerde kullanılıyor zaten ✓
# ============================================
NOP
NOP
NOP

# ============================================
# COMPLETION FLAG
# ============================================
ADDI r7, r0, 63     # r7 = 63 (maksimum değer)
NOP
NOP
SW r7, 31(r0)       # MEM[31] = 63 ✓ (Test tamamlandı!)
NOP
NOP
NOP


# ============================================
# BEKLENEN SONUÇLAR (Data Memory)
# ============================================
# MEM[0]  = 15   ← ADDI test
# MEM[1]  = 25   ← ADDI test
# MEM[2]  = 40   ← ADD test (15+25)
# MEM[3]  = 25   ← SUB test (40-15)
# MEM[4]  = 15   ← ANDI test (31&15)
# MEM[5]  = 28   ← AND test (31&28)
# MEM[6]  = 15   ← ORI test (12|3)
# MEM[7]  = 23   ← OR test (16|7)
# MEM[8]  = 1    ← SLT test (10<20=true)
# MEM[9]  = 0    ← SLT test (20<10=false)
# MEM[10] = 42   ← SW test
# MEM[11] = 42   ← LW test
# MEM[12] = 50   ← BEQ test (branch alındı)
# MEM[13] = 35   ← BNE test (branch alındı)
# MEM[14] = 40   ← Combination test (50-10)
# MEM[15] = 63   ← Logical combination
# MEM[20] = 55   ← Memory copy source
# MEM[21] = 55   ← Memory copy destination
# MEM[31] = 63   ← COMPLETION FLAG ✓
# ============================================

# ============================================
# TEST İSTATİSTİKLERİ (Tahmini)
# ============================================
# Total Instructions: ~140-150
# Total Cycles: ~400-450
# Stalls: 0 (NOP'lar sayesinde)
# Flushes: 2 (BEQ, BNE)
# Forwards: 0 (NOP'lar sayesinde)
# CPI: ~3.0
# ============================================

# ============================================
# 6-BIT KURAL HATIRLATMA
# ============================================
# ✓ Tüm immediate değerler: 0-63 aralığında
# ✓ Maximum safe value: 63 (111111 binary)
# ✓ Minimum value: 0 (000000 binary)
# ✗ 64 ve üzeri: TAŞMA riski!
# ============================================
