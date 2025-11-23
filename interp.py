"""
Note that states are represented using the state-vector model, as opposed to the matrix model. 
We use OOP for weighted kets, and then a quantum state is simply an array of weighted kets. Note that the kets are little-endian.
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
        return f"({self.amplitude:+.4g})|{self.bitstring}>"

def interp(parse_tree):
    
    # init state to |00...00>
    state = []
    n = parse_tree["qreg_size"]
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
    from lexer import lex
    from parser import parse
    tokens = lex(sys.argv[1])
    parse_tree = parse(tokens)
    final_state = interp(parse_tree)
    nonzero_states = [wk for wk in final_state if abs(wk.amplitude) > 1e-10]
    import pprint
    pprint.pprint(nonzero_states)