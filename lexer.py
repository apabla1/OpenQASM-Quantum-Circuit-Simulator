import re

QREG = re.compile(r'^qreg\s+q\[(\d+)\];$')
CREG = re.compile(r'^creg\s+c\[(\d+)\];$')
SQ_GATE = re.compile(r'^(h|x|t|tdg)\s+q\[(\d+)\];$')
CX_GATE = re.compile(r'^cx\s+q\[(\d+)\],\s*q\[(\d+)\];$')

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
        m = QREG.match(line)
        if m:
            reg_idx = m.group(1)
            toks.append(('QREG', (reg_idx, None)))
            continue
        m = CREG.match(line)
        if m:
            reg_idx = m.group(1)
            toks.append(('CREG', (reg_idx, None)))
            continue
        m = SQ_GATE.match(line)
        if m:
            gate, qubit_idx = m.groups()
            toks.append((gate.upper(), (qubit_idx, None)))
            continue
        m = CX_GATE.match(line)
        if m:
            control_idx, target_idx = m.groups()
            toks.append(('CX', (control_idx, target_idx)))
            continue
        raise ValueError(f"Unknown instruction: {line}")
    return toks
                
if __name__ == "__main__":
    import sys
    toks = lex(sys.argv[1])
    import pprint
    pprint.pprint(toks)