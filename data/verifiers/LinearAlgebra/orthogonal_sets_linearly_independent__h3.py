import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: V is an inner product space (witness is a set of vectors of the same dimension)
    try:
        h1 = False
        if isinstance(witness, (list, tuple)):
            if len(witness) == 0:
                h1 = True
            else:
                h1 = True
                shape = witness[0].shape
                if len(shape) != 2 or shape[1] != 1:
                    h1 = False
                for v in witness:
                    if not hasattr(v, 'shape') or v.shape != shape:
                        h1 = False
                        break
                # Check that it is a valid set (all elements are distinct)
                if h1:
                    for i in range(len(witness)):
                        for j in range(i + 1, len(witness)):
                            if witness[i] == witness[j]:
                                h1 = False
    except Exception:
        h1 = False

    # H_2: S is a set of mutually orthogonal vectors in V
    try:
        h2 = False
        if h1:
            h2 = True
            for i in range(len(witness)):
                for j in range(i + 1, len(witness)):
                    # Standard dot product for orthogonality
                    if witness[i].dot(witness[j]) != 0:
                        h2 = False
                        break
    except Exception:
        h2 = False

    # ¬Q: S is NOT linearly independent
    try:
        neg_q = False
        if h1 and len(witness) > 0:
            M = sympy.Matrix.hstack(*witness)
            # A set of vectors is linearly dependent if the rank of their matrix 
            # is strictly less than the number of vectors.
            if M.rank() < len(witness):
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is an inner product space (witness is a set of vectors)",
    "H_2: S is a set of mutually orthogonal vectors in V",
    "¬Q: S is not linearly independent"
]

N_HYP = 2
NEG_Q_INDEX = 2