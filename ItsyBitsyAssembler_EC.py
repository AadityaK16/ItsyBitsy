#Name: Aaditya Kulkarni and Samdarshi Kumar Rai
#Pledge: I pledge my honor that I have abided by the Stevens Honor System.
#Description: This program is an assembler that converts a simple assembly language into
#             machine code in Logisim Evolution RAM format.

# Converts register name to 2-bit binary (X0–X3)
def reg_to_bin(reg):
    reg = reg.upper().strip()  # Normalizing case and whitespace

    if not reg.startswith("X"):  # Register syntax check
        raise ValueError(f"Invalid register format: {reg}")

    try:
        rnum = int(reg[1:])
    except ValueError:
        raise ValueError(f"Register must be X0–X3, got '{reg}'")  # Error handling for non-integer

    if not (0 <= rnum <= 3):
        raise ValueError(f"Register out of range: {reg} (allowed: X0–X3)") # Error handling for out of range

    return format(rnum, "02b")  # 2-bit binary


# Assembles one line of code into 8-bit binary
def assemble_line(line):
    # Removing comments
    line = line.split("#")[0].split("//")[0].strip()

    if not line:  # Skipping empty lines
        return None

    # Normalizing spacing
    parts = line.replace(",", " ").split()
    instr = parts[0].upper()

    # Opcodes (2 bits)
    opcodes = { "PLUS":  "01", "CROSS": "10", "LOAD":  "11", "STORE": "00"}

    if instr not in opcodes: # Unknown instruction error
        raise ValueError(f"Unknown instruction: {instr}")

    # All instructions require Xi, Xj, Xk
    if len(parts) != 4:
        raise ValueError(f"Instruction '{instr}' requires format: {instr} Xi Xj Xk")

    opcode = opcodes[instr]
    Xi = reg_to_bin(parts[1])
    Xj = reg_to_bin(parts[2])
    Xk = reg_to_bin(parts[3])

    return opcode + Xi + Xj + Xk  # Returns 8-bit instruction = opcode(2) + Xi(2) + Xj(2) + Xk(2)


# Writes a 256-byte Logisim imagefile
def write_logisim_file(output_file, hex_bytes):
    # Padding to complete 256 bytes
    while len(hex_bytes) < 256:
        hex_bytes.append("00")
    #Writing to output file
    with open(output_file, "w") as f:
        f.write("v3.0 hex words addressed\n")
        for addr in range(0, 256, 16):
            row_addr = format(addr, "02x")
            row_data = " ".join(hex_bytes[addr:addr+16])
            f.write(f"{row_addr}: {row_data}\n")

    print(f"Assembly complete. Output written to {output_file}")


# Assembles an entire file with .text and .data sections
def assemble_file(input_file, text_out="text_output.hex", data_out="data_output.hex"):
    mode = None
    text_bytes = []
    data_bytes = []

    with open(input_file, "r") as f:
        for raw in f:
            line = raw.strip()

            # Detecting directives
            if line.lower() == ".text":
                mode = "text"
                continue
            if line.lower() == ".data":
                mode = "data"
                continue

            # Skipping blanks or comment-only lines
            if not line or line.startswith("#"):
                continue

            # Writing to text output file
            if mode == "text":
                binary = assemble_line(line)
                if binary:
                    text_bytes.append(format(int(binary, 2), "02x"))
                continue

            # Writing to data output file
            if mode == "data":
                try:
                    num = int(line)
                except ValueError: #Error handling for non-integer
                    raise ValueError(f"Invalid number in .data section: '{line}'")

                if not (0 <= num <= 255): #Error handling for out of range
                    raise ValueError(f"Data value must be 0–255, got {num}")

                data_bytes.append(format(num, "02x"))
                continue

            # If no directive found yet
            raise ValueError("Input file must begin with .text or .data")

    # Writing output files
    write_logisim_file(text_out, text_bytes)
    write_logisim_file(data_out, data_bytes)


#USERS ZONE

#PROGRAMS! ASSEMBLE!!
assemble_file("Sample_program.txt") #The first argument is the name of your program file,
                                    #the second is the text output file (default "text_output.hex"), the third is the data output file (default "data_output.hex")

