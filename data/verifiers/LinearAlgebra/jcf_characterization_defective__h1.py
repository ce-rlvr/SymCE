import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: Let J be the Jordan canonical form of A",
    "¬Q: The equivalence between A being defective and J having a block of size > 1 fails"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        # Ensure the witness is a SymPy Matrix
        if not isinstance(witness, Matrix):
            witness = Matrix(witness)
        
        # A must be a square matrix to have a Jordan canonical form
        if not witness.is_square:
            return [False, False]
        
        # H1: J is the Jordan canonical form of A
        # We verify this by successfully computing the Jordan form
        P, J = witness.jordan_form()
        h1_ok = True
    except Exception:
        return [False, False]
        
    try:
        # Determine if the matrix is strictly over the Reals
        is_real_matrix = True
        for e in witness:
            if not e.is_real:
                is_real_matrix = False
                break
                
        # A matrix is defective if it does not possess a complete basis of eigenvectors 
        # in its base field. For real matrices, we check diagonalizability over R.
        if is_real_matrix:
            a_defective = not witness.is_diagonalizable(reals_only=True)
        else:
            a_defective = not witness.is_diagonalizable()
            
        # J contains a block of size > 1 if and only if J is not a diagonal matrix
        j_has_block_gt_1 = not J.is_diagonal()
        
        # ¬Q: The equivalence fails if the two conditions do not match
        neg_q_ok = bool(a_defective != j_has_block_gt_1)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]