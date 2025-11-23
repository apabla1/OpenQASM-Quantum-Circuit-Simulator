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
$$X|0\rangle = |1\rangle, \quad X|1\rangle = |0\rangle$$
$$H|0\rangle = \dfrac{1}{\sqrt 2}(|0\rangle + |1\rangle), \quad H|1\rangle = \dfrac{1}{\sqrt 2}(|0\rangle - \1\rangle)$$
$$T|0\rangle = |0\rangle, \quad T|1\rangle = \dfrac{1+i}{\sqrt 2}|1\rangle$$
$$T^\dag |0\rangle = |0\rangle, \quad T^\dag|1\rangle = \dfrac{1-i}{\sqrt 2}|1\rangle$$
$$\text{(File headers, comments, and whitespace do nothing.)}$$
