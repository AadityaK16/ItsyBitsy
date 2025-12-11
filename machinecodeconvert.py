#python script for mapping machine code

# assembler.py
def reg_to_bin(reg):
    reg = reg.upper().strip()
    rnum = int(reg.replace("X", ""))
    return format(rnum, "02b")


def assemble_line(line):
    # Remove comments
    line = line.split("#")[0].split("//")[0].strip()
    if not line:
        return None

    parts = line.replace(",", " ").split()
    instr = parts[0].upper()

    opcodes = {
        "PLUS":  "01",
        "CROSS": "10",
        "LOAD":  "11",
        "STORE": "00"
    }

    opcode = opcodes[instr]

    if instr in ("PLUS", "CROSS"):
        Xi = reg_to_bin(parts[1])
        Xj = reg_to_bin(parts[2])
        Xk = reg_to_bin(parts[3])
    else:
        Xi = reg_to_bin(parts[1])
        Xj = reg_to_bin(parts[2])
        Xk = "00"

    return opcode + Xi + Xj + Xk



def assemble_file(input_file, output_file):
    with open(input_file, "r") as f:
        lines = f.readlines()

    hex_bytes = []

    for line in lines:
        binary = assemble_line(line)
        if binary:
            # convert to lowercase hex
            hex_bytes.append(format(int(binary, 2), "02x"))

    # Fill up to 256 bytes with "00"
    while len(hex_bytes) < 256:
        hex_bytes.append("00")

    with open(output_file, "w") as f:
        f.write("v3.0 hex words addressed\n")

        for addr in range(0, 256, 16):
            # lowercase address index
            row_addr = format(addr, "02x")
            chunk = hex_bytes[addr:addr + 16]
            chunk_str = " ".join(chunk)
            f.write(f"{row_addr}: {chunk_str}\n")

    print(f"Assembly complete. Output written to {output_file}")


# ----------- RUN EXAMPLE -----------
assemble_file("machineprogram.txt", "output_hex.txt")
