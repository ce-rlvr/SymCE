import sympy
from sympy import groebner, reduced, symbols, Dummy, S, factor_list, Mul
from sympy.abc import x, y, z, u, v, w
from itertools import combinations_with_replacement

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: P is a prime ideal of R",
    "H_3: The radical \sqrt{q_i} equals P for all i from 1 to k",
    "¬Q: The intersection q_1 \cap ... \cap q_k is not a primary ideal or its radical is not P"
]
N_HYP = 3
NEG_Q_INDEX = 3

def get_gb(I_gens, vars):
    if not I_gens:
        return None
    gens = [g for g in I_gens if g != 0]
    if not gens:
        return None
    return groebner(gens, *vars)

def in_ideal_gb(f, gb, vars):
    if gb is None:
        return f == 0
    try:
        _, rem = reduced(f, gb, *vars)
        return rem == 0
    except Exception:
        return False

def is_prime_ideal(P_gens, vars):
    if not P_gens:
        return True
    try:
        gb = list(groebner(P_gens, *vars))
    except Exception:
        return False
    if not gb:
        return True
    if len(gb) == 1 and gb[0] == 0:
        return True
    if len(gb) == 1 and gb[0] == 1:
        return False
    
    if len(gb) == 1:
        try:
            facs = factor_list(gb[0])
            if len(facs[1]) == 1 and facs[1][0][1] == 1:
                return True
        except Exception:
            pass

    try:
        is_linear = True
        for g in gb:
            if g.as_poly(*vars).total_degree() != 1:
                is_linear = False
                break
        if is_linear:
            return True
    except Exception:
        pass

    try:
        if all(g in vars for g in gb):
            return True
    except Exception:
        pass

    return False

def intersection(I_gens, J_gens, vars):
    t = Dummy('t')
    new_vars = (t,) + tuple(vars)
    gens = [t * g for g in I_gens] + [(1 - t) * g for g in J_gens]
    gb = groebner(gens, *new_vars, order='lex')
    intersect_gens = [g for g in gb if t not in g.free_symbols]
    return intersect_gens

def intersect_all(q_list, vars):
    if not q_list:
        return [S(1)]
    res = q_list[0]
    for q in q_list[1:]:
        res = intersection(res, q, vars)
    return res

def is_not_primary(I_gb, P_gb, vars):
    monomials = [S(1)] + list(vars)
    for d in range(2, 5):
        for comb in combinations_with_replacement(vars, d):
            m = Mul(*comb)
            monomials.append(m)
            
    for a in monomials:
        for b in monomials:
            if in_ideal_gb(a * b, I_gb, vars):
                if not in_ideal_gb(a, I_gb, vars):
                    if not in_ideal_gb(b, P_gb, vars):
                        return True
    return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            vars = witness.get('vars', [])
            P_gens = witness.get('P', [])
            q_list = witness.get('q_list', [])
        else:
            vars, P_gens, q_list = witness
    except Exception:
        return [False, False, False, False]

    # H1: R is a commutative ring with identity
    try:
        h1 = isinstance(vars, (list, tuple)) and len(vars) > 0 and all(isinstance(v, sympy.Symbol) for v in vars)
    except Exception:
        h1 = False

    # H2: P is a prime ideal of R
    try:
        h2 = is_prime_ideal(P_gens, vars)
    except Exception:
        h2 = False

    # H3: The radical \sqrt{q_i} equals P for all i from 1 to k
    try:
        h3 = True
        if not q_list:
            h3 = False
        P_gb = get_gb(P_gens, vars)
        for q in q_list:
            q_gb = get_gb(q, vars)
            # q subset P
            for g in q:
                if not in_ideal_gb(g, P_gb, vars):
                    h3 = False
                    break
            if not h3: break
            # P subset radical(q)
            for p in P_gens:
                found = False
                for n in range(1, 15):
                    if in_ideal_gb(p**n, q_gb, vars):
                        found = True
                        break
                if not found:
                    h3 = False
                    break
            if not h3: break
    except Exception:
        h3 = False

    # neg_Q: The intersection q_1 \cap ... \cap q_k is not a primary ideal or its radical is not P
    try:
        neg_q = False
        I_gens = intersect_all(q_list, vars)
        I_gb = get_gb(I_gens, vars)
        P_gb = get_gb(P_gens, vars)
        
        rad_not_P = False
        for g in I_gens:
            if not in_ideal_gb(g, P_gb, vars):
                rad_not_P = True
                break
        if not rad_not_P:
            for p in P_gens:
                found = False
                for n in range(1, 15):
                    if in_ideal_gb(p**n, I_gb, vars):
                        found = True
                        break
                if not found:
                    rad_not_P = True
                    break
        
        if rad_not_P:
            neg_q = True
        else:
            neg_q = is_not_primary(I_gb, P_gb, vars)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]