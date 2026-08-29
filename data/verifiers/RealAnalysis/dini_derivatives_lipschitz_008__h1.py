import sympy
from sympy import Symbol, limit, oo, zoo, nan, Abs, Piecewise
from sympy.abc import x, y, z, t
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should provide the function f, interval bounds a and b, point x, and bound L.
    It can be a dictionary with keys 'f', 'a', 'b', 'x', 'L' or a tuple (f, a, b, x, L).
    """
    try:
        if isinstance(witness, dict):
            f = witness.get('f')
            a = witness.get('a')
            b = witness.get('b')
            x0 = witness.get('x')
            L = witness.get('L')
        else:
            f, a, b, x0, L = witness
            
        f = sympy.sympify(f)
        a = sympy.sympify(a)
        b = sympy.sympify(b)
        x0 = sympy.sympify(x0)
        L = sympy.sympify(L)
        
        # H_1: x is in (a, b)
        try:
            h1 = bool(a < x0) and bool(x0 < b)
        except Exception:
            h1 = False
            
        # neg_Q: At least one Dini derivative of f at x is NOT bounded in absolute value by L
        neg_q = False
        try:
            free = f.free_symbols
            if len(free) == 1:
                var = list(free)[0]
            else:
                var = x
                
            h = Symbol('h')
            dini_derivs = []
            
            # Compute right and left limits of the difference quotient
            for direction in ['+', '-']:
                dq = (f.subs(var, x0 + h) - f.subs(var, x0)) / h
                res = limit(dq, h, 0, dir=direction)
                
                # If the limit doesn't exist but is bounded, sympy returns AccumBounds
                if hasattr(res, 'is_AccumBounds') and res.is_AccumBounds:
                    dini_derivs.extend([res.min, res.max])
                else:
                    dini_derivs.extend([res, res])
                    
            # Check if any Dini derivative exceeds L in absolute value or is unbounded
            for d in dini_derivs:
                if d in (oo, -oo, zoo, nan):
                    neg_q = True
                    break
                if hasattr(d, 'has') and d.has(oo, -oo, zoo, nan):
                    neg_q = True
                    break
                if bool(Abs(d) > L):
                    neg_q = True
                    break
        except Exception:
            neg_q = False
            
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: x is in (a, b)",
    "¬Q: At least one Dini derivative of f at x is not bounded in absolute value by L"
]

N_HYP = 1
NEG_Q_INDEX = 1