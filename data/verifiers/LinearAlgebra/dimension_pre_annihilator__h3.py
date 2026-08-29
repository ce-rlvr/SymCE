import sympy
from sympy import Matrix, eye, zeros, Mod
from sympy.abc import x, y, z
from sympy.ntheory import isprime

# Top-level setup for Linear Algebra
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: U is a subspace of the dual space V^*",
    "¬Q: dim(^0U) != dim(V) - dim(U)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        V_dim = None
        U = None
        
        # Parse the witness
        if isinstance(witness, tuple) and len(witness) == 2:
            V_dim, U = witness
            if isinstance(U, list):
                U = Matrix(U)
            elif not hasattr(U, 'cols') and hasattr(U, 'shape'):
                U = Matrix(U)
        elif isinstance(witness, list):
            U = Matrix(witness)
            V_dim = U.cols
        else:
            U = witness
            if not hasattr(U, 'cols') and hasattr(U, 'shape'):
                U = Matrix(U)
            V_dim = U.cols
            
        if not hasattr(U, 'cols') or not hasattr(U, 'rows'):
            return [False, False, False]
            
        if V_dim != U.cols:
            return [False, False, False]
            
        # H1: V is a finite-dimensional vector space over a field F
        # We verify that the matrix elements do not belong to a composite modulo ring
        h1 = True
        for e in U:
            if isinstance(e, Mod):
                if not isprime(e.args[1]):
                    h1 = False
                    break
                    
        # H2: U is a subspace of the dual space V^*
        # Any matrix represents a subspace of V^* spanned by its row vectors
        h2 = True
        
        # Conclusion: dim(^0U) = dim(V) - dim(U)
        # The pre-annihilator ^0U corresponds to the nullspace of the matrix U
        dim_V = int(V_dim)
        dim_U = int(U.rank())
        dim_pre_annihilator = int(len(U.nullspace()))
        
        # neg_Q is True if the conclusion FAILS
        neg_q = not (dim_pre_annihilator == dim_V - dim_U)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]