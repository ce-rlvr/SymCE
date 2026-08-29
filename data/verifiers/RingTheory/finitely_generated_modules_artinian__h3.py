import sympy
from sympy import Rational, Integer

class Ring:
    def __init__(self, name, has_identity=True):
        self.name = name
        self.has_identity = has_identity

class Module:
    def __init__(self, name, ring, is_fg=True, is_artinian=False):
        self.name = name
        self.ring = ring
        self.is_fg = is_fg
        self.is_artinian = is_artinian

# Top-level setup: named object bindings that the witness expression may reference.
Z_ring = Ring("Z", has_identity=True)
Z_module = Module("Z", Z_ring, is_fg=True, is_artinian=False)

Q_ring = Ring("Q", has_identity=True)
Q_module = Module("Q", Q_ring, is_fg=True, is_artinian=True)

Qx_ring = Ring("Q[x]", has_identity=True)
Qx_module = Module("Q[x]", Qx_ring, is_fg=True, is_artinian=False)

EvenZ_ring = Ring("2Z", has_identity=False)
EvenZ_module = Module("2Z", EvenZ_ring, is_fg=True, is_artinian=False)

Q_module_over_Z = Module("Q_over_Z", Z_ring, is_fg=False, is_artinian=False)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, M = witness
        else:
            M = witness
            R = M.ring
    except Exception:
        return [False] * 5

    # H_1: R is a ring
    try:
        h1 = isinstance(R, Ring)
    except Exception:
        h1 = False

    # H_2: R has a multiplicative identity
    try:
        h2 = bool(R.has_identity)
    except Exception:
        h2 = False

    # H_3: M is a left R-module
    try:
        h3 = isinstance(M, Module) and M.ring == R
    except Exception:
        h3 = False

    # H_4: M is finitely generated
    try:
        h4 = bool(M.is_fg)
    except Exception:
        h4 = False

    # ¬Q: M is not an Artinian module
    try:
        neg_q = not bool(M.is_artinian)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: R has a multiplicative identity",
    "H_3: M is a left R-module",
    "H_4: M is finitely generated",
    "¬Q: M is not an Artinian module"
]

N_HYP = 4
NEG_Q_INDEX = 4