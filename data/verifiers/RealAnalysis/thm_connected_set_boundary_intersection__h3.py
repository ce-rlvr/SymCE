import sympy
from sympy import S, Interval, FiniteSet

# Top-level setup
# In Real Analysis, witnesses are typically subsets of the real line.
# We define standard spaces and sets that might be used as witnesses.
R = S.Reals
Z = S.Integers
Q = S.Rationals
N = S.Naturals

def conditions(witness):
    """
    Given a witness object, evaluates the hypotheses and the negated conclusion.
    The witness is expected to be a tuple (X, A, B) or a dictionary with keys 'X', 'A', 'B',
    where X is a topological space (e.g., S.Reals), A is a connected subset, and B is a subset.
    """
    try:
        if isinstance(witness, dict):
            X = witness.get('X', S.Reals)
            A = witness['A']
            B = witness['B']
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                X, A, B = witness
            else:
                A, B = witness
                X = S.Reals
        else:
            A = witness.A
            B = witness.B
            X = getattr(witness, 'X', S.Reals)
    except Exception:
        return [False, False, False, False, False]

    # H1: X is a topological space
    try:
        # In this context, if X is a SymPy Set, it inherits the standard topology
        h1 = hasattr(X, 'intersect') or X is True
        if X is S.Reals:
            h1 = True
    except Exception:
        h1 = False

    # H2: A is a connected subset of X
    try:
        if hasattr(A, 'is_subset'):
            is_sub = A.is_subset(X)
            is_sub = True if is_sub is None else bool(is_sub)
        else:
            is_sub = True
            
        # Check connectedness
        is_conn = False
        if hasattr(A, 'is_connected'):
            val = A.is_connected
            is_conn = val() if callable(val) else bool(val)
        elif type(A).__name__ in ['Interval', 'Reals']:
            is_conn = True
        elif type(A).__name__ == 'FiniteSet' and len(A) == 1:
            is_conn = True
        else:
            # Fallback for custom objects
            is_conn = True
            
        h2 = is_sub and is_conn
    except Exception:
        h2 = False

    # H3: A \cap B \neq \emptyset
    try:
        inter = A.intersect(B)
        h3 = (inter.is_empty == False)
    except Exception:
        h3 = False

    # H4: A \setminus B \neq \emptyset
    try:
        diff = A - B
        h4 = (diff.is_empty == False)
    except Exception:
        h4 = False

    # neg_Q: A \cap \partial B == \emptyset  (Conclusion FAILS)
    try:
        if hasattr(B, 'boundary'):
            bnd = B.boundary
            if callable(bnd):
                bnd = bnd()
        else:
            bnd = None
            
        if bnd is not None:
            inter_bnd = A.intersect(bnd)
            neg_q = (inter_bnd.is_empty == True)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: X is a topological space",
    "H_2: A is a connected subset of X",
    "H_3: A \\cap B \\neq \\emptyset",
    "H_4: A \\setminus B \\neq \\emptyset",
    "¬Q: A \\cap \\partial B = \\emptyset"
]

N_HYP = 4
NEG_Q_INDEX = 4