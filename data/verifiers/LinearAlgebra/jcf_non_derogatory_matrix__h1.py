import sympy
from sympy import Matrix, eye, zeros, MatrixBase
from sympy.abc import x

# Top-level setup for Linear Algebra
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    try:
        # The witness must be a matrix
        if not isinstance(witness, MatrixBase):
            return [False, False]
    except Exception:
        return [False, False]

    def check_H1(A):
        try:
            # If A is not square, it has no eigenvalues, so "every eigenvalue..." is vacuously true.
            if not A.is_square:
                return True
            
            evs = A.eigenvects()
            for val, alg_mult, vects in evs:
                if len(vects) != 1:
                    return False
            return True
        except Exception:
            return False

    def check_Q(A):
        try:
            # A non-square matrix does not have a Jordan form or characteristic polynomial
            if not A.is_square:
                return False
            
            # A 0x0 matrix vacuously satisfies the conclusion
            if A.shape == (0, 0):
                return True
                
            # Check if minimal polynomial equals characteristic polynomial
            min_poly = A.minpoly(x)
            char_poly = A.charpoly(x).as_expr()
            if sympy.expand(min_poly - char_poly) != 0:
                return False
                
            # Check if Jordan canonical form contains exactly one block per distinct eigenvalue
            P, J = A.jordan_form()
            evs = A.eigenvals()
            num_distinct_evs = len(evs)
            
            n = A.shape[0]
            num_blocks = 0
            i = 0
            while i < n:
                num_blocks += 1
                k = 1
                # A Jordan block continues as long as the diagonal is the same and superdiagonal is 1
                while i + k < n and J[i+k, i+k] == J[i, i] and J[i+k-1, i+k] == 1:
                    k += 1
                i += k
                
            if num_blocks != num_distinct_evs:
                return False
                
            return True
        except Exception:
            return False

    h1_ok = check_H1(witness)
    q_ok = check_Q(witness)
    
    return [h1_ok, not q_ok]

CONDITION_LABELS = [
    "H_1: The geometric multiplicity of every eigenvalue of A is exactly 1",
    "¬Q: The Jordan canonical form of A does not contain exactly one Jordan block for each distinct eigenvalue, or the minimal polynomial of A is not equal to its characteristic polynomial"
]

N_HYP = 1
NEG_Q_INDEX = 1