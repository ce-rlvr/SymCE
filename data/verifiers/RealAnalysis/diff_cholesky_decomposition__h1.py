import sympy
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings that the witness expression may reference
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Evaluates the hypotheses and the negated conclusion at the given witness.
    The conjecture claims that the Cholesky decomposition map f is continuously 
    differentiable on S_{++}^n. However, if the ambient space is taken to be all 
    n x n matrices (R^{n x n}), S_{++}^n has empty interior for n > 1, meaning 
    f cannot be differentiable in the standard Frechet sense without restricting 
    the domain to the subspace of symmetric matrices. For n = 1, S_{++}^1 is open 
    in R^{1 x 1}, so it is differentiable.
    
    The witness can be either the dimension `n` or a specific matrix `A` in S_{++}^n.
    """
    try:
        # If witness is provided as a list of lists, convert to sympy Matrix
        if isinstance(witness, list):
            witness = Matrix(witness)
            
        # Case 1: witness is the dimension n
        if isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
            if n < 1:
                return [False, False, False]
            
            h1 = True
            h2 = True
            # The conclusion fails (is not continuously differentiable in R^{n x n}) for n > 1
            neg_q = (n > 1)
            return [h1, h2, neg_q]
        
        # Case 2: witness is a matrix A
        elif hasattr(witness, 'is_square') and witness.is_square:
            n = witness.shape[0]
            if n < 1:
                return [False, False, False]
            
            h1 = True
            
            # Check H2: A has a unique Cholesky factor in L_n
            # This is true iff A is symmetric positive definite
            if not witness.is_symmetric():
                h2 = False
            else:
                h2 = True
                # Sylvester's criterion for positive definiteness
                for i in range(1, n + 1):
                    minor = witness[:i, :i].det()
                    try:
                        val = float(minor)
                        if val <= 0:
                            h2 = False
                            break
                    except Exception:
                        h2 = False
                        break
            
            # The conclusion fails for n > 1
            neg_q = (n > 1)
            return [h1, h2, neg_q]
            
        else:
            return [False, False, False]
            
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: L_n is the set of n x n lower triangular real matrices with strictly positive diagonal entries",
    "H_2: f: S_{++}^n -> L_n maps a matrix A to its unique Cholesky factor L such that A = LL^T",
    "¬Q: The function f is not continuously differentiable on S_{++}^n"
]

N_HYP = 2
NEG_Q_INDEX = 2