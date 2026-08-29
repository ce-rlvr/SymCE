import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

# Standard linear algebra objects for witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Let R be a ring, M a Noetherian R-module, and f: M -> M an R-module homomorphism. 
    Then f is an isomorphism."
    
    A valid witness is represented as a square sympy.Matrix, which corresponds to 
    an endomorphism of a finite-dimensional vector space (over Q) or a finitely 
    generated free module (over Z), both of which are Noetherian modules.
    """
    try:
        # Extract matrix if witness is a dictionary, otherwise assume it's the matrix itself
        if isinstance(witness, dict):
            mat = witness.get("matrix", witness)
        else:
            mat = witness
            
        # H_1: R is a ring. 
        # We implicitly satisfy this by requiring the witness to be a matrix over a ring (Z or Q).
        h1 = isinstance(mat, sympy.Matrix)
    except Exception:
        h1 = False

    try:
        # H_2: M is a Noetherian R-module.
        # A finite-dimensional vector space or finitely generated Z-module is Noetherian.
        # We require the matrix to be square to represent an endomorphism M -> M.
        h2 = h1 and mat.is_square
    except Exception:
        h2 = False

    try:
        # ¬Q: The homomorphism f is NOT an isomorphism.
        if not h2:
            neg_q = False
        else:
            det = mat.det()
            if det == 0:
                # Determinant 0 means it's not an isomorphism over any integral domain
                neg_q = True
            else:
                # If all entries are integers, we treat it as an endomorphism over Z.
                # Over Z, it is an isomorphism if and only if the determinant is 1 or -1.
                is_int_mat = all(isinstance(val, (int, sympy.Integer)) for val in mat)
                if is_int_mat and abs(det) != 1:
                    neg_q = True
                else:
                    neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: M is a Noetherian R-module",
    "¬Q: The homomorphism f is not an isomorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2