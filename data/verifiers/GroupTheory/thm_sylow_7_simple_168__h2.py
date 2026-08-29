import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.named_groups import *
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    """
    # H_1: G is a simple finite group
    try:
        if not hasattr(witness, 'order'):
            h1 = False
        else:
            order = witness.order()
            if order < 2:
                h1 = False
            else:
                sim = getattr(witness, 'is_simple', None)
                if callable(sim):
                    h1 = bool(sim())
                elif sim is not None:
                    h1 = bool(sim)
                else:
                    h1 = (len(witness.normal_subgroups()) == 2)
    except Exception:
        h1 = False

    # ¬Q: The number of Sylow 7-subgroups of G is not exactly 8
    try:
        if not hasattr(witness, 'order'):
            neg_q = False
        else:
            order = witness.order()
            if order % 7 != 0:
                n7 = 1
            else:
                try:
                    # Find one Sylow 7-subgroup
                    P = witness.sylow_subgroup(7)
                    P_elements = frozenset(P.elements)
                    
                    # Compute the number of conjugates of P in G
                    orbit = {P_elements}
                    queue = [P_elements]
                    gens = witness.generators
                    
                    while queue:
                        current = queue.pop(0)
                        for g in gens:
                            g_inv = ~g
                            conj = frozenset(g_inv * x * g for x in current)
                            if conj not in orbit:
                                orbit.add(conj)
                                queue.append(conj)
                        if len(orbit) > 5000:
                            break
                    n7 = len(orbit)
                except Exception:
                    # Fallback for groups where sylow_subgroup might fail
                    k = 0
                    temp = order
                    while temp % 7 == 0:
                        k += 1
                        temp //= 7
                    if k == 1 and order <= 10000:
                        elements_of_order_7 = sum(1 for g in witness.elements if g.order() == 7)
                        n7 = elements_of_order_7 // 6
                    else:
                        n7 = -1
            
            neg_q = (n7 != 8) and (n7 != -1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a simple finite group",
    "¬Q: The number of Sylow 7-subgroups of G is not exactly 8"
]

N_HYP = 1
NEG_Q_INDEX = 1