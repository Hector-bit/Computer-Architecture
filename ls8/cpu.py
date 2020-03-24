"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0
        self.reg = [0] * 8
        

    def load(self):
        """Load a program into memory."""
        address = 0

        # For now, we've just hardcoded a program:
        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

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
        # self.pc = 0
        # running = True

        # HALT = 1
        # PRINT = 47
        # while running:
        #     command = self.ram[self.pc]
        #     if command == HALT:
        #         running = False
        #         self.pc += 1
        #     elif command == PRINT:
        #         self.pc += 2
        #     else:
        #         print(f'Do not know what {command} is')
        #         sys.exit(1)
        #     self.pc += 1
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

