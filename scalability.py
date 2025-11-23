# miller_11.qasm -- 3 qubits
# decod24-v2_43.qasm -- 4 qubits
# one-two-three-v3_101.qasm -- 5 qubits
# hwb5_53.qasm -- 6 qubits
# alu-bdd_288.qasm -- 7 qubits
# f2_232.qasm -- 8 qubits
# con1_216.qasm -- 9 qubits
# mini_alu_305.qasm -- 10 qubits
# wim_266.qasm -- 11 qubits
# cm152a_212.qasm -- 12 qubits
# squar5_261.qasm -- 13 qubits
# sym6_316.qasm -- 14 qubits
# rd84_142.qasm -- 15 qubits
# cnt3-5_179.qasm -- 16 qubits

from simulator import Simulator
import time
import os

def sim_time(file_path):
    with open(file_path, 'r') as f:
        qasm_string = f.read()
    
    sim = Simulator()
    
    start_time = time.time()
    final_state = sim.simulate(qasm_string)
    end_time = time.time()
    execution_time = end_time - start_time

    return execution_time

if __name__ == "__main__":
    files = {
        3 : "./tests/miller_11.qasm",
        4 : "./tests/decod24-v2_43.qasm",
        5 : "./tests/one-two-three-v3_101.qasm",
        6 : "./tests/hwb5_53.qasm",
        7 : "./tests/alu-bdd_288.qasm",
        8 : "./tests/f2_232.qasm",
        9 : "./tests/con1_216.qasm",
        10 : "./tests/mini_alu_305.qasm",
        11 : "./tests/wim_266.qasm",
        12 : "./tests/cm152a_212.qasm",
        13 : "./tests/squar5_261.qasm",
        14 : "./tests/sym6_316.qasm",
        15 : "./tests/rd84_142.qasm",
        16 : "./tests/cnt3-5_179.qasm"
    }

    execution_times = {}
    for num_qubits, file_path in files.items():
        exec_time = sim_time(file_path)
        execution_times[num_qubits] = exec_time
        
    import matplotlib.pyplot as plt
    plt.plot(list(execution_times.keys()), list(execution_times.values()), marker='o')
    plt.xlabel('Number of Qubits')
    plt.ylabel('Execution Time (seconds)')
    plt.show()
        
        

