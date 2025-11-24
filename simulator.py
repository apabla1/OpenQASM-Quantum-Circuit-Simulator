import numpy as np
# from lexer import lex
# from parser import parse
# from interp import interp

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
        tokens = lex(qasm_str)
        parse_tree = parse(tokens)
        final_state = interp(parse_tree)
                
        ## Convert final_state (list of WeightedKet) to statevector (numpy array)
        state_vector = np.zeros(2**len(final_state[0].bitstring), dtype=complex)
        for wk in final_state:
            idx = int(wk.bitstring, 2)
            state_vector[idx] += complex(round(wk.amplitude.real, 3), round(wk.amplitude.imag, 3))

        return state_vector
    
############################### Functions pasted below (& modified) for the autograder ###############################

"""
Lexer -- modified for no regex 
(Added helper function to lex each instruction; virtually all the same. They all just use built-in python string functions instead.)
"""
def lex_qreg(line):
    if not line.startswith("qreg"):
        return None
    parts = line.split()
    if len(parts) != 2 or parts[0] != "qreg":
        return None
    arg = parts[1]
    if not (arg.startswith("q[") and arg.endswith("];")):
        return None
    size = arg[2:-2]
    return size if size.isdigit() else None
def lex_creg(line):
    if not line.startswith("creg"):
        return None
    parts = line.split()
    if len(parts) != 2 or parts[0] != "creg":
        return None
    arg = parts[1]
    if not (arg.startswith("c[") and arg.endswith("];")):
        return None
    size = arg[2:-2]
    return size if size.isdigit() else None
def lex_sq_gate(line):
    parts = line.split()
    if len(parts) != 2:
        return None
    gate = parts[0]
    if gate not in ("h", "x", "t", "tdg"):
        return None
    arg = parts[1]
    if not (arg.startswith("q[") and arg.endswith("];")):
        return None
    idx = arg[2:-2]
    if not idx.isdigit():
        return None
    return gate, idx
def lex_cx_gate(line):
    parts = line.split(None, 1) # "cx q[0], q[2];" -> ["cx", "q[0], q[2];"]
    if len(parts) != 2 or parts[0] != "cx":
        return None
    rest = parts[1]
    if not rest.endswith(";"):
        return None
    if len(rest) >= 2 and rest[-2].isspace():
        return None
    core = rest[:-1]
    if "," not in core:
        return None
    left, right = core.split(",", 1)
    left, right = left.strip(), right.strip()
    def lex_qubit(token):
        if not (token.startswith("q[") and token.endswith("]")):
            return None
        num = token[len("q["):-1]
        return num if num.isdigit() else None
    control = lex_qubit(left)
    target = lex_qubit(right)
    if control is None or target is None:
        return None
    return control, target

def lex(str):
    toks = []
    lines = str.split(';')
    for line in lines:
        line = line.strip()
        line = line + ';' if line != '' else line
        #print(f"line = {line} \n toks = {toks}")
        if line == "OPENQASM 2.0;":
            toks.append(('OPENQASM 2.0', None))
            continue
        elif line == 'include "qelib1.inc";':
            toks.append(('INCLUDE_QELIB1', None))
            continue
        elif line.startswith('//'):
            toks.append(('COMMENT', None))
            continue
        elif line == '':
            toks.append(('NEWLINE', None))
            continue
        m = lex_qreg(line)
        if m is not None:
            toks.append(('QREG', (m, None)))
            continue
        m = lex_creg(line)
        if m is not None:
            toks.append(('CREG', (m, None)))
            continue
        m = lex_sq_gate(line)
        if m is not None:
            gate, qubit_idx = m
            toks.append((gate.upper(), (qubit_idx, None)))
            continue
        m = lex_cx_gate(line)
        if m is not None:
            control_idx, target_idx = m
            toks.append(('CX', (control_idx, target_idx)))
            continue
        raise ValueError(f"Unknown instruction: {line}")
    return toks

"""
Parser
"""
def parse(toks):
    parse_tree = {
        "qreg_size": None,
        "num_used_qubits": None,
        "creg_size": None,
        "ops": [],
    }
    max_qubit_used = -1 # to purge unused qubits
    for type, value in toks:
        if type in ['COMMENT', 'NEWLINE', 'OPENQASM 2.0', 'INCLUDE_QELIB1']:
            continue
        elif type == 'CREG':
            reg_idx, _ = value
            parse_tree["creg_size"] = int(reg_idx)
            parse_tree["num_used_qubits"] = int(reg_idx)
        elif type == 'QREG':
            reg_idx, _ = value
            parse_tree["qreg_size"] = int(reg_idx)
        elif type in ['H', 'X', 'T', 'TDG']:
            qubit_idx, _ = value
            q = int(qubit_idx)
            parse_tree["ops"].append({
                "gate": type,          
                "qubits": [q], 
            })
            if q > max_qubit_used:
                max_qubit_used = q
        elif type == 'CX':
            control_idx, target_idx = value
            c = int(control_idx)
            t = int(target_idx)
            parse_tree["ops"].append({
                "gate": "CX",
                "qubits": [c, t],  # [control, target]
            })
            if c > max_qubit_used or t > max_qubit_used:
                max_qubit_used = max(c, t)
        else:
            raise ValueError(f"Unknown token type: {type}")
    # purge unused qubits
    if max_qubit_used >= 0:
        parse_tree["num_used_qubits"] = max_qubit_used + 1

    return parse_tree

"""
Interpreter
"""
"""
Note that states are represented using the state-vector model, as opposed to the matrix model. 
We use OOP for weighted kets, and then a quantum state is simply an array of weighted kets. Note that the kets are little-endian.
"""
"""
NOTE: This interpreter DOES convert back to full qreg_size by padding with zeros.
"""
class WeightedKet:
    size: int    # number of qubits
    bitstring: str      # e.g. LITTLE-endian; bitstring[i] is qubit i 
    amplitude: complex   # amplitude 
    
    def __init__(self, size, bitstring, amplitude):
        self.size = size
        self.bitstring = bitstring
        self.amplitude = amplitude
        
    def __repr__(self):
        return f"({round(self.amplitude.real,3):+g}{round(self.amplitude.imag,3):+g}j)|{self.bitstring}>"

def interp(parse_tree):
    
    # init state to |00...00>
    state = []
    n = parse_tree["num_used_qubits"]
    for i in range(2 ** n):
        bitstring = format(i, f'0{n}b')[::-1]
        state.append(WeightedKet(n, bitstring, 0.0 + 0.0j)) # every ampltiude is 0
    state[0].amplitude = 1.0 + 0.0j  # except for 00.00
    
    for op in parse_tree["ops"]:
        gate = op["gate"]
        qs = op["qubits"]
        if gate == "X":
            apply_x(state, qs[0])
        elif gate == "H":
            apply_h(state, qs[0])
        elif gate == "T":
            apply_t(state, qs[0])
        elif gate == "TDG":
            apply_tdg(state, qs[0])
        elif gate == "CX":
            apply_cx(state, qs[0], qs[1])
        sort(state)
        aggregate(state)
        
    # convert back to full qreg_size by padding with zeros
    full_state = []
    full_n = parse_tree["qreg_size"]
    for wk in state:
        padded_bitstring = wk.bitstring + '0' * (full_n - n)
        full_state.append(WeightedKet(full_n, padded_bitstring, wk.amplitude))
            
    return state

def apply_x(state, qubit_idx):
    for wk in state:
        bitlist = list(wk.bitstring)
        bitlist[qubit_idx] = '1' if bitlist[qubit_idx] == '0' else '0'
        wk.bitstring = ''.join(bitlist)
    
def apply_h(state, qubit_idx):
    new_state = []
    for wk in state:
        amp = wk.amplitude
        bits = list(wk.bitstring)

        # H|0> = (|0> + |1>)/sqrt2
        if bits[qubit_idx] == '0': 
            # |same thing>/\sqrt2
            new_state.append(WeightedKet(wk.size, wk.bitstring, wk.amplitude * (1 / 2**0.5)))
            
            # |same thing with qubit_idx flipped>/\sqrt2
            bits1 = bits[:]
            bits1[qubit_idx] = '1'
            new_state.append(WeightedKet(wk.size, ''.join(bits1), wk.amplitude * (1 / 2**0.5)))
            
        # H|1> = (|0> - |1>)/sqrt2
        else:
            # |same thing with qubit_idx flipped>/\sqrt2
            bits0 = bits[:]
            bits0[qubit_idx] = '0'
            new_state.append(WeightedKet(wk.size, ''.join(bits0), wk.amplitude * (1 / 2**0.5)))

            # |same thing with minus sign>/\sqrt2
            new_state.append(WeightedKet(wk.size, wk.bitstring, -amp * (1 / 2**0.5)))

    state[:] = new_state
    
def apply_t(state, qubit_idx):
    for wk in state:
        if wk.bitstring[qubit_idx] == '1':
            wk.amplitude *= (1 + 1j)/(2**0.5) # (1+i)/sqrt(2) phase
    
def apply_tdg(state, qubit_idx):
    for wk in state:
        if wk.bitstring[qubit_idx] == '1':
            wk.amplitude *= (1 - 1j)/(2**0.5) # (1-i)/sqrt(2) phase
    
def apply_cx(state, control_idx, target_idx):
    new_state = []
    for wk in state:
        bits = list(wk.bitstring)
        if bits[control_idx] == '1':
            bits[target_idx] = '1' if bits[target_idx] == '0' else '0'
        new_state.append(WeightedKet(wk.size, ''.join(bits), wk.amplitude))
    state[:] = new_state

def sort(state):
    state.sort(key=lambda wk: wk.bitstring)

def aggregate(state):
    aggregated = []
    current = state[0]
    for wk in state[1:]:
        if wk.bitstring == current.bitstring:
            current.amplitude += wk.amplitude
        else:
            aggregated.append(current)
            current = wk
    aggregated.append(current)
    state[:] = aggregated

if __name__ == "__main__":
    import sys
    with open (sys.argv[1], 'r') as f:
        qasm_string = f.read()
    tokens = lex(qasm_string)
    parse_tree = parse(tokens)
    bk_state = interp(parse_tree)
    vec_state = Simulator().simulate(qasm_str=qasm_string)
    print(f"State Vector (little-endian): \n{vec_state}")
    print(f"Bra-Ket (little-endian): \n{bk_state}")