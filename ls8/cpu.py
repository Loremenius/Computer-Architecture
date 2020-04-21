"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.pc = 0
        self.ram = [0] * 256

    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) == 1:
            print('There is no file to run')
        else:
            program = []
            f = open(sys.argv[1], "r").read()
            f = f.split('\n')
            for line in f:
                if line == '':
                    line = ' '
                if line[0] == '1' or line[0] == '0':
                    if line.find('#') > 0:
                        new_line = line.split('#')
                        line = new_line[0]
                    new_line = line.rstrip()
                    line = int(new_line, base=2)
                    program.append(line)
            print(program)
            for instruction in program:
                self.ram_write(instruction, address)
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

    def run(self):
        """Run the CPU."""
        running = True
        IR = None
        while running:
            IR = self.ram[self.pc]

            if IR == 0b10000010: #LDI
                reg_num = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]
                self.reg[reg_num] = value
                self.pc += 3

            elif IR == 0b01000111: #PRN
                reg_num = self.ram[self.pc + 1]
                value = self.reg[reg_num]
                print(value)
                self.pc += 2
            
            elif IR == 0b00000001:
                break

            elif IR == 0b10100010:
                reg_num_1 = self.ram_read(self.pc + 1)
                reg_num_2 = self.ram_read(self.pc + 2)
                value_1 = self.reg[reg_num_1]
                value_2 = self.reg[reg_num_2]
                self.reg[reg_num_1] = value_1 * value_2
                self.pc += 3
            
            else:
                print('unknown instruction')
                break




    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value
