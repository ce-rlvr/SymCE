import sympy as sp
import itertools

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def is_psd(M):
    if M != M.H:
        if sp.expand(M - M.H) != sp.zeros(*M.shape):
            return False
    n = M.shape[0]
    for k in range(1, n + 1):
        for indices in itertools.combinations(range(n), k):
            subM = M.extract(indices, indices)
            det_val = sp.expand(subM.det())
            try:
                if bool(det_val < 0):
                    return False
            except TypeError:
                try:
                    if bool(sp.re(det_val).evalf() < 0):
                        return False
                except Exception:
                    return False
    return True

def conditions(witness):
    try:
        h1 = isinstance(witness, sp.MatrixBase) and witness.is_square
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            n = witness.shape[0]
            is_proj = (witness ** 2 == witness)
            is_self_adjoint = (witness == witness.H)
            A = is_proj and is_self_adjoint
            
            I = sp.eye(n)
            M = I - witness.H * witness
            B = is_psd(M)
            
            neg_q = bool(A != B)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: V is an inner product space (witness is a square matrix)",
    "¬Q: The equivalence 'P is an orthogonal projection iff ||Px|| <= ||x|| for all x' fails"
]

N_HYP = 1
NEG_Q_INDEX = 1