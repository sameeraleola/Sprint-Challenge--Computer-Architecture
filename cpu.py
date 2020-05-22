"""
Day 2: Add the ability to load files dynamically, get mult.ls8 running
 x Un-hardcode the machine code
 x Implement the load() function to load an .ls8 file given the filename passed in as an argument
 Implement a Multiply instruction (run mult.ls8)
"""
import sys

class CPU:
    """Main CPU class."""

    """Construct a new CPU."""
    def __init__(self):
        # RAM
        self.ram = [0] * 256
        # CPU registers
        self.reg = [0] * 8
        # Program counter
        self.pc = 0
        # Instruction register
        self.ir = 0
        # Compare flag
        self.fl = 0
        # Memory data register
        # self.mdr = 0

       
        self.opcodes = {
        # Check the opcode for the following information:
        # 1. Bits 6-7: Number of operands for the opcode 0, 1, or 2
        # 2. Bit 5 ALU or CPU
        # 3. Bit 4 if the operand sets the PC or jumps
        # 4. Bits 0-2 the opcode identifier
            0b10000010: self.ldi,
            0b01000111: self.prn,
            0b00000001: self.hlt,

            # Jump opcodes
            0b01010100: self.jmp,
            0b01010101: self.jeq,
            0b01010110: self.jne,
            
            # ALU Opcodes
            0b10100000: self.add, # ALU add
            0b10100001: self.sub, # ALU subtract
            0b10100010: self.mul, # ALU multiple 4th bit defines set (0) for increment or jump (1)
            0b10100111: self.cmp # ALU compare
        }

    ### CPU opcodes ###
    # LDI: Load immediate = Load the data in mdr into the register specified in mar
    def ldi(self, mar, mdr):
        self.reg[mar] = mdr

    # PRN: print the value in the register specified in mar
    def prn(self, mar, mdr):
        print(self.reg[mar])
    
    # HLT: Exit the executing program
    def hlt(self, mar, mdr):
        exit(0)
    
    # Subroutine and functions opcodes
    #----------------------------------
    def jmp(self, mar, mdr):
        print(f'jmp mar = {bin(mar)}')
        self.pc = mar

    def jeq(self, mar, mdr):
        print(f'self.fl = {bin(self.fl)}')
        print(f'jeq mar = {bin(mar)}')
        if self.fl == 0b0000001:
            self.pc = self.reg[mar]
            

    def jne(self, mar, mdr):
        print(f'jne mar = {bin(mar)}')
        if self.fl == 0b00000010:
            self.pc = mar


    # ALU Opcode definitions
    #-----------------------
    # ADD: Add in ALU
    def add(self, mar, mdr):
        self.alu("ADD", mar, mdr)

    # SUB: Subtract in ALU
    def sub(self, mar, mdr):
        self.alu("SUB", mar, mdr)

    # MUL: Multiple in ALU
    def mul(self, mar, mdr):
        self.alu("MUL", mar, mdr)

    # CMP: Compare in ALU
    def cmp(self, mar, mdr):
        mar = self.reg[mar]
        mdr = self.reg[mdr]
        self.alu("CMP", mar, mdr)

    
    # Read the value stored in memory location adr
    def ram_read(self, mar):
        return self.ram[mar]

   # Write the value (mdr) the value stored in memory location adr
    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    def pcinc(self, opcode):
        # Get the PC increment
        opsize = int((opcode & 0b11000000) >> 6)
        self.pc += (opsize + 1)

    # def isalu(self, opcode):
    #     # Mask and shift for the ALU selection 
    #     ALUMASK = 0b00100000
    #     # if ((opcode & ALUMASK))
    #     print(f'aluflag = {(opcode & ALUMASK) >> 5}')
    #     print(f'Here is the ALU bit: {self.alubit}')       

    # Load program from an external file
    def load(self, programfile):
        """Load a program into memory."""
        address = 0

        # Open and parsee the program file
        with open(programfile) as program:
            for instruction in program:
                # print(f'instruction read = {instruction}')
                line_read = instruction.split("#")[0].strip()
                if line_read == '':
                    continue
                prog_step = int(line_read, 2)
                # print(prog_step)
                self.ram[address] = prog_step
                # print(f'ram[{address}] = {self.ram[address]}')
                address += 1

            # is_alu = (self.ir & 0b00100000) >> 5)
            # set_pc = (self.ir & 0b00010000) >> 4) 

    # Run the CPU
    def run(self):
        while True:
            # Initialize the program
            print(f'self.ram[self.pc] = {bin(self.ram[self.pc])}')
            self.ir = self.ram[self.pc]
            # Get the alu and PC set mask
            # is_alu = (self.ir & 0b00100000) >> 5
            set_pc = (self.ir & 0b00010000) >> 4
            # print(f'set_pc = {set_pc}')

            # Cache the first two values in memory
            op_a = self.ram[self.pc + 1]
            op_b = self.ram[self.pc + 2]

            # Execute the opcode in the opcode dict
            self.opcodes[self.ir](op_a, op_b)
            print(f'Back from opcode. PC = {bin(self.pc)}')
            # Increment or set the PC
            if set_pc == 0:
            # print(f'pc = {self.pc}')
                self.pcinc(self.ir)


    # Implement the ALU
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "CMP":
            if reg_a == reg_b:
                self.fl = 0b0000001
            else:
                self.fl = 0b00000010
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    # def run(self):
    #     """Run the CPU."""
    #     pass
