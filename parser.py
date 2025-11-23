def parse(toks):
    parse_tree = {
        "qreg_size": None,
        "creg_size": None,
        "ops": [],
    }
    for type, value in toks:
        if type in ['COMMENT', 'NEWLINE', 'OPENQASM 2.0', 'INCLUDE_QELIB1']:
            continue
        elif type == 'QREG':
            reg_idx, _ = value
            parse_tree["qreg_size"] = int(reg_idx)
        elif type == 'CREG':
            reg_idx, _ = value
            parse_tree["creg_size"] = int(reg_idx)
        elif type in ['H', 'X', 'T', 'TDG']:
            qubit_idx, _ = value
            parse_tree["ops"].append({
                "gate": type,          
                "qubits": [int(qubit_idx)], 
            })
        elif type == 'CX':
            control_idx, target_idx = value
            parse_tree["ops"].append({
                "gate": "CX",
                "qubits": [int(control_idx), int(target_idx)],  # [control, target]
            })
        else:
            raise ValueError(f"Unknown token type: {type}")

    return parse_tree

if __name__ == "__main__":
    import sys
    from lexer import lex
    tokens = lex(sys.argv[1])
    parse_tree = parse(tokens)
    import pprint
    pprint.pprint(parse_tree)