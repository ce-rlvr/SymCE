import sympy
from sympy import Poly, Symbol, QQ
from sympy.ntheory import isprime

x = Symbol('x')

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (F, f, K_1, K_2) or a dictionary with these keys.
    """
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            f = witness.get('f')
            K_1 = witness.get('K_1')
            K_2 = witness.get('K_2')
        else:
            F, f, K_1, K_2 = witness
    except Exception:
        return [False, False, False, False]

    # H_1: F is a field
    try:
        H1 = hasattr(F, 'is_Field') and F.is_Field
    except Exception:
        H1 = False

    # H_2: f(x) is a non-constant polynomial over F
    try:
        free_symbols = f.free_symbols
        if len(free_symbols) != 1:
            H2 = False
        else:
            sym = list(free_symbols)[0]
            p = Poly(f, sym)
            if p.degree() < 1:
                H2 = False
            else:
                H2 = all(c in F for c in p.coeffs())
    except Exception:
        H2 = False

    # H_3: K_1 is a splitting field of f(x) over F
    try:
        if not (hasattr(K_1, 'is_Field') and K_1.is_Field):
            H3 = False
        else:
            free_symbols = f.free_symbols
            sym = list(free_symbols)[0]
            p = Poly(f, sym)
            
            factors_K1 = p.factor_list(domain=K_1)
            splits_in_K1 = all(fac.degree() == 1 for fac, mult in factors_K1[1])
            
            if not splits_in_K1:
                H3 = False
            else:
                if K_1 == F:
                    H3 = True
                elif F == QQ and hasattr(K_1, 'mod'):
                    deg = K_1.mod.degree()
                    factors_F = p.factor_list(domain=F)
                    splits_in_F = all(fac.degree() == 1 for fac, mult in factors_F[1])
                    
                    if not splits_in_F and isprime(deg):
                        H3 = True
                    else:
                        from sympy.polys.numberfields import primitive_element
                        from sympy import Dummy
                        roots_dict = p.roots(domain=K_1)
                        roots_expr = []
                        for r in roots_dict.keys():
                            if hasattr(r, 'as_expr'):
                                re = r.as_expr()
                            else:
                                re = r
                            if not getattr(re, 'is_Rational', False):
                                roots_expr.append(re)
                        
                        if not roots_expr:
                            H3 = (K_1 == QQ)
                        else:
                            minpoly, _ = primitive_element(roots_expr, Dummy('x'))
                            H3 = (minpoly.degree() == deg)
                else:
                    H3 = False
    except Exception:
        H3 = False

    # neg_Q: There does not exist a field isomorphism from K_1 to K_2 fixing F
    try:
        def get_degree(K, base_F):
            if K == base_F:
                return 1
            if base_F == QQ and hasattr(K, 'mod'):
                return K.mod.degree()
            return None

        if not (hasattr(K_2, 'is_Field') and K_2.is_Field):
            neg_Q = True
        else:
            deg1 = get_degree(K_1, F)
            deg2 = get_degree(K_2, F)
            
            if deg1 is not None and deg2 is not None:
                if deg1 != deg2:
                    neg_Q = True
                else:
                    if deg1 == 1:
                        neg_Q = False
                    elif K_1 == K_2:
                        neg_Q = False
                    else:
                        try:
                            roots_in_K2 = K_1.mod.roots(domain=K_2)
                            if sum(roots_in_K2.values()) > 0:
                                neg_Q = False
                            else:
                                neg_Q = True
                        except Exception:
                            neg_Q = True
            else:
                neg_Q = False
    except Exception:
        neg_Q = False

    return [bool(H1), bool(H2), bool(H3), bool(neg_Q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f is a non-constant polynomial over F",
    "H_3: K_1 is a splitting field of f over F",
    "¬Q: There does not exist a field isomorphism from K_1 to K_2 fixing F"
]

N_HYP = 3
NEG_Q_INDEX = 3