import itertools

def parse_witness(witness):
    if isinstance(witness, tuple) and len(witness) == 3:
        n, m, f_dict = witness
        R_elements = list(range(n))
        R_add = {(a, b): (a + b) % n for a in R_elements for b in R_elements}
        R_mul = {(a, b): (a * b) % n for a in R_elements for b in R_elements}
        S_elements = list(range(m))
        S_add = {(a, b): (a + b) % m for a in S_elements for b in S_elements}
        S_mul = {(a, b): (a * b) % m for a in S_elements for b in S_elements}
        if callable(f_dict):
            f = {x: f_dict(x) for x in R_elements}
        else:
            f = f_dict
        return R_elements, R_add, R_mul, S_elements, S_add, S_mul, f
    elif isinstance(witness, tuple) and len(witness) == 7:
        return witness
    else:
        raise ValueError("Invalid witness format")

def is_ring(elements, add, mul):
    if not elements: return False
    # closure
    for a in elements:
        for b in elements:
            if add.get((a, b)) not in elements: return False
            if mul.get((a, b)) not in elements: return False
    # add commutativity
    for a in elements:
        for b in elements:
            if add[(a, b)] != add[(b, a)]: return False
    # add associativity
    for a in elements:
        for b in elements:
            for c in elements:
                if add[(add[(a, b)], c)] != add[(a, add[(b, c)])]: return False
    # zero
    zeros = [z for z in elements if all(add[(z, a)] == a for a in elements)]
    if not zeros: return False
    z = zeros[0]
    # inverses
    for a in elements:
        if not any(add[(a, b)] == z for b in elements): return False
    # mul associativity
    for a in elements:
        for b in elements:
            for c in elements:
                if mul[(mul[(a, b)], c)] != mul[(a, mul[(b, c)])]: return False
    # distributivity
    for a in elements:
        for b in elements:
            for c in elements:
                if mul[(a, add[(b, c)])] != add[(mul[(a, b)], mul[(a, c)])]: return False
                if mul[(add[(a, b)], c)] != add[(mul[(a, c)], mul[(b, c)])]: return False
    # identity
    ones = [e for e in elements if all(mul[(e, a)] == a and mul[(a, e)] == a for a in elements)]
    if not ones: return False
    return True

def is_valid_f(R_elements, S_elements, f):
    for a in R_elements:
        if a not in f: return False
        if f[a] not in S_elements: return False
    return True

def conditions(witness):
    try:
        R_elements, R_add, R_mul, S_elements, S_add, S_mul, f = parse_witness(witness)
    except Exception:
        return [False, False]

    try:
        h1 = is_ring(R_elements, R_add, R_mul) and is_ring(S_elements, S_add, S_mul) and is_valid_f(R_elements, S_elements, f)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            zeros_S = [z for z in S_elements if all(S_add[(z, a)] == a for a in S_elements)]
            if not zeros_S:
                neg_q = True
            else:
                zero_S = zeros_S[0]
                ker_f = [x for x in R_elements if f[x] == zero_S]
                
                # Check if ker_f is an ideal
                is_ideal = True
                for a in ker_f:
                    for b in ker_f:
                        if R_add[(a, b)] not in ker_f: is_ideal = False
                for a in ker_f:
                    for r in R_elements:
                        if R_mul[(a, r)] not in ker_f: is_ideal = False
                        if R_mul[(r, a)] not in ker_f: is_ideal = False
                
                if not is_ideal:
                    neg_q = True
                else:
                    # Build cosets
                    cosets = []
                    for x in R_elements:
                        coset = frozenset(R_add[(x, k)] for k in ker_f)
                        if coset not in cosets:
                            cosets.append(coset)
                    
                    # Image f(R)
                    f_R = list(set(f[x] for x in R_elements))
                    
                    # Check if f_R is a subring of S
                    is_subring = True
                    for a in f_R:
                        for b in f_R:
                            if S_add[(a, b)] not in f_R: is_subring = False
                            if S_mul[(a, b)] not in f_R: is_subring = False
                    
                    # Check if f_R has an identity
                    has_id = False
                    for e in f_R:
                        if all(S_mul[(e, a)] == a and S_mul[(a, e)] == a for a in f_R):
                            has_id = True
                            break
                    if not has_id:
                        is_subring = False
                    
                    if not is_subring:
                        neg_q = True
                    else:
                        # Check isomorphism
                        if len(cosets) != len(f_R):
                            neg_q = True
                        else:
                            is_iso_overall = False
                            for perm in itertools.permutations(f_R):
                                mapping = {i: perm[i] for i in range(len(cosets))}
                                is_iso = True
                                for i in range(len(cosets)):
                                    for j in range(len(cosets)):
                                        c1 = cosets[i]
                                        c2 = cosets[j]
                                        rep1 = next(iter(c1))
                                        rep2 = next(iter(c2))
                                        
                                        sum_rep = R_add[(rep1, rep2)]
                                        sum_idx = next(k for k, c in enumerate(cosets) if sum_rep in c)
                                        if S_add[(mapping[i], mapping[j])] != mapping[sum_idx]:
                                            is_iso = False
                                            break
                                        
                                        mul_rep = R_mul[(rep1, rep2)]
                                        mul_idx = next(k for k, c in enumerate(cosets) if mul_rep in c)
                                        if S_mul[(mapping[i], mapping[j])] != mapping[mul_idx]:
                                            is_iso = False
                                            break
                                    if not is_iso:
                                        break
                                if is_iso:
                                    is_iso_overall = True
                                    break
                            neg_q = not is_iso_overall
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Let R and S be rings",
    "¬Q: The quotient ring R/\\ker(f) is not isomorphic to the image f(R)"
]

N_HYP = 1
NEG_Q_INDEX = 1