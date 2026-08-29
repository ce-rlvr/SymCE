import sympy
from sympy.matrices import MatrixBase

# Top-level setup for standard objects
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture:
    "A is unitarily diagonalizable if and only if A is normal"
    
    The true theorem (Complex Spectral Theorem) requires A to be a complex matrix.
    If the field is restricted to the reals, "unitarily diagonalizable" corresponds 
    to "orthogonally diagonalizable", which requires the matrix to be symmetric, 
    not just normal (e.g., a real rotation matrix is normal but not symmetric).
    """
    try:
        # Check if A is normal: A commutes with its conjugate transpose
        if hasattr(witness, 'H'):
            A_H = witness.H
        else:
            A_H = witness
            
        comm = witness * A_H - A_H * witness
        
        if hasattr(comm, 'is_zero_matrix') and comm.is_zero_matrix:
            normal = True
        elif comm == 0:
            normal = True
        elif hasattr(comm, 'is_zero') and comm.is_zero:
            normal = True
        else:
            try:
                comm_simp = sympy.simplify(comm)
                if hasattr(comm_simp, 'is_zero_matrix') and comm_simp.is_zero_matrix:
                    normal = True
                elif comm_simp == 0:
                    normal = True
                elif hasattr(comm_simp, 'is_zero') and comm_simp.is_zero:
                    normal = True
                else:
                    normal = False
            except Exception:
                normal = False
    except Exception:
        normal = False

    try:
        # Check if A is unitarily diagonalizable over its respective field
        if isinstance(witness, MatrixBase):
            if not witness.is_square:
                diag = False
            else:
                # Check if the matrix is strictly real
                is_real_matrix = True
                for e in witness:
                    if getattr(e, 'is_real', None) is not True:
                        is_real_matrix = False
                        break
                
                if is_real_matrix:
                    # For real matrices, unitarily diagonalizable over R means orthogonally diagonalizable.
                    # A real matrix is orthogonally diagonalizable if and only if it is symmetric.
                    diag = witness.is_symmetric()
                else:
                    # For complex matrices, the Spectral Theorem holds: normal implies unitarily diagonalizable.
                    diag = normal
        else:
            # For scalars or other commutative objects
            if hasattr(witness, 'is_commutative') and witness.is_commutative:
                diag = True
            else:
                diag = False
    except Exception:
        diag = False

    # The conjecture claims normal == unitarily_diagonalizable.
    # The negated conclusion is True when this equivalence fails.
    neg_q = (normal != diag)
    
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: A is normal but not unitarily diagonalizable (or vice versa)"
]

N_HYP = 0
NEG_Q_INDEX = 0