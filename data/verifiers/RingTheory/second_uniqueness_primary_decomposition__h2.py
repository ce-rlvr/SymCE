import sympy
from sympy import symbols, groebner, reduced
from sympy.abc import x, y, z, u, v, w

# Top-level setup
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def intersect_ideals(I1, I2_ideal, gens):
    t_dummy = symbols('t_dummy_intersect')
    gens_ext = [t_dummy] + list(gens)
    J = [t_dummy * f for f in I1] + [(1 - t_dummy) * g for g in I2_ideal]
    gb = groebner(J, *gens_ext, order='lex')
    intersection = [p for p in gb if t_dummy not in p.free_symbols]
    return intersection

def intersect_multiple_ideals(ideals, gens):
    if not ideals:
        return [sympy.S.One]
    res = ideals[0]
    for I in ideals[1:]:
        res = intersect_ideals(res, I, gens)
    return res

def is_in_ideal(f, I, gens):
    if not I:
        return f == 0 or f == sympy.S.Zero
    try:
        gb = groebner(I, *gens)
        _, r = reduced(f, gb, *gens)
        return r == 0 or r == sympy.S.Zero
    except Exception:
        return False

def ideal_subset(I1, I2_ideal, gens):
    if not I2_ideal:
        return all(f == 0 or f == sympy.S.Zero for f in I1)
    try:
        gb = groebner(I2_ideal, *gens)
        for f in I1:
            _, r = reduced(f, gb, *gens)
            if r != 0 and r != sympy.S.Zero:
                return False
        return True
    except Exception:
        return False

def ideals_equal(I1, I2_ideal, gens):
    return ideal_subset(I1, I2_ideal, gens) and ideal_subset(I2_ideal, I1, gens)

def is_minimal_prime(P_list, i, gens):
    Pi = P_list[i]
    for j, Pj in enumerate(P_list):
        if j != i:
            if ideal_subset(Pj, Pi, gens) and not ideal_subset(Pi, Pj, gens):
                return False
    return True

def conditions(witness):
    try:
        gens = witness['gens']
        I = witness['I']
        Q_list = witness['Q_list']
        P_list = witness['P_list']
        idx = witness['i']
    except Exception:
        return [False, False, False, False]

    if len(Q_list) != len(P_list):
        return [False, False, False, False]

    # H_1: R is a commutative ring
    # Polynomial rings over fields (which we use here) are commutative rings.
    h1 = True
    
    # H_2: I = \bigcap_{i=1}^n Q_i is a minimal primary decomposition of I
    h2 = False
    try:
        int_Q = intersect_multiple_ideals(Q_list, gens)
        if ideals_equal(I, int_Q, gens):
            minimal = True
            for j in range(len(Q_list)):
                Q_without_j = Q_list[:j] + Q_list[j+1:]
                int_Q_without_j = intersect_multiple_ideals(Q_without_j, gens)
                if ideals_equal(I, int_Q_without_j, gens):
                    minimal = False
                    break
            if minimal:
                distinct = True
                for j in range(len(P_list)):
                    for k in range(j + 1, len(P_list)):
                        if ideals_equal(P_list[j], P_list[k], gens):
                            distinct = False
                            break
                    if not distinct:
                        break
                if distinct:
                    radicals_ok = True
                    for Q, P in zip(Q_list, P_list):
                        if not ideal_subset(Q, P, gens):
                            radicals_ok = False
                            break
                        for p in P:
                            in_rad = False
                            for m in range(1, 15):
                                if is_in_ideal(p**m, Q, gens):
                                    in_rad = True
                                    break
                            if not in_rad:
                                radicals_ok = False
                                break
                        if not radicals_ok:
                            break
                    if radicals_ok:
                        h2 = True
    except Exception:
        h2 = False

    # H_3: P_i = \sqrt{Q_i} is a minimal element in the set of associated primes of I with respect to inclusion
    h3 = False
    try:
        if 0 <= idx < len(P_list):
            h3 = is_minimal_prime(P_list, idx, gens)
    except Exception:
        h3 = False

    # ¬Q: The primary component Q_i is NOT uniquely determined by I
    neg_q = False
    try:
        Q_list_alt = witness['Q_list_alt']
        int_Q_alt = intersect_multiple_ideals(Q_list_alt, gens)
        if ideals_equal(I, int_Q_alt, gens):
            minimal_alt = True
            for j in range(len(Q_list_alt)):
                Q_alt_without_j = Q_list_alt[:j] + Q_list_alt[j+1:]
                int_Q_alt_without_j = intersect_multiple_ideals(Q_alt_without_j, gens)
                if ideals_equal(I, int_Q_alt_without_j, gens):
                    minimal_alt = False
                    break
            if minimal_alt:
                if len(Q_list_alt) != len(P_list):
                    radicals_alt_ok = False
                else:
                    radicals_alt_ok = True
                    for Q_alt, P in zip(Q_list_alt, P_list):
                        if not ideal_subset(Q_alt, P, gens):
                            radicals_alt_ok = False
                            break
                        for p in P:
                            in_rad = False
                            for m in range(1, 15):
                                if is_in_ideal(p**m, Q_alt, gens):
                                    in_rad = True
                                    break
                            if not in_rad:
                                radicals_alt_ok = False
                                break
                        if not radicals_alt_ok:
                            break
                if radicals_alt_ok:
                    if not ideals_equal(Q_list[idx], Q_list_alt[idx], gens):
                        neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I = \\bigcap_{i=1}^n Q_i is a minimal primary decomposition of I",
    "H_3: P_i = \\sqrt{Q_i} is a minimal element in the set of associated primes of I with respect to inclusion",
    "¬Q: The primary component Q_i is NOT uniquely determined by I"
]

N_HYP = 3
NEG_Q_INDEX = 3