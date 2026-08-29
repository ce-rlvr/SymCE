import sympy
from sympy import Matrix, eye, zeros
from sympy import QQ, ZZ, RR, CC

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_ring(R):
    """Check if R is a ring."""
    if R in (QQ, ZZ, RR, CC):
        return True
    if hasattr(R, 'is_Ring') and R.is_Ring:
        return True
    if hasattr(R, 'is_ring'):
        return R.is_ring() if callable(R.is_ring) else R.is_ring
    
    # Check if R is a matrix ring (list of basis matrices)
    if isinstance(R, list) and all(isinstance(m, Matrix) for m in R):
        if not R: 
            return False
        shape = R[0].shape
        if shape[0] != shape[1]: 
            return False
        
        vecs = [m.vec() for m in R]
        M = Matrix.hstack(*vecs)
        _, pivots = M.rref()
        if not pivots:
            return False
        
        basis = [R[i] for i in pivots]
        B_mat = Matrix.hstack(*[vecs[i] for i in pivots])
        
        # Check for multiplicative identity
        I_mat = eye(shape[0])
        if B_mat.row_join(I_mat.vec()).rank() > len(pivots):
            return False
            
        # Check closure under multiplication
        for A in basis:
            for B in basis:
                AB = A * B
                if B_mat.row_join(AB.vec()).rank() > len(pivots):
                    return False
        return True
        
    return False

def is_ideal(I, R):
    """Check if I is a two-sided ideal of R."""
    if hasattr(I, 'is_ideal_of'):
        return I.is_ideal_of(R)
    if hasattr(R, 'is_ideal'):
        return R.is_ideal(I)
        
    # Check if I is an ideal of a matrix ring R
    if isinstance(R, list) and isinstance(I, list) and all(isinstance(m, Matrix) for m in R) and all(isinstance(m, Matrix) for m in I):
        if not I: 
            return True
        if not R: 
            return False
        
        vecs_R = [m.vec() for m in R]
        M_R = Matrix.hstack(*vecs_R)
        _, pivots_R = M_R.rref()
        if not pivots_R:
            return False
        basis_R = [R[i] for i in pivots_R]
        B_R_mat = Matrix.hstack(*[vecs_R[i] for i in pivots_R])
        rank_R = len(pivots_R)
        
        vecs_I = [m.vec() for m in I]
        M_I = Matrix.hstack(*vecs_I)
        _, pivots_I = M_I.rref()
        if not pivots_I:
            return True
        basis_I = [I[i] for i in pivots_I]
        B_I_mat = Matrix.hstack(*[vecs_I[i] for i in pivots_I])
        rank_I = len(pivots_I)
        
        # Check if I is a subset of R
        for i_mat in basis_I:
            if B_R_mat.row_join(i_mat.vec()).rank() > rank_R:
                return False
                
        # Check left and right ideal properties (absorption)
        for r in basis_R:
            for i in basis_I:
                ri = r * i
                if B_I_mat.row_join(ri.vec()).rank() > rank_I:
                    return False
                ir = i * r
                if B_I_mat.row_join(ir.vec()).rank() > rank_I:
                    return False
        return True
        
    # Check for standard SymPy domains
    if R in (QQ, RR, CC):
        if I == R: 
            return True
        return False
        
    if R == ZZ:
        if I == ZZ: 
            return True
        return False
        
    return False

def conditions(witness):
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness is expected to provide a ring R, a positive integer n, and a subset I.
    """
    R, n, I = None, None, None
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            n = witness.get('n')
            I = witness.get('I')
        elif isinstance(witness, tuple) and len(witness) == 3:
            R, n, I = witness
        else:
            R = getattr(witness, 'R', None)
            n = getattr(witness, 'n', None)
            I = getattr(witness, 'I', None)
    except Exception:
        pass

    # H_1: R is a ring
    h1 = False
    try:
        if hasattr(witness, 'is_ring'):
            h1 = witness.is_ring() if callable(witness.is_ring) else witness.is_ring
        elif R is not None:
            h1 = is_ring(R)
    except Exception:
        pass

    # H_2: n is a positive integer
    h2 = False
    try:
        if hasattr(witness, 'n'):
            n_val = witness.n
        elif n is not None:
            n_val = n
        else:
            n_val = None
        h2 = isinstance(n_val, int) and n_val > 0
    except Exception:
        pass

    # ¬Q: M_n(R)/M_n(I) is NOT isomorphic to M_n(R/I)
    # This happens exactly when I is not a two-sided ideal of R,
    # meaning the quotient is not a well-defined ring.
    neg_q = False
    try:
        if hasattr(witness, 'is_isomorphic'):
            iso = witness.is_isomorphic() if callable(witness.is_isomorphic) else witness.is_isomorphic
            neg_q = not iso
        elif R is not None and I is not None:
            neg_q = not is_ideal(I, R)
    except Exception:
        pass

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: n is a positive integer",
    "¬Q: M_n(R)/M_n(I) is not isomorphic to M_n(R/I)"
]

N_HYP = 2
NEG_Q_INDEX = 2