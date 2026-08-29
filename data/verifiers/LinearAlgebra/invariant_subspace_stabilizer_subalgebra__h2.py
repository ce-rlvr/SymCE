import sympy as sp
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # Allow witness to be a tuple of (dimension, W)
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], int):
            witness = witness[1]
            
        # Normalize witness to a list of lists representing vectors in W
        if isinstance(witness, sp.Matrix):
            W = [list(witness[:, i]) for i in range(witness.shape[1])]
        elif isinstance(witness, (list, tuple, set)):
            W = []
            for w in witness:
                if isinstance(w, sp.Matrix):
                    W.append(list(w))
                else:
                    W.append(list(w))
        else:
            return [False, False]
            
        if not W:
            n = 1
        else:
            n = len(W[0])
            if any(len(w) != n for w in W):
                return [False, False]
                
        H1 = True
    except Exception:
        return [False, False]
        
    try:
        # Convert all elements to sympy objects for safe comparison
        W_sym = [[sp.sympify(x) for x in w] for w in W]
        W_set = set(tuple(w) for w in W_sym)
        zero = tuple(sp.sympify(0) for _ in range(n))
        
        # The set of operators leaving W invariant forms a subalgebra 
        # if and only if W is a subspace (or empty).
        # We check if W is a subspace by verifying closure under addition and scalar multiplication.
        is_sub = True
        if W_set and zero not in W_set:
            is_sub = False
        else:
            # Check closure under addition
            for w1 in W_sym:
                for w2 in W_sym:
                    w_add = tuple(a + b for a, b in zip(w1, w2))
                    if w_add not in W_set:
                        is_sub = False
                        break
                if not is_sub:
                    break
            
            # Check closure under scalar multiplication (using scalar = 2)
            if is_sub:
                for w in W_sym:
                    w_mult = tuple(2*a for a in w)
                    if w_mult not in W_set:
                        is_sub = False
                        break
                        
        neg_Q = not is_sub
    except Exception:
        neg_Q = False
        
    return [H1, neg_Q]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "¬Q: The set of linear operators leaving W invariant does not form a subalgebra"
]

N_HYP = 1
NEG_Q_INDEX = 1