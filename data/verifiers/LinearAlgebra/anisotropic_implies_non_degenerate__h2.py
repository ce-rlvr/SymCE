import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness expressions
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

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    
    A finite-dimensional bilinear space (represented by a matrix) cannot be a 
    counterexample because if det(M) == 0, there exists x != 0 such that Mx = 0, 
    which implies x^T M x = 0, meaning it cannot be anisotropic.
    Thus, any valid counterexample must be infinite-dimensional (where the map 
    V -> V* is injective but not surjective) and will likely be provided as a 
    mock object or dictionary by the caller.
    """
    # 1. Duck typing for custom objects or dictionaries (expected for infinite-dimensional spaces)
    if isinstance(witness, dict):
        if 'is_vector_space' in witness or 'is_anisotropic' in witness:
            h1 = bool(witness.get('is_vector_space', False))
            h2 = bool(witness.get('is_anisotropic', False))
            neg_q = not bool(witness.get('is_non_degenerate', True))
            return [h1, h2, neg_q]
            
    if hasattr(witness, 'is_vector_space') or hasattr(witness, 'is_anisotropic'):
        try:
            h1 = bool(getattr(witness, 'is_vector_space', False))
            h2 = bool(getattr(witness, 'is_anisotropic', False))
            neg_q = not bool(getattr(witness, 'is_non_degenerate', True))
            return [h1, h2, neg_q]
        except Exception:
            pass

    # 2. Fallback for matrix witnesses (finite-dimensional spaces)
    if hasattr(witness, 'det') and hasattr(witness, 'shape'):
        h1 = True
        try:
            neg_q = (witness.det() == 0)
        except Exception:
            neg_q = False
            
        h2 = False
        # If the matrix is degenerate (neg_q is True), it mathematically cannot be anisotropic.
        # We only attempt to verify anisotropy if it is non-degenerate.
        if not neg_q:
            try:
                sym = witness + witness.T
                if sym.is_positive_definite or sym.is_negative_definite:
                    h2 = True
            except Exception:
                pass
                
        return [h1, h2, neg_q]
        
    return [False, False, False]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "H_2: B is anisotropic",
    "¬Q: The bilinear form B is degenerate"
]

N_HYP = 2
NEG_Q_INDEX = 2