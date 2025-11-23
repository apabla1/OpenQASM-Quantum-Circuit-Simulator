def parse(toks):
    parse_tree = {
        "qreg_size": None,
        "creg_size": None,
        "ops": [],
    }
    max_qubit_used = -1 # to purge unused qubits
    for type, value in toks:
        if type in ['COMMENT', 'NEWLINE', 'OPENQASM 2.0', 'INCLUDE_QELIB1']:
            continue
        elif type == 'CREG':
            reg_idx, _ = value
            parse_tree["creg_size"] = int(reg_idx)
        elif type == 'QREG':
            reg_idx, _ = value
            parse_tree["qreg_size"] = int(reg_idx)
        elif type in ['H', 'X', 'T', 'TDG']:
            qubit_idx, _ = value
            q = int(qubit_idx)
            parse_tree["ops"].append({
                "gate": type,          
                "qubits": [q], 
            })
            if q > max_qubit_used:
                max_qubit_used = q
        elif type == 'CX':
            control_idx, target_idx = value
            c = int(control_idx)
            t = int(target_idx)
            parse_tree["ops"].append({
                "gate": "CX",
                "qubits": [c, t],  # [control, target]
            })
            if c > max_qubit_used or t > max_qubit_used:
                max_qubit_used = max(c, t)
        else:
            raise ValueError(f"Unknown token type: {type}")
    # purge unused qubits
    if max_qubit_used >= 0:
        parse_tree["qreg_size"] = max_qubit_used + 1

    return parse_tree

if __name__ == "__main__":
    import sys
    from lexer import lex
    tokens = lex(sys.argv[1])
    parse_tree = parse(tokens)
    import pprint
    pprint.pprint(parse_tree)