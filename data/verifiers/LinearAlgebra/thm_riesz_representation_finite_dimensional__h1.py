import sympy as sp
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    h1 = False
    neg_q = False
    
    G = None
    
    try:
        # The witness can be either a single Gram matrix G (assuming f is the zero functional),
        # or a tuple (G, F) where G is the Gram matrix of the bilinear form and F is the 
        # column vector (or callable) representing the linear functional.
        if hasattr(witness, 'is_square') and witness.is_square:
            G = witness
            h1 = True
        elif isinstance(witness, (list, tuple)) and len(witness) == 2:
            G_cand, F_cand = witness
            if hasattr(G_cand, 'is_square') and G_cand.is_square:
                n = G_cand.shape[0]
                if hasattr(F_cand, 'shape') and F_cand.shape == (n, 1):
                    G = G_cand
                    h1 = True
                elif callable(F_cand):
                    G = G_cand
                    h1 = True
    except Exception:
        pass

    try:
        if h1 and G is not None:
            # The conclusion states there is a UNIQUE u such that f(v) = <v, u> for all v.
            # In matrix form, this is F^T v = v^T G u for all v, which implies G u = F.
            # A unique solution u exists if and only if G is invertible (det(G) != 0).
            # Therefore, the conclusion fails (neg_q is True) iff det(G) == 0.
            det_G = G.det()
            if det_G == 0 or det_G is sp.S.Zero:
                neg_q = True
            else:
                neg_q = bool(sp.simplify(det_G) == 0)
    except Exception:
        pass

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: f is a linear functional on V",
    "¬Q: There does not exist a unique vector u in V such that f(v) = ⟨v, u⟩ for all v in V"
]

N_HYP = 1
NEG_Q_INDEX = 1