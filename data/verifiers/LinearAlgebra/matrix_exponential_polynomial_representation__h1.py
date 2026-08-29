import sympy as sp
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture claims that for the given matrix A, e^A can be written as a 
    polynomial in A of degree at most n-1 with complex scalar coefficients.
    """
    try:
        # The witness can be a tuple (A, n) or just a matrix A (where n is inferred as its dimension)
        if isinstance(witness, tuple):
            A, n = witness
        else:
            A = witness
            if not hasattr(A, 'shape'):
                n = 1
                A = sp.Matrix([[A]])
            else:
                n = A.shape[0]
                
        if not isinstance(A, sp.MatrixBase):
            q_holds = False
        elif A.shape[0] != A.shape[1]:
            # Matrix exponential is undefined for non-square matrices
            q_holds = False
        else:
            eA = sp.exp(A)
            eA_vec = list(eA)
            
            vecs = []
            for k in range(n):
                Ak = A**k
                vecs.append(list(Ak))
                
            M = sp.Matrix(vecs).T
            b = sp.Matrix(eA_vec)
            
            if n == 0:
                q_holds = all(x == 0 for x in eA_vec)
            elif not A.free_symbols:
                # For constant matrices, check if b is in the column space of M
                aug = M.row_join(b)
                q_holds = (M.rank() == aug.rank())
            else:
                # For symbolic matrices, check if there exists a solution with constant coefficients
                try:
                    c, params = M.gauss_jordan_solve(b)
                    # Substitute 0 for any free parameters to get a particular solution
                    c_zero = c.subs({p: 0 for p in params})
                    # If the solution still contains free symbols from A, the coefficients are not complex scalars
                    q_holds = not bool(c_zero.free_symbols)
                except ValueError:
                    # System is inconsistent
                    q_holds = False
                    
    except Exception:
        # If any computation fails (e.g., exp(A) cannot be computed), the conclusion formula is invalid
        q_holds = False
        
    neg_q = not q_holds
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: Matrix exponential e^A cannot be written as a polynomial in A of degree n-1 with complex scalars"
]

N_HYP = 0
NEG_Q_INDEX = 0