import sympy
from sympy import *

# Top-level setup: named object bindings that the witness expression may reference.
Q = "Q"
Q_bar = "Q_bar"
Q_ab = "Q_ab"
Q_sqrt_primes = "Q_sqrt_primes"
Q_mu_infty = "Q(mu_infty)"
F_p = "F_p"
F_p_bar = "F_p_bar"
F_q = "F_q"
F_q_bar = "F_q_bar"
R = "R"
C = "C"
Q_sqrt_2 = "Q(sqrt(2))"
Q_cbrt_2 = "Q(cbrt(2))"

# Dictionary of known field extensions (K, F) and their properties.
# "bijection" refers to whether the map E \mapsto Gal(K/E) is an inclusion-reversing bijection.
# This bijection holds for finite Galois extensions, but fails for infinite Galois extensions
# (where the image only consists of Krull-closed subgroups).
KNOWN_EXTENSIONS = {
    (Q_bar, Q): {"is_extension": True, "is_galois": True, "bijection": False},
    (Q_ab, Q): {"is_extension": True, "is_galois": True, "bijection": False},
    (Q_sqrt_primes, Q): {"is_extension": True, "is_galois": True, "bijection": False},
    (Q_mu_infty, Q): {"is_extension": True, "is_galois": True, "bijection": False},
    (F_p_bar, F_p): {"is_extension": True, "is_galois": True, "bijection": False},
    (F_q_bar, F_q): {"is_extension": True, "is_galois": True, "bijection": False},
    (Q_sqrt_2, Q): {"is_extension": True, "is_galois": True, "bijection": True},
    (Q_cbrt_2, Q): {"is_extension": True, "is_galois": False, "bijection": False},
    (R, Q): {"is_extension": True, "is_galois": False, "bijection": False},
    (C, R): {"is_extension": True, "is_galois": True, "bijection": True},
    ("Q(sqrt(2), sqrt(3))", Q): {"is_extension": True, "is_galois": True, "bijection": True},
    ("Q(zeta_5)", Q): {"is_extension": True, "is_galois": True, "bijection": True},
}

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, str) and "/" in witness:
            K, F = witness.split("/")
            K, F = K.strip(), F.strip()
        elif isinstance(witness, tuple) and len(witness) == 2:
            K, F = witness
        else:
            return [False, False, False]
            
        props = KNOWN_EXTENSIONS.get((K, F))
        if props is None:
            return [False, False, False]
            
        h1 = props["is_extension"]
        h2 = props["is_galois"]
        neg_q = not props["bijection"]
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: K is a field extension of F",
    "H_2: The extension K/F is Galois",
    "¬Q: The map E \\mapsto Gal(K/E) is not a bijection (fails for infinite Galois extensions)"
]

N_HYP = 2
NEG_Q_INDEX = 2