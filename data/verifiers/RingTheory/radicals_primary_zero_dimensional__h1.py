import sympy
from sympy import symbols

# Top-level setup
x, y, z = symbols('x y z')
Z = sympy.S.Integers
Q = sympy.S.Rationals

def conditions(witness):
    h1 = False
    neg_q = False
    
    # Try to interpret witness as an ideal in Z (represented by its integer generator)
    try:
        n = None
        if isinstance(witness, str):
            s = witness.replace('Z', '').replace('(', '').replace(')', '').replace('ideal', '').replace('<', '').replace('>', '').strip()
            if s == '':
                n = 1
            else:
                n = int(s)
        elif isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
        elif isinstance(witness, (tuple, list, set)):
            w_list = list(witness)
            if len(w_list) == 1:
                if isinstance(w_list[0], (int, sympy.Integer)):
                    n = int(w_list[0])
            elif len(w_list) == 2:
                if isinstance(w_list[0], (int, sympy.Integer)):
                    n = int(w_list[0])
        
        if n is None:
            n = int(witness) # fallback
            
        n_abs = abs(n)
        if n_abs == 1:
            h1 = False
            is_max_rad = False
        elif n_abs == 0:
            h1 = True
            is_max_rad = False
        else:
            factors = sympy.factorint(n_abs)
            h1 = (len(factors) == 1)
            rad = 1
            for p in factors:
                rad *= p
            is_max_rad = sympy.isprime(rad)
            
        neg_q = not is_max_rad
        return [h1, neg_q]
    except Exception:
        pass

    # Try to interpret witness as a principal ideal in a polynomial ring over a field
    # Format: witness = poly OR witness = (poly, [vars])
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 2 and isinstance(witness[1], (list, tuple, set)):
                f, ring_vars = witness
            else:
                if len(witness) == 1:
                    f = witness[0]
                    ring_vars = list(f.free_symbols) if isinstance(f, sympy.Expr) else []
                else:
                    return [False, False]
        elif isinstance(witness, sympy.Expr):
            f = witness
            ring_vars = list(f.free_symbols)
        else:
            raise ValueError
            
        if not isinstance(f, sympy.Expr):
            raise ValueError
            
        factors = sympy.factor_list(f)
        poly_factors = factors[1]
        
        if len(poly_factors) == 0:
            h1 = False
            is_max_rad = False
        elif len(poly_factors) == 1:
            h1 = True
            # In a polynomial ring over a field, a principal prime ideal is maximal 
            # if and only if the Krull dimension of the ring is 1.
            if len(ring_vars) == 1:
                is_max_rad = True
            else:
                is_max_rad = False
        else:
            h1 = False
            is_max_rad = False
            
        neg_q = not is_max_rad
        return [h1, neg_q]
    except Exception:
        pass

    return [False, False]

CONDITION_LABELS = [
    "H_1: Q is a primary ideal of R",
    "¬Q: The radical of Q is not a maximal ideal of R"
]

N_HYP = 1
NEG_Q_INDEX = 1