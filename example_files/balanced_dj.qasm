// DJ Algorithm for balanced f

OPENQASM 2.0;
include "qelib1.inc";

qreg q[4];
creg c[4];

x q[2];

h q[0];
h q[1];
h q[2];

// Uf for balanced f(x, y) = x
cx q[0], q[2];

h q[0];
h q[1];

// expected: 10 in first 2 qubits
