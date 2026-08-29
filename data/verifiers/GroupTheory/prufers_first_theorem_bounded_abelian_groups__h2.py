import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z
import math
import itertools
import functools
import z3

# Top-level setup: named object bindings
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

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture:
    "Every abelian group is isomorphic to a direct sum of cyclic groups."
    (The dropped hypothesis was that the group is bounded).
    """
    h1 = False
    try:
        if hasattr(witness, 'is_abelian'):
            h1 = bool(witness.is_abelian)
        elif witness in [sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes, sympy.S.Integers]:
            h1 = True
        elif hasattr(sympy, 'QQ') and witness in [sympy.QQ, sympy.RR, sympy.CC, sympy.ZZ]:
            h1 = True
        elif isinstance(witness, str):
            w_lower = witness.lower()
            if w_lower in ["q", "r", "c", "rationals", "reals", "complexes", "prufer", "prufer group", "z(p^infty)", "z", "integers"]:
                h1 = True
    except Exception:
        h1 = False

    neg_q = False
    try:
        is_dscg = None
        if hasattr(witness, 'is_direct_sum_of_cyclic_groups'):
            is_dscg = bool(witness.is_direct_sum_of_cyclic_groups)
        elif witness in [sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes]:
            is_dscg = False
        elif hasattr(sympy, 'QQ') and witness in [sympy.QQ, sympy.RR, sympy.CC]:
            is_dscg = False
        elif witness == sympy.S.Integers or (hasattr(sympy, 'ZZ') and witness == sympy.ZZ):
            is_dscg = True
        elif isinstance(witness, str):
            w_lower = witness.lower()
            if w_lower in ["q", "r", "c", "rationals", "reals", "complexes", "prufer", "prufer group", "z(p^infty)"]:
                is_dscg = False
            elif w_lower in ["z", "integers"]:
                is_dscg = True
        elif hasattr(witness, 'is_abelian') and witness.is_abelian:
            # For SymPy's finite/finitely presented groups, abelian implies direct sum of cyclic groups
            is_dscg = True
            
        if is_dscg is not None:
            neg_q = not is_dscg
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "¬Q: G is not isomorphic to a direct sum of cyclic groups"
]

N_HYP = 1
NEG_Q_INDEX = 1