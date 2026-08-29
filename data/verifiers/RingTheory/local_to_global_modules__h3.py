import sympy
from sympy import ZZ, QQ, RR, CC, S
from sympy.polys.domains.domain import Domain
from sympy import Set, FiniteSet

# Top-level setup
Z = ZZ
Q = QQ
R_ring = RR
C_ring = CC

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness can be a tuple (R, M) or just a single object representing both R and M.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, M = witness
        else:
            R, M = witness, witness
    except Exception:
        R, M = None, None

    def is_comm_ring_with_id(ring):
        if isinstance(ring, Domain):
            return True
        if ring in [S.Integers, S.Rationals, S.Reals, S.Complexes]:
            return True
        return False

    def is_R_module(ring, mod):
        if isinstance(mod, (Domain, Set, list, tuple)):
            return True
        return False

    def is_zero_module(mod):
        if isinstance(mod, Domain):
            return False
        if isinstance(mod, FiniteSet):
            if len(mod) == 1 and list(mod)[0] == 0:
                return True
            return False
        if isinstance(mod, Set):
            return False
        if isinstance(mod, (list, tuple)):
            if len(mod) == 0:
                return False
            return all(x == 0 for x in mod)
        return False

    try:
        h1 = is_comm_ring_with_id(R)
    except Exception:
        h1 = False

    try:
        h2 = is_R_module(R, M)
    except Exception:
        h2 = False

    try:
        neg_q = not is_zero_module(M)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: M is an R-module",
    "¬Q: M is not the zero module"
]

N_HYP = 2
NEG_Q_INDEX = 2