import sympy

x = sympy.Symbol('x')

def field_degree(gens):
    valid_gens = [g for g in gens if not g.is_Rational]
    if not valid_gens:
        return 1
    primes = list(sympy.primerange(2, 200))
    pe = sum(p * g for p, g in zip(primes, valid_gens))
    return sympy.minpoly(pe).degree()

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple):
            f = sympy.sympify(witness[0])
        else:
            f = sympy.sympify(witness)
            
        free_syms = f.free_symbols
        if len(free_syms) == 1:
            var = list(free_syms)[0]
        elif len(free_syms) == 0:
            var = sympy.Symbol('x')
        else:
            raise ValueError
            
        poly = sympy.Poly(f, var)
        if poly.domain.is_RationalField or poly.domain.is_IntegerRing:
            h1 = True
    except Exception:
        h1 = False

    try:
        if h1:
            roots_dict = sympy.roots(f, var)
            if sum(roots_dict.values()) < poly.degree():
                neg_q = True
            else:
                rts = list(roots_dict.keys())
                d_K = field_degree(rts)
                if d_K != 4:
                    neg_q = True
                else:
                    target_gens = [sympy.sqrt(-3), sympy.sqrt(-11)]
                    d_combined = field_degree(rts + target_gens)
                    if d_combined != 4:
                        neg_q = True
                    else:
                        neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = ["H_1: K is the splitting field of f(x) over Q", "not Q: K is not Q(sqrt(-3), sqrt(-11)) or degree is not 4"]
N_HYP = 1
NEG_Q_INDEX = 1