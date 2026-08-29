import itertools

# Precompute finite groups S3 and S4 for testing relation independence
def get_Sn(n):
    elements = list(itertools.permutations(range(n)))
    idx_map = {e: i for i, e in enumerate(elements)}
    mult_table = []
    inv_table = []
    for e1 in elements:
        row = []
        for e2 in elements:
            # e1 * e2 means e1(e2(x))
            prod = tuple(e1[e2[i]] for i in range(n))
            row.append(idx_map[prod])
        mult_table.append(row)
        
        inv = tuple(e1.index(i) for i in range(n))
        inv_table.append(idx_map[inv])
        
    return list(range(len(elements))), mult_table, inv_table

S3_elems, S3_mult, S3_inv = get_Sn(3)
S4_elems, S4_mult, S4_inv = get_Sn(4)

def check_H1(witness):
    """
    Check if the witness is a valid regular planar projection of a knot/link
    with n arcs and n crossings.
    Witness format: list of tuples (over_arc, in_arc, out_arc, sign)
    where arcs are integers 0 to n-1, and sign is 1 or -1.
    """
    try:
        if not isinstance(witness, list): return False
        n = len(witness)
        if n < 1: return False
        
        in_arcs = []
        out_arcs = []
        for crossing in witness:
            if not isinstance(crossing, (list, tuple)): return False
            if len(crossing) != 4: return False
            over, in_a, out_a, sign = crossing
            if not isinstance(over, int) or not isinstance(in_a, int) or not isinstance(out_a, int): return False
            if not (0 <= over < n and 0 <= in_a < n and 0 <= out_a < n): return False
            if sign not in [1, -1]: return False
            in_arcs.append(in_a)
            out_arcs.append(out_a)
            
        # Every arc must be an in-arc exactly once and an out-arc exactly once
        if sorted(in_arcs) != list(range(n)): return False
        if sorted(out_arcs) != list(range(n)): return False
        
        return True
    except Exception:
        return False

def check_homomorphisms(R, k, H_elements, H_mult, H_inv, max_states=200000):
    """
    Check if the k-th relation is independent of the others by finding a homomorphism
    to a finite group H where all relations except the k-th hold, but the k-th fails.
    """
    n = len(R)
    assignment = [None] * n
    rels = [r for i, r in enumerate(R) if i != k]
    target_rel = R[k]
    
    state_count = [0]
    
    def deduce(current_assignment):
        changed = True
        assign = list(current_assignment)
        while changed:
            changed = False
            for over, in_a, out_a, sign in rels:
                o = assign[over]
                i = assign[in_a]
                out_val = assign[out_a]
                
                if o is not None:
                    if i is not None and out_val is None:
                        if sign == 1:
                            assign[out_a] = H_mult[H_inv[o]][H_mult[i][o]]
                        else:
                            assign[out_a] = H_mult[o][H_mult[i][H_inv[o]]]
                        changed = True
                    elif out_val is not None and i is None:
                        if sign == 1:
                            assign[in_a] = H_mult[o][H_mult[out_val][H_inv[o]]]
                        else:
                            assign[in_a] = H_mult[H_inv[o]][H_mult[out_val][o]]
                        changed = True
                
                if o is not None and i is not None and out_val is not None:
                    if sign == 1:
                        expected_out = H_mult[H_inv[o]][H_mult[i][o]]
                    else:
                        expected_out = H_mult[o][H_mult[i][H_inv[o]]]
                    if out_val != expected_out:
                        return None
        return assign

    def backtrack(idx, current_assignment):
        state_count[0] += 1
        if state_count[0] > max_states:
            return False
            
        if idx == n:
            over, in_a, out_a, sign = target_rel
            o = current_assignment[over]
            i = current_assignment[in_a]
            out_val = current_assignment[out_a]
            if sign == 1:
                expected_out = H_mult[H_inv[o]][H_mult[i][o]]
            else:
                expected_out = H_mult[o][H_mult[i][H_inv[o]]]
            if out_val != expected_out:
                return True
            return False
            
        if current_assignment[idx] is not None:
            return backtrack(idx + 1, current_assignment)
            
        for g in H_elements:
            new_assign = list(current_assignment)
            new_assign[idx] = g
            deduced = deduce(new_assign)
            if deduced is not None:
                if backtrack(idx + 1, deduced):
                    return True
        return False

    return backtrack(0, assignment)

def check_neg_Q(witness):
    """
    Check if the conclusion fails.
    The conclusion fails if there exists a crossing relation that CANNOT be omitted
    without changing the group (i.e., it is not a consequence of the other relations).
    """
    try:
        if not check_H1(witness):
            return False
        n = len(witness)
        for k in range(n):
            # If we find a homomorphism to S3 or S4 that violates r_k while satisfying the rest,
            # then r_k is not a consequence, so omitting it changes the group.
            if check_homomorphisms(witness, k, S3_elems, S3_mult, S3_inv):
                return True
            if check_homomorphisms(witness, k, S4_elems, S4_mult, S4_inv):
                return True
        return False
    except Exception:
        return False

def conditions(witness):
    return [
        check_H1(witness),
        check_neg_Q(witness)
    ]

CONDITION_LABELS = [
    "H_1: D is a regular planar projection of K with n arcs and n crossings",
    "¬Q: Omitting some crossing relation changes the group (relation is not a consequence)"
]

N_HYP = 1
NEG_Q_INDEX = 1