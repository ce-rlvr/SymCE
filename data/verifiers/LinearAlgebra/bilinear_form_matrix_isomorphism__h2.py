import math
import sympy
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # Extract dimensions from the witness
        if isinstance(witness, dict):
            n = witness['n']
            m = witness['m']
            dim_W = witness.get('dim_W', math.inf)
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 2:
                n, m = witness
                dim_W = math.inf
            else:
                n, m, dim_W = witness[0], witness[1], witness[2]
        else:
            n = getattr(witness, 'n')
            m = getattr(witness, 'm')
            dim_W = getattr(witness, 'dim_W', math.inf)
            
        # Handle string representations of infinity
        if isinstance(dim_W, str):
            if dim_W.lower() in ['inf', 'infinity', 'oo']:
                dim_W = math.inf
            else:
                dim_W = float(dim_W)
                
        # H_1: V is a finite-dimensional vector space over a field F of dimension n
        h1 = isinstance(n, int) and n >= 0
        
        # Conclusion: The vector space of all bilinear forms from V x W to F 
        # is isomorphic to the vector space of n by m matrices over F.
        # Two vector spaces over F are isomorphic iff their dimensions are equal.
        if not (isinstance(m, int) and m >= 0):
            # If m is not a valid matrix dimension, the space of n by m matrices is undefined,
            # so the isomorphism conclusion trivially fails.
            neg_q = True
        else:
            if n == 0:
                # If V is 0-dimensional, any bilinear form is trivial (dimension 0).
                # The space of 0 by m matrices is also 0-dimensional.
                dim_bilin = 0
                dim_matrices = 0
            else:
                # Dimension of Bilin(V, W; F) is dim(V) * dim(W)
                dim_bilin = n * dim_W
                # Dimension of M_{n,m}(F) is n * m
                dim_matrices = n * m
                
            q = (dim_bilin == dim_matrices)
            neg_q = not q
            
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F of dimension n",
    "¬Q: The vector space of bilinear forms is not isomorphic to n by m matrices"
]

N_HYP = 1
NEG_Q_INDEX = 1