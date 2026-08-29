import sympy as sp
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for standard algebra objects
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
    Given a witness (T, v), checks if it is a valid counterexample to the conjecture.
    T is a sympy Matrix representing the linear transformation.
    v is a sympy Matrix representing the column vector.
    """
    try:
        T, v = witness
    except Exception:
        return [False, False, False, False, False]

    # H_1: GL(V) is the general linear group of V (T is invertible)
    try:
        h1 = bool(T.shape[0] == T.shape[1] and T.det() != 0)
    except Exception:
        h1 = False

    # H_2: P(V) is the projective space of V
    h2 = True

    # H_3: GL(V) acts on P(V) via T.span(u) = span(T(u))
    h3 = True

    # H_4: L is a 1-dimensional subspace spanned by non-zero v
    try:
        h4 = bool(v.shape[1] == 1 and not all(sp.simplify(v[i]) == 0 for i in range(v.shape[0])))
    except Exception:
        h4 = False

    # ¬Q: The stabilizer of L in GL(V) does not consist exactly of those linear transformations in GL(V) for which v is an eigenvector.
    # We check if T stabilizes L iff v is an eigenvector of T.
    try:
        u = T * v
        n = v.shape[0]
        
        # Check if v is an eigenvector (i.e., u is a scalar multiple of v)
        # This is true iff all 2x2 minors of [u, v] are zero.
        is_eig = True
        for i in range(n):
            for j in range(n):
                if sp.simplify(u[i]*v[j] - u[j]*v[i]) != 0:
                    is_eig = False
                    break
            if not is_eig:
                break
                
        # Check if T stabilizes L
        # T stabilizes L iff span(T(v)) == span(v)
        # Since v != 0, this means T(v) is a non-zero scalar multiple of v
        is_u_zero = all(sp.simplify(u[i]) == 0 for i in range(n))
        stabilizes = is_eig and not is_u_zero
        
        # The conclusion fails if the equivalence does not hold for this T
        neg_q = bool(stabilizes != is_eig)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: GL(V) is the general linear group of V",
    "H_2: P(V) is the projective space of V",
    "H_3: GL(V) acts on P(V) via T.span(u) = span(T(u))",
    "H_4: L is a 1-dimensional subspace spanned by non-zero v",
    "¬Q: The stabilizer of L in GL(V) does not consist exactly of those linear transformations for which v is an eigenvector"
]

N_HYP = 4
NEG_Q_INDEX = 4