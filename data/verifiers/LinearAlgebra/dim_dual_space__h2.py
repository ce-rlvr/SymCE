import sympy
from sympy import oo

class VectorSpace:
    """
    A simple representation of a vector space for testing purposes.
    """
    def __init__(self, dimension):
        self.dimension = dimension

    def __str__(self):
        return f"VectorSpace(dimension={self.dimension})"

# Common vector spaces
R_x = VectorSpace(oo)
R2 = VectorSpace(2)
R3 = VectorSpace(3)

def get_dim(w):
    if w == oo:
        return oo
    if isinstance(w, int) and w >= 0:
        return w
    if isinstance(w, VectorSpace):
        return w.dimension
    if hasattr(w, 'dimension'):
        d = w.dimension
        return d() if callable(d) else d
    if hasattr(w, 'dim'):
        d = w.dim
        return d() if callable(d) else d
    if type(w).__name__ in ('PolyRing', 'FractionField'):
        return oo
    if isinstance(w, str) and '[x]' in w:
        return oo
    raise ValueError("Not recognized as a vector space")

def conditions(witness) -> list[bool]:
    # H_1: V is a vector space over a field F
    try:
        dim = get_dim(witness)
        h1_ok = True
    except Exception:
        h1_ok = False

    # neg_Q: The dual space V^* is not finite-dimensional or \dim(V^*) != \dim(V)
    try:
        dim = get_dim(witness)
        if dim == oo:
            # For an infinite-dimensional space, the dual space is not finite-dimensional
            neg_q_ok = True
        else:
            # For a finite-dimensional space, the dual space is finite-dimensional and dimensions match
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "¬Q: The dual space V^* is not finite-dimensional or \\dim(V^*) != \\dim(V)"
]

N_HYP = 1
NEG_Q_INDEX = 1