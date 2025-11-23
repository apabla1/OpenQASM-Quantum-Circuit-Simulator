import sys
import numpy as np
import cirq
from cirq.contrib.qasm_import import circuit_from_qasm
from pathlib import Path

# Import your simulate function here.
# cs238 can be a file, a folder with an __init__.py file,
from lexer import lex
from parser import parse
from interp import interp
from simulator import Simulator


def cirq_simulate(qasm_string: str) -> list:
    """Simulate a qasm string

    Args:
        qasm_string: a string following the qasm format

    Returns:
        statevector: a list, with a complex number for
            each of the 2^num_qubits possible amplitudes
            Ordered big endian, see:
        quantumai.google/reference/python/cirq/sim/StateVectorTrialResult#state_vector
    """

    circuit = circuit_from_qasm(qasm_string)
    result = cirq.Simulator().simulate(circuit)
    statevector = list(np.around(result.state_vector(), 3))
    return statevector


def compare(state_vector, cirq_state_vector):
    """Our comparison function for your grade

    Args:
        state_vector: your state vector amplitude list
        cirq_state_vector: cirq's state vector amplitude list

    Returns:
        Some value influencing your grade, subject to change :)
    """

    return np.all(np.isclose(state_vector, cirq_state_vector))


# get the directory of qasm files and make sure it's a directory
qasm_dir = Path(sys.argv[1])
assert qasm_dir.is_dir()

# iterate the qasm files in the directory
for qasm_file in qasm_dir.glob("**/*.qasm"):
    # read the qasm file
    with open(qasm_file, "r") as f:
        qasm_string = f.read()

    print(f"Testing YOUR simulation of {qasm_file}")
    # run your simulate function on the qasm string - returns BIG-endian!
    tokens = lex(qasm_string)
    parse_tree = parse(tokens)
    
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
        idx = int(wk.bitstring, 2) # BIG-endian
        state_vector[idx] += wk.amplitude

    state_vector = np.array([complex(round(a.real, 3), round(a.imag, 3)) for a in state_vector], dtype=complex)
    print(f"Testing CIRC simulation of {qasm_file}")
    
    
    
    # run cirq's simulator on the qasm string
    cirq_state_vector = cirq_simulate(qasm_string)
    
    
    # compare the results!
    print(compare(state_vector, cirq_state_vector))
