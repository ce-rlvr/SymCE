import sympy
from sympy import Symbol, limit, oo, Abs
import math
import itertools
import functools

# Top-level setup
n = Symbol('n', integer=True, positive=True)
x = Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        # If the witness is a finite sequence, the remaining coefficients are 0,
        # so the radius of convergence is infinity.
        if isinstance(witness, (list, tuple)):
            R = oo
            neg_q = (sympy.simplify(R - 1) != 0)
            return [bool(neg_q)]
            
        if callable(witness):
            expr = witness(n)
        else:
            expr = witness
            
        # Try root test to find limsup |a_n|^(1/n)
        L = limit(Abs(expr)**(1/n), n, oo)
        if type(L).__name__ == 'AccumBounds':
            L = L.max
            
        if not L.has(sympy.limit):
            if L == 0:
                R = oo
            elif L == oo:
                R = 0
            else:
                R = 1 / L
        else:
            # Fallback to ratio test if root test limit is unevaluated
            L2 = limit(Abs(expr.subs(n, n+1) / expr), n, oo)
            if type(L2).__name__ == 'AccumBounds':
                L2 = L2.max
                
            if not L2.has(sympy.limit):
                if L2 == 0:
                    R = oo
                elif L2 == oo:
                    R = 0
                else:
                    R = 1 / L2
            else:
                # Could not compute the radius of convergence
                return [False]
                
        neg_q = (sympy.simplify(R - 1) != 0)
    except Exception:
        neg_q = False
        
    return [bool(neg_q)]

CONDITION_LABELS = [
    "¬Q: The radius of convergence of the power series is not equal to 1"
]

N_HYP = 0
NEG_Q_INDEX = 0