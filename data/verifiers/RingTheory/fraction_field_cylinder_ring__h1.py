import sympy
from sympy import Poly, Symbol
from sympy.abc import x, y, z
from sympy import ZZ, QQ

CONDITION_LABELS = [
    "H_1: f(x) is an irreducible polynomial",
    "not Q: The factor ring is not an integral domain or its field of fractions is not isomorphic to E(y)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                domain, expr = witness
                if hasattr(expr, 'free_symbols') and expr.free_symbols:
                    free = sorted(expr.free_symbols, key=lambda s: s.name)
                    gen = free[0]
                else:
                    gen = Symbol('x')
                f = Poly(expr, gen, domain=domain)
            else:
                return [False, False]
        elif isinstance(witness, Poly):
            f = witness
        else:
            if hasattr(witness, 'free_symbols') and witness.free_symbols:
                free = sorted(witness.free_symbols, key=lambda s: s.name)
                gen = free[0]
            else:
                gen = Symbol('x')
            f = Poly(witness, gen)
            
        if not f.is_univariate:
            h1 = False
        else:
            h1 = f.is_irreducible
            
        # The conclusion Q states that F[x,y]/<f(x)> is an integral domain whose field 
        # of fractions is isomorphic to E(y), where E = F[x]/<f(x)>.
        # For E(y) to be a field of rational functions over E, E must be a field.
        # E is a field if and only if F is a field and f(x) is irreducible.
        # If F is not a field, E is not a field, so E(y) is not a field (or undefined),
        # meaning it cannot be isomorphic to the field of fractions of F[x,y]/<f(x)>.
        # Therefore, Q is true if and only if F is a field and f is irreducible.
        is_field = f.domain.is_Field
        q = is_field and h1
        neg_q = not q
        
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]