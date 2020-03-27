"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.fl_L = None
        self.fl_G = None
        self.fl_E = None
        

    def load(self, filename):
        """Load a program into memory."""
        address = 0

        try:
            with open(filename) as f:
                for line in f:
                    #ignore comments
                    comment_split = line.split("#")
                    #Strip whitespace
                    num = comment_split[0].strip()
                    #Ignore blank lines
                    if num =='':
                        continue 
                        
                    # val = eval(f"0b{num}")
                    val = int(num, 2) #base 2
                    self.ram_write(address, val)
                    print(f"RAM --> val: {val}, address: {address}")
                    address +=1
        except FileNotFoundError:
            print(f" {sys.argv[0]}: {filename} not found")
            sys.exit(2)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def run(self):
        """Run the CPU."""
        running = True

        LDI = 0b10000010
        PRINT_NUM = 0b01000111
        HALT = 0b00000001
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001

        SP = 7

        CMP = 0B10100111
        JMP = 0b01010100
        JNE = 0b01010110
        JEQ = 0b01010101

        while running:
            instructions = self.ram[self.pc]
            # print(instructions)
            # print(type(instructions))
            print(self.ram)
            print(self.reg)
            # print
            print('-------------')
            if instructions == HALT:
                running = False
                sys.exit(0)
                self.pc += 1

            elif instructions == LDI:
                reg = self.ram_read(self.pc + 1)
                num = self.ram_read(self.pc + 2)
                self.reg[reg] = num
                print(num, f'<-- number at index {reg} was printed')
                self.pc += 3

            elif instructions == PRINT_NUM:
                reg = self.ram_read(self.pc + 1)
                print(self.ram_read(reg))
                self.pc += 2

            elif instructions == MUL:
                reg_a = self.ram_read(self.pc + 1)
                reg_b = self.ram_read(self.pc + 2)
                self.alu("MUL", reg_a, reg_b)
                self.pc += 3

            elif instructions == PUSH:
                reg = self.ram[self.pc + 1]
                val = self.reg[reg]
                self.reg[SP] -= 1
                #copy the value in the given register to the address pointed to by SP
                self.ram[self.reg[SP]] =  val
                self.pc += 2

            elif instructions == POP:
                reg = self.ram[self.pc + 1]
                val = self.ram[self.reg[SP]]
                #copy the value from the address pointed to be the SP
                self.reg[reg] = val
                self.reg[SP] += 1
                self.pc += 2

            elif instructions == CALL:
                self.reg[SP] -= 1
                self.ram[self.reg[SP]] = self.pc + 2
                reg = self.ram[self.pc + 1]
                self.pc = self.reg[reg]

            elif instructions == RET:
                #return from subroutine
                #POP the value from the top of the stack and store it in the PC
                self.pc = self.ram[self.ram[SP]]
                self.reg[SP] += 1

            # - - - Sprint Challenge operations - - - - - - - - - -

            elif instructions == CMP:
                reg_a = self.ram_read(self.pc + 1)
                reg_b = self.ram_read(self.pc + 2)
                A = self.reg[0]
                B = self.reg[1]
                if A == B:
                    print('register A and B were equal')
                    self.fl_E = 1
                elif A > B:
                    print('register A is greater than B')
                    self.fl_G = 1
                elif A < B: 
                    print('register A is less than B')
                    self.fl_L = 1
                self.pc += 3

            elif instructions == JEQ:
                if self.fl_E == 1:
                    self.pc = self.reg[2]
                else:
                    self.pc += 2

            elif instructions == JNE:
                if self.fl_E == 0:
                    self.pc = self.reg[2]
                else:
                    self.pc += 2

            elif instructions == JMP:
                self.pc = self.reg[2]

            else:
                print(f'Do not know what {instructions} is')
                sys.exit(1)
