import sympy
from sympy.abc import n

# Top-level setup
# (No specific named objects needed for this domain; using sympy.abc.n for the polynomial variable)

def conditions(witness) -> list[bool]:
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be an object or dictionary providing the properties of the ring, 
    its Krull dimension, and the Hilbert-Samuel polynomial.
    """
    try:
        if isinstance(witness, dict):
            get = lambda k: witness.get(k, None)
        else:
            get = lambda k: getattr(witness, k, None)
            
        # H_1: (R, \mathfrak{m}) is a commutative Noetherian local ring
        try:
            h1 = bool(get('is_commutative_noetherian_local_ring'))
        except Exception:
            h1 = False
            
        # H_2: d is the Krull dimension of R
        try:
            d = get('d')
            krull_dim = get('krull_dimension')
            if d is None or krull_dim is None:
                h2 = False
            else:
                h2 = bool(sympy.sympify(d) == sympy.sympify(krull_dim))
        except Exception:
            h2 = False
            
        # H_3: P_I(n) is the Hilbert-Samuel polynomial associated to the I-adic filtration of R
        try:
            h3 = bool(get('is_Hilbert_Samuel_polynomial'))
        except Exception:
            h3 = False
            
        # ¬Q: The degree of the polynomial P_I(n) is not exactly d
        try:
            P_I = get('P_I')
            if P_I is None or d is None:
                neg_q = False
            else:
                P_I_sym = sympy.sympify(P_I)
                deg = sympy.degree(P_I_sym, gen=n)
                d_sym = sympy.sympify(d)
                neg_q = bool(deg != d_sym)
        except Exception:
            neg_q = False
            
    except Exception:
        return [False, False, False, False]

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: (R, m) is a commutative Noetherian local ring",
    "H_2: d is the Krull dimension of R",
    "H_3: P_I(n) is the Hilbert-Samuel polynomial associated to the I-adic filtration of R",
    "¬Q: The degree of the polynomial P_I(n) is not exactly d"
]

N_HYP = 3
NEG_Q_INDEX = 3