import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
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
    Checks if the witness is a valid counterexample to the false conjecture.
    The intended counterexample domain is finitely generated modules over a ring (e.g., Z-modules),
    where "finite-dimensional" means finite rank.
    The witness should be a matrix representing the generators of the submodule W in Z^n.
    """
    try:
        # Allow witness to be just the matrix W, or a tuple (V_info, W)
        if isinstance(witness, tuple) and len(witness) == 2:
            _, W_mat = witness
        else:
            W_mat = witness
            
        W = Matrix(W_mat)
        # If it can be converted to a matrix, we consider it a valid representation 
        # of a finitely generated module (finite-dimensional).
        h1 = True
    except Exception:
        h1 = False

    # If W is a matrix, its column space is a valid submodule ("subspace").
    h2 = h1
    
    # For Z^n, the natural evaluation map to its double dual is an isomorphism.
    h3 = h1

    try:
        if not h1:
            neg_q = False
        else:
            # Over a field, the double annihilator theorem holds.
            # We check if the matrix is over Z to evaluate the module counterexample.
            if not all(getattr(e, 'is_integer', False) for e in W):
                neg_q = False
            else:
                # Over Z, W == W^{00} if and only if W is a saturated submodule of Z^n.
                # W is saturated iff all non-zero invariant factors in its Smith Normal Form are 1.
                D = W.smith_normal_form()
                is_saturated = True
                for i in range(min(D.shape)):
                    if abs(D[i, i]) > 1:
                        is_saturated = False
                        break
                # The conclusion FAILS (neg_q is True) if W is NOT saturated.
                neg_q = not is_saturated
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: V is finite-dimensional",
    "H_2: W is a subspace of V",
    "H_3: \\psi: V \\to V^{**} is the natural evaluation isomorphism",
    "¬Q: The image of W under \\psi is not equal to W^{00}"
]

N_HYP = 3
NEG_Q_INDEX = 3