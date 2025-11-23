import numpy as np
from lexer import lex
from parser import parser
from interp import interp0

def fidelity(statevector1, statevector2):
    """Compute the fidelity between two statevectors."""
    return np.abs(np.vdot(statevector1, statevector2))**2

class Simulator:
    def __init__(self):
        pass

    def simulate(self, qasm_str: str):
        """
            Simulate the circuit implemented by the input qasm string qasm_str. 
            Return the statevector in numpy array format of that qasm str.
            Please use Little endian encoding.
        """
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
        pass

if __name__ == "__main__":
    import sys
    with open (sys.argv[1], 'r') as f:
        qasm_string = f.read()
    tokens = lex(qasm_string)
    parse_tree = parser(tokens)
    bk_state = interp(parse_tree)
    vec_state = simulate(qasm_string)
    print(f"Trimmed Vector State: \n{vec_state}")
    print(f"Untrimmed Bra-Ket State: \n{bk_state}")