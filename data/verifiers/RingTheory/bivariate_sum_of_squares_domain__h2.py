import sympy
from sympy import symbols, Poly, QQ, CC, RR, GF

x, y = symbols('x y')

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            F = witness['F']
            I_gens = witness.get('I', [x**2 + y**2])
        elif isinstance(witness, tuple) and len(witness) == 2:
            F, I_gens = witness
        else:
            F = witness
            I_gens = [x**2 + y**2]
            
        if not isinstance(I_gens, (list, tuple)):
            I_gens = [I_gens]
    except Exception:
        return [False, False]
        
    try:
        is_field = F.is_Field
        char = F.characteristic()
        h1 = bool(is_field and char != 2)
    except Exception:
        h1 = False
        
    try:
        if hasattr(F, 'characteristic') and F.characteristic() == 2:
            has_sqrt = True
        elif F == QQ:
            has_sqrt = False
        elif F == CC:
            has_sqrt = True
        elif F == RR:
            has_sqrt = False
        elif hasattr(F, 'order'):
            has_sqrt = (F.order % 4) == 1
        else:
            poly_sqrt = Poly(x**2 + 1, x, domain=F)
            has_sqrt = not poly_sqrt.is_irreducible
            
        Q = not has_sqrt
        
        if len(I_gens) == 0:
            P = True
        elif len(I_gens) == 1:
            f = I_gens[0]
            poly = Poly(f, x, y, domain=F)
            if poly.is_zero:
                P = True
            elif poly.total_degree() == 0:
                P = False
            elif poly.total_degree() == 1:
                P = True
            else:
                P = poly.is_irreducible
        else:
            P = False
            
        neg_Q = bool(P != Q)
    except Exception:
        neg_Q = False
        
    return [h1, neg_Q]

CONDITION_LABELS = [
    "H_1: Let F be a field of characteristic not equal to 2.",
    "¬Q: The factor ring over F modulo I is an integral domain iff there is no element a in F such that a^2 = -1 fails."
]

N_HYP = 1
NEG_Q_INDEX = 1