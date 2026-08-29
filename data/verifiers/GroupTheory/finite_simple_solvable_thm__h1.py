import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.ntheory import isprime

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    # H_1: G is a simple group
    try:
        h1 = False
        if hasattr(witness, 'is_simple') and witness.is_simple is not None:
            val = witness.is_simple
            h1 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'composition_series'):
            # A group is simple iff its composition series has exactly length 2 (the group itself and the trivial group)
            h1 = len(witness.composition_series()) == 2
        elif hasattr(witness, 'normal_subgroups'):
            h1 = len(witness.normal_subgroups()) == 2
    except Exception:
        h1 = False

    # H_2: G is a solvable group
    try:
        h2 = False
        if hasattr(witness, 'is_solvable') and witness.is_solvable is not None:
            val = witness.is_solvable
            h2 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'derived_series'):
            ds = witness.derived_series()
            last_order = ds[-1].order() if callable(getattr(ds[-1], 'order', None)) else ds[-1].order
            h2 = (last_order == 1)
    except Exception:
        h2 = False

    # ¬Q: G is not a cyclic group of prime order
    try:
        is_cyc = False
        if hasattr(witness, 'is_cyclic') and witness.is_cyclic is not None:
            val = witness.is_cyclic
            is_cyc = bool(val() if callable(val) else val)
        elif hasattr(witness, 'elements'):
            o = witness.order() if callable(getattr(witness, 'order', None)) else witness.order
            for g in witness.elements:
                go = g.order() if callable(getattr(g, 'order', None)) else g.order
                if go == o:
                    is_cyc = True
                    break
        
        o = witness.order() if callable(getattr(witness, 'order', None)) else witness.order
        q = is_cyc and isprime(o)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a simple group",
    "H_2: G is a solvable group",
    "¬Q: G is not a cyclic group of prime order"
]

N_HYP = 2
NEG_Q_INDEX = 2