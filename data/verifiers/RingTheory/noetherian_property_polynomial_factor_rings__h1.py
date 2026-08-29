import sympy
from sympy import Symbol

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

class NonNoetherianRing:
    """
    A mock representation of a non-Noetherian ring, 
    e.g., a polynomial ring in infinitely many variables.
    Provided for convenience so the witness can easily reference it.
    """
    def __init__(self, name="k[x_1, x_2, ...]"):
        self.name = name
        self.is_noetherian = False
        self.is_Noetherian = False

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

R_inf = NonNoetherianRing("k[x_1, x_2, ...]")

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    def is_non_noetherian(R):
        if hasattr(R, 'is_noetherian') and not R.is_noetherian:
            return True
        if hasattr(R, 'is_Noetherian') and not R.is_Noetherian:
            return True
        s = str(R).lower()
        if '...' in s or 'infty' in s or 'infinity' in s or 'infinite' in s:
            return True
        if 'continuous' in s:
            return True
        if 'algebraic integer' in s:
            return True
        return False

    try:
        # Parse the witness
        if isinstance(witness, dict):
            R = witness.get('R', '')
            f = witness.get('f', '')
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, f = witness
        elif isinstance(witness, str):
            s = witness.lower()
            h1 = 'f' in s or 'x' in s
            is_unit = 'f(x) = 1' in s or 'f = 1' in s or 'f(x)=1' in s or 'f=1' in s
            if is_non_noetherian(witness):
                neg_q = not is_unit
            return [h1, neg_q]
        else:
            R = getattr(witness, 'R', '')
            f = getattr(witness, 'f', '')
            if not R and not f:
                return [False, False]
                
        # Check H1: f(x) is a polynomial
        if isinstance(f, str):
            try:
                f_str = f.replace('^', '**')
                f_expr = sympy.sympify(f_str)
                h1 = isinstance(f_expr, (sympy.Expr, sympy.Poly, int))
            except Exception:
                h1 = len(f.strip()) > 0
        else:
            h1 = isinstance(f, (sympy.Expr, sympy.Poly, int))
            
        # Check ¬Q: The factor ring is NOT a Noetherian ring
        # This happens if R is non-Noetherian and f(x) is not a unit (e.g., not 1 or -1)
        if is_non_noetherian(R):
            if isinstance(f, str):
                try:
                    f_str = f.replace('^', '**')
                    f_expr = sympy.sympify(f_str)
                    is_unit = f_expr in [1, -1, sympy.S.One, sympy.S.NegativeOne]
                except Exception:
                    is_unit = f.strip() in ['1', '-1']
            else:
                if isinstance(f, sympy.Poly):
                    f_expr = f.as_expr()
                else:
                    f_expr = f
                is_unit = f_expr in [1, -1, sympy.S.One, sympy.S.NegativeOne]
            
            neg_q = not is_unit
            
    except Exception:
        pass
        
    return [h1, neg_q]

# Note: Avoided using square brackets inside the strings to prevent regex parsing issues in the validator.
CONDITION_LABELS = [
    "H_1: f(x) is a polynomial",
    "¬Q: The factor ring is not a Noetherian ring"
]

N_HYP = 1
NEG_Q_INDEX = 1