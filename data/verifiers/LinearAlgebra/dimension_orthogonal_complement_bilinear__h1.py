import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

CONDITION_LABELS = [
    "H_1: B is a non-degenerate bilinear form on V",
    "H_2: W is a subspace of V",
    "¬Q: dim(W) + dim(W^perp) != dim(V)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    # 1. Try dictionary representation
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get('B_non_degenerate', witness.get('h1', False)))
            h2 = bool(witness.get('W_is_subspace', witness.get('h2', False)))
            if 'dim_V' in witness and 'dim_W' in witness and 'dim_W_perp' in witness:
                neg_q = (witness['dim_W'] + witness['dim_W_perp'] != witness['dim_V'])
            else:
                neg_q = bool(witness.get('neg_q', False))
            return [h1, h2, neg_q]
        except Exception:
            pass

    # 2. Try object with attributes/methods (for infinite-dimensional custom objects)
    try:
        if hasattr(witness, 'B_is_non_degenerate'):
            h1 = witness.B_is_non_degenerate()
        elif hasattr(witness, 'is_non_degenerate'):
            h1 = witness.is_non_degenerate()
        elif hasattr(witness, 'h1'):
            h1 = witness.h1() if callable(witness.h1) else witness.h1
            
        if hasattr(witness, 'W_is_subspace'):
            h2 = witness.W_is_subspace()
        elif hasattr(witness, 'is_subspace'):
            h2 = witness.is_subspace()
        elif hasattr(witness, 'h2'):
            h2 = witness.h2() if callable(witness.h2) else witness.h2
            
        if hasattr(witness, 'dim_V') and hasattr(witness, 'dim_W') and hasattr(witness, 'dim_W_perp'):
            dim_V = witness.dim_V() if callable(witness.dim_V) else witness.dim_V
            dim_W = witness.dim_W() if callable(witness.dim_W) else witness.dim_W
            dim_W_perp = witness.dim_W_perp() if callable(witness.dim_W_perp) else witness.dim_W_perp
            neg_q = (dim_W + dim_W_perp != dim_V)
        elif hasattr(witness, 'neg_q'):
            neg_q = witness.neg_q() if callable(witness.neg_q) else witness.neg_q
            
        if h1 or h2 or neg_q:
            return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    # 3. Try tuple of matrices (B, W) for finite-dimensional spaces
    # Note: The theorem is always true for finite-dimensional spaces, so neg_q will correctly evaluate to False.
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            B, W_in = witness
            if hasattr(B, 'shape') and hasattr(B, 'det'):
                if not hasattr(W_in, 'shape'):
                    W = Matrix(W_in)
                else:
                    W = W_in
                
                n = B.shape[0]
                if W.shape[0] != n and W.shape[1] == n:
                    W = W.T
                    
                h1 = False
                if B.shape[0] == B.shape[1]:
                    try:
                        h1 = (B.det() != 0)
                    except Exception:
                        pass
                        
                h2 = (W.shape[0] == n)
                
                dim_V = n
                dim_W = W.rank()
                
                # W^perp is the nullspace of W^T * B
                W_perp_matrix = W.T * B
                dim_W_perp = n - W_perp_matrix.rank()
                
                neg_q = (dim_W + dim_W_perp != dim_V)
                return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    return [False, False, False]