# Simulator For A Subset Of OpenQASM (Open Quantum Assembly Language)
> **To run:** `python3 simulator.py <filename>`

Will print out the final state in (1) state vector form, and (2) bra-ket form. Also note that little-endian is used.

### How it works
1. The file contents will be converted to a string.
2. The string will be passed to the lexer (`lexer.py`), which will delimit lines by semicolons and convert the string to a list of tokens using regular expressions.
3. The token list is then passed to the parser (`parser.py`), which converts the token list to a program representation with (i) the number of qubits (where unused qubits are optimized), (ii) the number of classical bits, and (iii) the ordered-operation list by using the following grammar:

$$
\begin{aligned}
\text{P}\ \rightarrow &\ \textsf{OPENQASM 2.0;} \\
&\ \textsf{include "qelib1.inc";} \\
&\ \textsf{qreg q[n];} \qquad n \in \mathbb{Z} \\
&\ \textsf{creg c[n];} \qquad n \in \mathbb{Z} \\
&\ \text{S*}
\end{aligned}
$$

$$
\begin{aligned}
\text{S}\ &\rightarrow \textsf{h q[i];} \qquad 0 \leq i \leq n,\, i \in \mathbb{Z} \\
&\mid\ \ \textsf{x q[i];} \qquad 0 \leq i \leq n,\, i \in \mathbb{Z} \\
&\mid\ \ \textsf{t q[i];} \qquad 0 \leq i \leq n,\, i \in \mathbb{Z} \\
&\mid\ \ \textsf{tdg q[i];} \qquad 0 \leq i \leq n,\, i \in \mathbb{Z} \\
&\mid\ \ \textsf{cx q[i], q[j];} \qquad 0 \leq i, j \leq n,\, i, j \in \mathbb{Z} \\
&\mid\ \ \textsf{// }\epsilon^* \\
&\mid\ \ \textsf{\s} \quad \text{(whitespace)}
\end{aligned}
$$

4. This representation is then passed to the interpreter (`interp.py`). Using a weighted-ket class to represent singular (little-endian) kets with specific amplitudes and states as lists of weighted kets, the interpreter then starts in the all-0 state and applies gates in the operation list according to the following semantics:

$$X\ket{0} = \ket{1}, \quad X\ket{1} = \ket{0}$$
$$H\ket{0} = \dfrac{1}{\sqrt 2}\big(\ket{0} + \ket{1}\big), \quad H\ket{1} = \dfrac{1}{\sqrt 2}\big(\ket{0} - \ket{1} \big)$$
$$T\ket{0} = \ket{0}, \quad T\ket{1} = \dfrac{1+i}{\sqrt 2}\ket{1}$$
$$T^\dagger \ket{0} = \ket{0}, \quad T^\dagger \ket{1} = \dfrac{1-i}{\sqrt 2}\ket{1}$$
$$\text{(File headers, comments, and whitespace do nothing.)}$$

5. The final state is then reported. The simulator converts the state from a list of weighted to to a trimmed, vector (numpy array) form.

### Testing
* Running `python3 compare_simulators.py ./tests` will test the simulator against [Cirq](https://quantumai.google/cirq)'s simulator on the following 14 programs in the `/tests/` directory:

| Circuit                | Qubits | Lines |
|------------------------|-------:|------:|
| miller_11.qasm         |      3 |    54 |
| decod24-v2_43.qasm     |      4 |    56 |
| one-two-three-v3_101.qasm |   5 |    74 |
| hwb5_53.qasm           |      6 |  1340 |
| alu-bdd_288.qasm       |      7 |    88 |
| f2_232.qasm            |      8 |  1210 |
| con1_216.qasm          |      9 |   958 |
| mini_alu_305.qasm      |     10 |   177 |
| wim_266.qasm           |     11 |   990 |
| cm152a_212.qasm        |     12 |  1225 |
| squar5_261.qasm        |     13 |  1997 |
| sym6_316.qasm          |     14 |   274 |
| rd84_142.qasm          |     15 |   347 |
| cnt3-5_179.qasm        |     16 |   179 |

* Running `python3 scalability.py` will generate a graph mapping the number of qubits to the total simulator execution time for the same 14 test programs. 
* Additionally, the `/example_files/` directory contains simple 2-qubit implementations of the Deutsch-Jozsa algorithm in both the constant and balanced function cases. There is also a program that just  applies an $X$ gate, for simple testing.
