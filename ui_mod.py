import os

# Terminal Colors
C_CYAN = "\033[96m"
C_GREEN = "\033[92m"
C_BLUE = "\033[94m"
C_END = "\033[0m"

def clear():
    os.system('clear')

def header(fname):
    print(f"{C_CYAN}✧ H-ENGINE v3.0 // MODULAR_CORE ✧{C_END}")
    print(f"{C_BLUE}TARGET: {fname}{C_END}")
    print(f"{C_GREEN}COMMANDS: 'SAVE' (Store Data) | 'EXIT' (Return to HAXX){C_END}")
    print("-" * 45)

def get_input(num):
    return input(f"{C_BLUE}[{num}] » {C_END}")

def msg(text):
    print(f"{C_GREEN}>>> {text}{C_END}")

