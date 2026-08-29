import sympy
from sympy import Poly, groebner, reduced, factor_list, cancel
from sympy.abc import x, y, z, t, u, v, w

# Top-level setup
# The witness is expected to be a list or tuple of sympy expressions representing 
# the generators of an ideal in a polynomial ring over the rationals.

def conditions(witness):
    h1_ok = False
    h2_ok = False
    neg_q_ok = False
    
    try:
        if isinstance(witness, (list, tuple)):
            from sympy import Expr
            if all(isinstance(g, (Expr, int)) for g in witness):
                h1_ok = True
    except Exception:
        h1_ok = False
        
    try:
        if h1_ok:
            gens_set = set().union(*[getattr(g, 'free_symbols', set()) for g in witness])
            gens = sorted(list(gens_set), key=lambda sym: sym.name)
            
            is_homog = True
            for g in witness:
                if g == 0:
                    continue
                if not gens:
                    pass
                else:
                    p = Poly(g, *gens)
                    if not p.is_homogeneous:
                        is_homog = False
                        break
            
            is_proper = True
            if not gens:
                if not all(g == 0 for g in witness):
                    is_proper = False
            else:
                G = list(groebner(witness, *gens))
                _, rem = reduced(1, G, gens)
                if rem == 0:
                    is_proper = False
                    
            h2_ok = is_homog and is_proper
    except Exception:
        h2_ok = False
        
    try:
        if h1_ok:
            gens_set = set().union(*[getattr(g, 'free_symbols', set()) for g in witness])
            gens = sorted(list(gens_set), key=lambda sym: sym.name)
            
            if not gens:
                if all(g == 0 for g in witness):
                    neg_q_ok = False
                else:
                    neg_q_ok = True
            else:
                G = list(groebner(witness, *gens))
                
                def in_ideal(expr):
                    if not G:
                        return expr == 0
                    _, r = reduced(expr, G, gens)
                    return r == 0
                
                if in_ideal(1):
                    neg_q_ok = True
                else:
                    found_not_prime = False
                    
                    for p in list(witness) + G:
                        if p == 0:
                            continue
                        try:
                            coeff, factors = factor_list(p)
                        except Exception:
                            continue
                            
                        for f, exp in factors:
                            if exp > 1:
                                if not in_ideal(f):
                                    found_not_prime = True
                                    break
                        if found_not_prime:
                            break
                            
                        if len(factors) > 1:
                            f1 = factors[0][0]
                            if not in_ideal(f1):
                                cofactor = cancel(p / f1)
                                if not in_ideal(cofactor):
                                    found_not_prime = True
                                    break
                                    
                    if not found_not_prime:
                        for v_var in gens:
                            if in_ideal(v_var):
                                continue
                            for k in range(2, 6):
                                if in_ideal(v_var**k):
                                    found_not_prime = True
                                    break
                            if found_not_prime:
                                break
                                
                    if not found_not_prime:
                        for i in range(len(gens)):
                            for j in range(i+1, len(gens)):
                                v1, v2 = gens[i], gens[j]
                                if in_ideal(v1*v2):
                                    if not in_ideal(v1) and not in_ideal(v2):
                                        found_not_prime = True
                                        break
                            if found_not_prime:
                                break
                                
                    neg_q_ok = found_not_prime
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a graded commutative ring",
    "H_2: I is a proper homogeneous ideal of R",
    "¬Q: I is not a prime ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2