import sympy
from sympy import Symbol, sqrt
from sympy.polys.domains import QQ, ZZ, FF

# Top-level setup: named object bindings for the witness expression
x = Symbol('x')
y = Symbol('y')

# Common fields and extensions
QQ_x = QQ.frac_field(x)
QQ_y = QQ.frac_field(y)
QQ_sq2 = QQ.algebraic_field(sqrt(2))

F2 = FF(2)
F2_x = F2.frac_field(x)
F3 = FF(3)
F3_x = F3.frac_field(x)

def is_subfield(K, L):
    """Check if K is a subfield of L for our standard domains."""
    if K == L:
        return True
    if getattr(L, 'domain', None) == K:
        return True
    return False

def is_separable_closure(S, E, F):
    """Check if S is the separable closure of F in E."""
    if F == QQ:
        if E == QQ:
            return S == QQ
        if getattr(E, 'domain', None) == QQ:
            if hasattr(E, 'symbols'):  # Transcendental extension (fraction field)
                return S == QQ
            if hasattr(E, 'ext'):      # Algebraic extension
                return S == E
    elif hasattr(F, 'char') and F.char > 0:
        if E == F:
            return S == F
        if getattr(E, 'domain', None) == F:
            if hasattr(E, 'symbols'):  # Transcendental extension over finite field
                return S == F
    return False

def is_purely_inseparable(E, S):
    """Check if the extension E/S is purely inseparable."""
    if hasattr(S, 'char') and S.char == 0:
        # In characteristic 0, purely inseparable implies E == S
        return E == S
    elif hasattr(S, 'char') and S.char > 0:
        # For our standard transcendental extensions F(x)/F, it is not purely inseparable
        if hasattr(E, 'symbols') and getattr(E, 'domain', None) == S:
            return False
        return E == S
    return False

def conditions(witness) -> list[bool]:
    """
    Given a witness (E, F, S), check if it is a valid counterexample.
    Returns [H_1_ok, neg_Q_ok].
    """
    try:
        E, F, S = witness
    except Exception:
        return [False, False]
    
    # Hypothesis 1: S is the set of all elements in E that are separable over F
    try:
        h1 = is_separable_closure(S, E, F)
    except Exception:
        h1 = False
        
    # Conclusion: S is a subfield of E, S/F is separable, and E/S is purely inseparable.
    # We want the negation of this conclusion to be True.
    try:
        q_subfield = is_subfield(S, E)
        q_sep = is_separable_closure(S, S, F)
        q_pure_insep = is_purely_inseparable(E, S)
        
        q = q_subfield and q_sep and q_pure_insep
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: S is the set of all elements in E that are separable over F",
    "¬Q: It is not the case that S is a subfield of E, S/F is separable, and E/S is purely inseparable"
]

N_HYP = 1
NEG_Q_INDEX = 1