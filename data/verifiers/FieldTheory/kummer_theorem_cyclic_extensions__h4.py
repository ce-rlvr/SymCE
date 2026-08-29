import sympy
from sympy import Symbol, Poly, cyclotomic_poly
from sympy.polys.domains import CC, QQ, RR, ZZ, FF

# Top-level setup for witness evaluation
x = Symbol('x')

def conditions(witness):
    try:
        K, n = witness
    except Exception:
        return [False, False, False, False]
    
    # Safely parse n as an integer
    try:
        n_int = int(n)
        is_pos_int = (n_int == n) and (n_int > 0)
    except Exception:
        is_pos_int = False

    # H_1: K is a field
    try:
        h1 = getattr(K, 'is_Field', False)
    except Exception:
        h1 = False
        
    # H_2: n is a positive integer such that the characteristic of K does not divide n
    try:
        if is_pos_int:
            n_val = n_int
            char = getattr(K, 'char', None)
            if char is None:
                if hasattr(K, 'characteristic'):
                    char = K.characteristic()
                else:
                    char = 0
            if char is not None:
                if char == 0:
                    h2 = True
                else:
                    h2 = (n_val % char != 0)
            else:
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # H_3: K contains a primitive n-th root of unity
    try:
        if not is_pos_int:
            h3 = False
        elif K == CC:
            h3 = True
        elif K == RR:
            h3 = (n_int in (1, 2))
        elif K == QQ:
            h3 = (n_int in (1, 2))
        else:
            char = getattr(K, 'char', 0)
            if char > 0 and hasattr(K, 'order'):
                q = K.order
                h3 = ((q - 1) % n_int == 0)
            else:
                poly = cyclotomic_poly(n_int, x)
                factors = poly.factor_list(domain=K)[1]
                h3 = any(f[0].degree() == 1 for f in factors)
    except Exception:
        h3 = False
        
    # Conclusion: There exists an element a in K such that x^n - a is irreducible over K
    try:
        if not is_pos_int:
            conc = True
        elif n_int == 1:
            conc = True
        elif K == CC:
            conc = False
        elif K == RR:
            conc = (n_int == 2)
        elif K == QQ:
            conc = True
        else:
            char = getattr(K, 'char', 0)
            if char > 0 and hasattr(K, 'order'):
                q = K.order
                if q < 1000:
                    conc = False
                    for a in range(q):
                        if Poly(x**n_int - a, x, domain=K).is_irreducible:
                            conc = True
                            break
                else:
                    conc = ((q - 1) % n_int == 0)
            else:
                conc = True
    except Exception:
        conc = True
        
    neg_q = not conc
    
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: n is a positive integer such that the characteristic of K does not divide n",
    "H_3: K contains a primitive n-th root of unity",
    "¬Q: There does not exist an element a in K such that x^n - a is irreducible over K"
]

N_HYP = 3
NEG_Q_INDEX = 3