# Simulator for a subset of OpenQASM
* To run: `python3 simulator.py <filename>`
* Will print out the final state in (1) trimmed vector form, and (2) un-trimmed bra-ket form. By 'trim' we mean get rid of any qubits that were not used in any computation.

### How it works
1. The file contents will be converted to a string.
2. The string will be passed to the lexer (`lexer.py`), which will delimit lines by semicolons and convert the string to a list of tokens using regular expressions.
3. The token list is then passed to the parser (`parser.py`), which converts the token list to a program representation with (i) the number of qubits, (ii) the number of classical bits, and (iii) the ordered-operation list by using the following grammar:

$$
\begin{aligned}
\text{P}\ \rightarrow &\ \textsf{OPENQASM 2.0;} \\
&\ \textsf{include "qelib1.inc";} \\
&\ \textsf{qreg q[n];} \qquad n \in \mathcal{Z} \\
&\ \textsf{creg c[n];} \qquad n \in \mathcal{Z} \\
&\ \text{S* \n}
\end{aligned}
$$

$$
\begin{aligned}
\text{S}\ &\rightarrow \textsf{h q[i]} \qquad 0 \leq i \leq n,\, i \in \mathcal{Z} \\
&\mid\ \ \textsf{x q[i]} \qquad 0 \leq i \leq n,\, i \in \mathcal{Z} \\
&\mid\ \ \textsf{t q[i]} \qquad 0 \leq i \leq n,\, i \in \mathcal{Z} \\
&\mid\ \ \textsf{tdg q[i]} \qquad 0 \leq i \leq n,\, i \in \mathcal{Z} \\
&\mid\ \ \textsf{cx q[i], q[j]} \qquad 0 \leq i, j \leq n,\, i, j \in \mathcal{Z} \\
&\mid\ \ \textsf{// }\epsilon^* \\
&\mid\ \ \epsilon
\end{aligned}
$$

4. This representation is then passed to the interpreter (`interp.py`). Using a weighted-ket class to represent singular kets with specific amplitudes and states as lists of weighted kets, the interpreter then starts in the all-0 state and apply gates in the operation list according to the following semantics:

$$X\ket{0} = \ket{1}, \quad X\ket{1} = \ket{0}$$
$$H\ket{0} = \dfrac{1}{\sqrt 2}\big(\ket{0} + \ket{1}\big), \quad H\ket{1} = \dfrac{1}{\sqrt 2}\big(\ket{0} - 1\rangle\big)$$
$$T\ket{0} = \ket{0}, \quad T\ket{1} = \dfrac{1+i}{\sqrt 2}\ket{1}$$
$$T^\dag \ket{0} = \ket{0}, \quad T^\dag\ket{1} = \dfrac{1-i}{\sqrt 2}\ket{1}$$
$$\text{(File headers, comments, and whitespace do nothing.)}$$

5. The final state is then reported. The simulator converts the state from a list of weighted kets to matrix form.


### Testing
* Running `python3 compare_simulators.py ./tests` will test the simulator against Cirq's simulator on the following 14 programs:

$$\begin{table}[h]
\centering
\begin{tabular}{lrr}
\hline
Circuit & Qubits & Lines \\
\hline
miller\_11.qasm        &  3 &   54  \\
decod24-v2\_43.qasm    &  4 &   56  \\
one-two-three-v3\_101.qasm &  5 &   74  \\
hwb5\_53.qasm          &  6 & 1,340 \\
alu-bdd\_288.qasm      &  7 &   88  \\
f2\_232.qasm           &  8 & 1,210 \\
con1\_216.qasm         &  9 &  958  \\
mini\_alu\_305.qasm    & 10 &  177  \\
wim\_266.qasm          & 11 &  990  \\
cm152a\_212.qasm       & 12 & 1,225 \\
squar5\_261.qasm       & 13 & 1,997 \\
sym6\_316.qasm         & 14 &  274  \\
rd84\_142.qasm         & 15 &  347  \\
cnt3-5\_179.qasm       & 16 &  179  \\
\hline
\end{tabular}
\end{table}$$

* Running `python3 scalability.py` will generate a graph mapping the number of qubits to the total simulator execution time for the same 14 test programs. 
