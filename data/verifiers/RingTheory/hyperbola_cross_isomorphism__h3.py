import sympy as sp

x, y, u, v = sp.symbols('x y u v')

def conditions(witness):
    char = 0
    if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], int):
        char = witness[0]
        I_obj = witness[1]
    else:
        I_obj = witness

    try:
        if char == 0:
            h1 = True
        elif char > 0 and sp.isprime(char) and char != 2:
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if isinstance(I_obj, (list, tuple)):
            h2 = all(isinstance(p, sp.Expr) and p.free_symbols.issubset({x, y}) and p.is_polynomial(x, y) for p in I_obj)
            if len(I_obj) == 0:
                h2 = False
        else:
            h2 = isinstance(I_obj, sp.Expr) and I_obj.free_symbols.issubset({x, y}) and I_obj.is_polynomial(x, y)
    except Exception:
        h2 = False

    try:
        if isinstance(I_obj, (list, tuple)) and len(I_obj) != 1:
            neg_q = True
        else:
            poly = I_obj[0] if isinstance(I_obj, (list, tuple)) else I_obj
            
            if not isinstance(poly, sp.Expr):
                neg_q = True
            else:
                kwargs = {}
                if char > 0:
                    kwargs['modulus'] = char
                
                factors = sp.factor_list(poly, **kwargs)
                
                if len(factors[1]) != 2:
                    neg_q = True
                else:
                    (P1, m1), (P2, m2) = factors[1]
                    if m1 != 1 or m2 != 1:
                        neg_q = True
                    else:
                        J_det = sp.diff(P1, x)*sp.diff(P2, y) - sp.diff(P1, y)*sp.diff(P2, x)
                        J_det = sp.expand(J_det)
                        
                        if char > 0:
                            J_det = sp.Poly(J_det, x, y, modulus=char).as_expr()
                            
                        if not J_det.is_constant() or J_det == 0:
                            neg_q = True
                        else:
                            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field of characteristic not equal to 2",
    "H_2: I is an ideal in R",
    "¬Q: R mod I is not isomorphic to S mod uv"
]

N_HYP = 2
NEG_Q_INDEX = 2