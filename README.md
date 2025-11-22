### Grammar
$$
\begin{aligned}
\text{P}\ \rightarrow &\ \textsf{OPENQASM 2.0;} \\
&\ \textsf{include "qelib1.inc";} \\
&\ \textsf{qreg q[n];} \qquad n \in \mathcal{Z} \\
&\ \textsf{creg c[n];} \qquad n \in \mathcal{Z} \\
&\ \text{S*}
\end{aligned}
$$

$$
\begin{aligned}
\text{S}\ \rightarrow&\ \textsf{h q[i]} \qquad 0 \leq i \leq n,\, i \in \mathcal{Z} \\
&\mid\ \ \textsf{x q[i]} \qquad 0 \leq i \leq n,\, i \in \mathcal{Z} \\
&\mid\ \ \textsf{t q[i]} \qquad 0 \leq i \leq n,\, i \in \mathcal{Z} \\
&\mid\ \ \textsf{tdg q[i]} \qquad 0 \leq i \leq n,\, i \in \mathcal{Z} \\
&\mid\ \ \textsf{cx q[i], q[j]} \qquad 0 \leq i, j \leq n,\, i, j \in \mathcal{Z}
\end{aligned}
$$