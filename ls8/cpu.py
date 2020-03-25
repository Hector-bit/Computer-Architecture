"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        

    def load(self, filename):
        """Load a program into memory."""
        address = 0

        try:
            with open(filename) as f:
                for line in f:
                    #ignores comments
                    comment_split = line.split("#")
                    #cuts out whitespace
                    num = comment_split[0].strip()
                    #ignore blank lines
                    if num == '':
                        continue
                    val = int(num)
                    self.ram[address] = val
                    address += 1
        except FileNotFoundError:
            print('file not found')
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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

    def ram_write(self, address, new):
        self.ram[address] = new

    def run(self):
        """Run the CPU."""
        running = True

        LDI = 130
        PRINT_NUM = 71
        HALT = 1

        while running:
            instructions = self.ram[self.pc]
            print(instructions)
            print(type(instructions))
            if instructions == LDI:
                reg = self.ram_read(self.pc + 1)
                self.ram_write(self.pc, reg)
                self.pc += 3

            elif instructions == PRINT_NUM:
                reg = self.ram_read(self.pc + 1)
                print(self.ram_read(reg))
                self.pc += 2

            elif instructions == HALT:
                running = False
                sys.exit(0)

            else:
                print(f'Do not know what {instructions} is')
                sys.exit(1)

