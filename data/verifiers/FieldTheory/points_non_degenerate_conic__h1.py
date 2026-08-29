import sympy
import math

# Top-level setup
# No special named groups are required for this field theory conjecture.
# We define standard matrices that might be used as witnesses.
I3 = sympy.eye(3)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Evaluates the remaining hypotheses and the negated conclusion for the conjecture:
    'The number of F-rational points on a non-degenerate conic C is exactly q + 1'
    
    The witness is expected to be a tuple (q, M) where:
      - q is an integer representing the size of the field/ring.
      - M is a 3x3 symmetric matrix representing the conic.
    """
    try:
        q, M_data = witness
        M = sympy.Matrix(M_data)
    except Exception:
        return [False, False, False]

    # H_1: C is a projective conic curve defined by a homogeneous polynomial of degree 2 
    # in three variables over F.
    # We verify that M is a 3x3 symmetric matrix and q is a valid size (>= 2).
    try:
        h1 = (M.shape == (3, 3)) and (M == M.T) and isinstance(q, int) and (q >= 2)
    except Exception:
        h1 = False

    # H_2: The conic C is non-degenerate, meaning its associated symmetric matrix 
    # has non-zero determinant.
    try:
        h2 = (M.det() % q) != 0
    except Exception:
        h2 = False

    # ¬Q: The number of F-rational points on the conic C is NOT exactly q + 1.
    # We count the number of projective points (x:y:z) over Z/qZ such that X^T M X = 0 mod q.
    try:
        valid_triples = 0
        for x in range(q):
            for y in range(q):
                for z in range(q):
                    # A valid projective point must not be the zero vector, and its coordinates
                    # must not all share a common factor with q (to be a primitive point).
                    if math.gcd(math.gcd(x, y), math.gcd(z, q)) == 1:
                        v = sympy.Matrix([x, y, z])
                        val = (v.T * M * v)[0]
                        if val % q == 0:
                            valid_triples += 1
        
        # The number of projective points is the number of valid triples divided by phi(q),
        # since scalar multiplication by any unit modulo q gives the same projective point.
        phi_q = sum(1 for i in range(1, q) if math.gcd(i, q) == 1)
        if phi_q == 0:
            phi_q = 1
            
        num_points = valid_triples // phi_q
        neg_q = (num_points != q + 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: C is a projective conic curve defined by a homogeneous polynomial of degree 2 in three variables over F",
    "H_2: The conic C is non-degenerate, meaning its associated symmetric matrix has non-zero determinant",
    "¬Q: The number of F-rational points on the conic C is not exactly q + 1"
]

N_HYP = 2
NEG_Q_INDEX = 2