import sympy
from sympy import S
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup
from sympy.matrices import eye, zeros
from sympy.polys.domains.field import Field
from sympy.polys.domains.finitefield import FiniteField
from sympy.polys.domains.algebraicfield import AlgebraicField
from sympy.ntheory import isprime

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def _is_vector_space(v):
    if v in (S.Complexes, S.Reals, S.Rationals):
        return True
    if hasattr(v, 'is_Matrix') and v.is_Matrix:
        return True
    if isinstance(v, Field):
        return True
    if hasattr(v, 'ext') and hasattr(v, 'domain'):
        return True
    if hasattr(v, 'mod') and hasattr(v, 'domain'):
        return True
    if isinstance(v, PermutationGroup):
        if not v.is_abelian:
            return False
        orders = set(g.order() for g in v.elements if g.order() != 1)
        if len(orders) == 0:
            return True
        if len(orders) > 1:
            return False
        p = list(orders)[0]
        return isprime(p)
    if isinstance(v, tuple) and len(v) == 2:
        n, q = v
        if isinstance(n, int) and isinstance(q, int) and n > 0 and q > 1:
            return True
    return False

def _is_non_prime_field(v):
    if v in (S.Complexes, S.Reals):
        return True
    if v == S.Rationals:
        return False
    if hasattr(v, 'is_Matrix') and v.is_Matrix:
        return True
    if isinstance(v, AlgebraicField):
        return True
    if isinstance(v, FiniteField):
        return False
    if isinstance(v, PermutationGroup):
        return False
    if isinstance(v, tuple) and len(v) == 2:
        n, q = v
        return not isprime(q)
    return True

def conditions(witness):
    if isinstance(witness, tuple) and len(witness) == 2 and not isinstance(witness[0], int):
        v = witness[0]
    else:
        v = witness

    try:
        h1_ok = _is_vector_space(v)
    except Exception:
        h1_ok = False

    try:
        h2_ok = h1_ok
    except Exception:
        h2_ok = False

    try:
        neg_q_ok = _is_non_prime_field(v)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "H_2: phi is the natural action of GL(V) on V by linear evaluation",
    "¬Q: The affine group Aff(V) of V is not isomorphic to the external semidirect product V ⋊_phi GL(V)"
]

N_HYP = 2
NEG_Q_INDEX = 2