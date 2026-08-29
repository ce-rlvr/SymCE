import sympy as sp
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture:
    "If I and J are ideals of R, then IJ = JI."
    
    The witness is expected to be a tuple (R, I, J) where R, I, and J are 
    lists of sympy.Matrix objects representing the basis of the ring R and 
    its ideals I and J over the rationals.
    """
    try:
        R, I, J = witness
        
        # A ring must not be empty (it must at least contain the zero element, 
        # which can be represented by an empty basis, but R itself as a basis 
        # for a non-trivial ring should have elements).
        if not R:
            return [False, False, False]
            
        def flatten(M):
            return list(M)
            
        def rank(B):
            if not B:
                return 0
            mat = sp.Matrix([flatten(m) for m in B])
            return mat.rank()
            
        def is_in_span(M, B):
            if not B:
                return all(x == 0 for x in flatten(M))
            return rank(B) == rank(B + [M])
            
        def span_eq(B1, B2):
            r1 = rank(B1)
            r2 = rank(B2)
            r12 = rank(B1 + B2)
            return r1 == r2 and r1 == r12

        # Check if R is a ring (closed under multiplication)
        # Addition is implicitly closed since R is given as a basis of a vector space.
        R_is_ring = all(is_in_span(r1 * r2, R) for r1 in R for r2 in R)
        
        # Check if I is an ideal of R
        I_in_R = all(is_in_span(i, R) for i in I)
        I_left_ideal = all(is_in_span(r * i, I) for r in R for i in I)
        I_right_ideal = all(is_in_span(i * r, I) for r in R for i in I)
        h1 = R_is_ring and I_in_R and I_left_ideal and I_right_ideal
        
        # Check if J is an ideal of R
        J_in_R = all(is_in_span(j, R) for j in J)
        J_left_ideal = all(is_in_span(r * j, J) for r in R for j in J)
        J_right_ideal = all(is_in_span(j * r, J) for r in R for j in J)
        h2 = R_is_ring and J_in_R and J_left_ideal and J_right_ideal
        
        # Compute the generating sets for the ideals IJ and JI
        IJ = [i * j for i in I for j in J]
        JI = [j * i for j in J for i in I]
        
        # The conclusion is IJ = JI. It fails if their spans are not equal.
        neg_q = not span_eq(IJ, JI)
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "H_2: J is an ideal of R",
    "¬Q: IJ != JI"
]

N_HYP = 2
NEG_Q_INDEX = 2