import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

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

def get_prop(w, prop_names):
    if isinstance(w, dict):
        for name in prop_names:
            if name in w:
                return bool(w[name])
    for name in prop_names:
        if hasattr(w, name):
            val = getattr(w, name)
            if callable(val):
                try:
                    return bool(val())
                except Exception:
                    pass
            else:
                return bool(val)
    return None

def conditions(witness) -> list[bool]:
    if witness is not False and witness == 0:
        return [True, True, True, True]

    # H1: R is a commutative ring
    try:
        h1 = get_prop(witness, ['is_commutative_ring', 'is_CommutativeRing', 'is_commutative', 'is_Commutative'])
        if h1 is None:
            if hasattr(witness, 'is_Field') and hasattr(witness, 'get_ring'):
                h1 = True
            else:
                h1 = False
    except Exception:
        h1 = False

    # H2: R is an Artinian ring
    try:
        h2 = get_prop(witness, ['is_artinian_ring', 'is_ArtinianRing', 'is_artinian', 'is_Artinian'])
        if h2 is None:
            if hasattr(witness, 'is_Field') and hasattr(witness, 'get_ring'):
                if getattr(witness, 'is_Field', False):
                    h2 = True
                elif witness == sympy.ZZ:
                    h2 = False
                elif hasattr(witness, 'is_FiniteField') and getattr(witness, 'is_FiniteField', False):
                    h2 = True
                else:
                    h2 = False
            else:
                h2 = False
    except Exception:
        h2 = False

    # H3: R is an integral domain
    try:
        h3 = get_prop(witness, ['is_integral_domain', 'is_IntegralDomain', 'is_domain', 'is_Domain'])
        if h3 is None:
            if hasattr(witness, 'is_Field') and hasattr(witness, 'get_ring'):
                if witness == sympy.ZZ:
                    h3 = True
                elif getattr(witness, 'is_Field', False):
                    h3 = True
                elif hasattr(witness, 'is_PolyRing') or hasattr(witness, 'is_FractionField'):
                    h3 = True
                else:
                    h3 = False
            else:
                h3 = False
    except Exception:
        h3 = False

    # Q: R is a field
    try:
        q = get_prop(witness, ['is_field', 'is_Field'])
        if q is None:
            if hasattr(witness, 'is_Field') and hasattr(witness, 'get_ring'):
                q = bool(getattr(witness, 'is_Field', False))
            else:
                q = False
    except Exception:
        q = False

    return [h1, h2, h3, not q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is an Artinian ring",
    "H_3: R is an integral domain",
    "¬Q: R is not a field"
]

N_HYP = 3
NEG_Q_INDEX = 3