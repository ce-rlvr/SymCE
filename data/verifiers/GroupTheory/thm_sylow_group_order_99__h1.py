import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

CONDITION_LABELS = [
    "H_1: The order of G is 99",
    "¬Q: G does not have a unique, normal Sylow 11-subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    # H_1: The order of G is 99
    try:
        if hasattr(witness, 'order'):
            order_attr = witness.order
            if callable(order_attr):
                order = order_attr()
            else:
                order = order_attr
        else:
            order = len(witness)
        h1 = bool(order == 99)
    except Exception:
        h1 = False

    # ¬Q: G does not have a unique, normal Sylow 11-subgroup
    try:
        has_unique_normal = False
        is_group = hasattr(witness, 'sylow_subgroup') or hasattr(witness, 'elements') or hasattr(witness, 'generate')
        if not is_group:
            has_unique_normal = False
        else:
            try:
                if hasattr(witness, 'sylow_subgroup') and hasattr(witness, 'is_normal'):
                    P11 = witness.sylow_subgroup(11)
                    has_unique_normal = bool(witness.is_normal(P11))
                else:
                    raise AttributeError
            except Exception:
                # Fallback for groups if sylow_subgroup is not available
                if hasattr(witness, 'elements'):
                    elements = witness.elements
                elif hasattr(witness, 'generate'):
                    elements = list(witness.generate())
                else:
                    elements = list(witness)
                
                order_11_count = 0
                for g in elements:
                    if hasattr(g, 'order'):
                        g_order_attr = g.order
                        if callable(g_order_attr):
                            g_order = g_order_attr()
                        else:
                            g_order = g_order_attr
                        if g_order == 11:
                            order_11_count += 1
                
                # A group of order 99 has a unique Sylow 11-subgroup iff it has exactly 10 elements of order 11
                has_unique_normal = bool(order_11_count == 10)
    except Exception:
        has_unique_normal = False

    neg_q = not has_unique_normal

    return [h1, neg_q]