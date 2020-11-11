# File to translate intermediate code to arm

def to_arm(inter):
    inter = inter.split("\n")
    print("////////Intermediate code///////////")
    line = ".section .text\n .global start\n"
    for line in inter:
        print(line)

