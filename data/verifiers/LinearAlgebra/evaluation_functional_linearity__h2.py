import sympy as sp
from sympy import eye, zeros

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (n, v) where:
      - n is the dimension of the vector space V = F^n
      - v is the object used to define the evaluation map E_v
    """
    try:
        n, v = witness
    except Exception:
        return [False, False]
        
    # H_1: V is a vector space over a field F
    # We represent V as F^n, so n must be a non-negative integer.
    try:
        h1 = bool(int(n) == n and n >= 0)
    except Exception:
        h1 = False
        
    # ¬Q: The evaluation map E_v is NOT a linear functional on V*
    # E_v is a linear functional if it maps every f in V* to a scalar in F,
    # and satisfies E_v(c*f + g) = c*E_v(f) + E_v(g).
    try:
        if isinstance(v, (list, tuple)):
            v = sp.Matrix(v)
            
        # V* is the space of linear functionals on V, represented by 1 x n matrices.
        f_syms = [sp.Symbol(f'f_{i}') for i in range(int(n))]
        g_syms = [sp.Symbol(f'g_{i}') for i in range(int(n))]
        f = sp.Matrix([f_syms])
        g = sp.Matrix([g_syms])
        c = sp.Symbol('c')
        
        # Evaluate E_v(f) = f(v)
        if callable(v):
            fv = v(f)
            gv = v(g)
            cfgv = v(c*f + g)
        else:
            fv = f * v
            gv = g * v
            cfgv = (c*f + g) * v
            
        # Check if the result is a scalar and satisfies linearity
        if isinstance(fv, sp.Matrix):
            if fv.shape != (1, 1):
                neg_q = True
            else:
                diff = sp.simplify(cfgv - (c*fv + gv))
                if diff == sp.zeros(1, 1):
                    neg_q = False
                else:
                    neg_q = True
        else:
            diff = sp.simplify(cfgv - (c*fv + gv))
            if diff == 0:
                neg_q = False
            else:
                neg_q = True
    except Exception:
        # If f(v) is undefined or raises an error (e.g., shape mismatch),
        # E_v is not a well-defined map on V*, hence not a linear functional.
        neg_q = True
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "¬Q: The evaluation map E_v is not a linear functional on V*"
]

N_HYP = 1
NEG_Q_INDEX = 1