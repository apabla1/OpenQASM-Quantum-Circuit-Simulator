import sys
from lexer import lex
from parser import parser
from interp import interp

def simulate(str):
    tokens = lex(str)
    parse_tree = parser(tokens)
    
    # trim unused qubits
    if parse_tree["ops"]:
        max_qubit = max(max(op["qubits"]) for op in parse_tree["ops"])
        parse_tree["qreg_size"] = max_qubit + 1
    
    final_state = interp(parse_tree)
    
    ### convert from list of WeightedKets to state vector
    num_qubits = final_state[0].size
    dim = 2 ** num_qubits
    state_vector = [0j] * dim

    for wk in final_state:
        idx = int(wk.bitstring, 2)
        state_vector[idx] += wk.amplitude

    state_vector = [complex(round(a.real, 3), round(a.imag, 3)) for a in state_vector]
    return state_vector

def Simulator(str):
    return simulate(str)

if __name__ == "__main__":
    with open (sys.argv[1], 'r') as f:
        qasm_string = f.read()
    final_state = simulate(qasm_string)
    print(final_state)