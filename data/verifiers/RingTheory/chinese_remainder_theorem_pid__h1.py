import sympy
from sympy import S, gcd, groebner, symbols
from sympy.abc import x, y, z, t, u, v, w

CONDITION_LABELS = [
    "H_1: a_1, a_2, ..., a_k are non-zero elements of R",
    "H_2: For all i != j, a_i and a_j are coprime",
    "¬Q: R/(a_1...a_k) is not isomorphic to the direct product R/(a_1) x ... x R/(a_k)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_domain_and_gens(exprs):
    gens = set()
    for e in exprs:
        gens.update(e.free_symbols)
    gens = sorted(list(gens), key=lambda sym: sym.name)
    
    domain = 'ZZ'
    for e in exprs:
        if any((a.is_number and not a.is_Integer) for a in e.atoms()):
            domain = 'QQ'
            break
    return gens, domain

def is_unit(expr, domain, gens):
    try:
        expr = S(expr)
        if domain == 'ZZ':
            return expr in [S(1), S(-1)]
        else:
            if not gens:
                return expr != S(0)
            return expr.is_number and expr != S(0)
    except Exception:
        return False

def are_coprime(a, b, domain, gens):
    try:
        g = gcd(a, b)
        return is_unit(g, domain, gens)
    except Exception:
        return False

def are_comaximal(a, b, domain, gens):
    try:
        if not gens:
            g = gcd(a, b)
            return is_unit(g, domain, gens)
        gb = groebner([a, b], *gens, domain=domain)
        gb_list = list(gb)
        if len(gb_list) == 1:
            return is_unit(gb_list[0], domain, gens)
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)):
            return [False, False, False]
        
        exprs = [S(w) for w in witness]
    except Exception:
        return [False, False, False]
        
    if len(exprs) < 2:
        try:
            h1 = all(e != S(0) for e in exprs)
        except Exception:
            h1 = False
        return [h1, True, False]

    gens, domain = get_domain_and_gens(exprs)
    
    try:
        h1 = all(e != S(0) for e in exprs)
    except Exception:
        h1 = False
        
    try:
        h2 = True
        for i in range(len(exprs)):
            for j in range(i+1, len(exprs)):
                if not are_coprime(exprs[i], exprs[j], domain, gens):
                    h2 = False
                    break
            if not h2:
                break
    except Exception:
        h2 = False
        
    try:
        all_comaximal = True
        for i in range(len(exprs)):
            for j in range(i+1, len(exprs)):
                if not are_comaximal(exprs[i], exprs[j], domain, gens):
                    all_comaximal = False
                    break
            if not all_comaximal:
                break
        neg_q = not all_comaximal
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]