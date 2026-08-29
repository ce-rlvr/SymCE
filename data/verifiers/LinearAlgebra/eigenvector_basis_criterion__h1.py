import sympy as sp
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: T is a linear operator from V to V",
    "¬Q: The equivalence between T being diagonalizable and having a basis of eigenvectors fails"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    """
    Given a witness object, checks whether it is a valid counterexample to the false conjecture.
    Returns a list of booleans: [H_1_ok, neg_Q_ok].
    """
    try:
        # H_1: T is a linear operator from V to V
        # A square matrix represents a linear operator on a finite-dimensional vector space.
        # We also allow custom objects that represent linear operators.
        h1 = hasattr(witness, 'is_square') and witness.is_square
        if not h1:
            h1 = hasattr(witness, 'is_diagonalizable')
    except Exception:
        h1 = False

    try:
        # ¬Q: T is diagonalizable if and only if there exists a basis of V consisting entirely of eigenvectors of T
        # The conjecture is false because a matrix might be diagonalizable over the algebraic closure (e.g., C),
        # but lack a basis of eigenvectors over its base field (e.g., R).
        if hasattr(witness, 'is_square') and witness.is_square:
            # Check if the matrix is strictly over the reals
            is_real_matrix = all(getattr(e, 'is_real', False) == True for e in witness)
            
            # SymPy's is_diagonalizable() checks diagonalizability over C by default
            is_diag = witness.is_diagonalizable()
            
            # Count the geometric multiplicity of eigenvectors in the base field
            geom_mult = 0
            for val, mult, vects in witness.eigenvects():
                if is_real_matrix:
                    # For a real vector space V, eigenvectors must have real eigenvalues to be in V
                    if getattr(val, 'is_real', False) == True:
                        geom_mult += len(vects)
                else:
                    geom_mult += len(vects)
                    
            has_basis = (geom_mult == witness.shape[0])
            
            # The conclusion holds if both are true or both are false
            q = (is_diag == has_basis)
            neg_q = not q
        else:
            # Fallback for custom infinite-dimensional operator objects
            is_diag = getattr(witness, 'is_diagonalizable', False)
            if callable(is_diag): 
                is_diag = is_diag()
            
            has_basis = getattr(witness, 'has_basis_of_eigenvectors', False)
            if callable(has_basis): 
                has_basis = has_basis()
            
            q = (is_diag == has_basis)
            neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]