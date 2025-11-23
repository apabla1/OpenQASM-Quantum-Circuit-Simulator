### Grammar
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

### Semantic Rules
$$X\ket{0} = \ket{1}, \quad X\ket{1} = \ket{0}$$
$$H\ket{0} = \dfrac{1}{\sqrt 2}(\ket{0} + \ket{1}), \quad H\ket{1} = \dfrac{1}{\sqrt 2}(\ket{0} - 1\rangle)$$
$$T\ket{0} = \ket{0}, \quad T\ket{1} = \dfrac{1+i}{\sqrt 2}\ket{1}$$
$$T^\dag \ket{0} = \ket{0}, \quad T^\dag\ket{1} = \dfrac{1-i}{\sqrt 2}\ket{1}$$
$$\text{(File headers, comments, and whitespace do nothing.)}$$
