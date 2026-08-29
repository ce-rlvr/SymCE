import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            N = witness.get('N')
            H = witness.get('H')
        else:
            G, N, H = witness
    except Exception:
        return [False, False, False]

    def get_elements(grp):
        if hasattr(grp, 'elements'):
            return list(grp.elements)
        elif hasattr(grp, 'generate'):
            return list(grp.generate())
        else:
            return []

    def is_cyclic(grp):
        try:
            if hasattr(grp, 'is_cyclic') and callable(grp.is_cyclic):
                return grp.is_cyclic()
            elif hasattr(grp, 'is_cyclic'):
                return grp.is_cyclic
        except Exception:
            pass
        
        try:
            order = grp.order()
            if order == 1:
                return True
            for g in get_elements(grp):
                if hasattr(g, 'order') and callable(g.order):
                    if g.order() == order:
                        return True
            return False
        except Exception:
            return False

    def is_quotient_cyclic(G, K):
        try:
            q_order = G.order() // K.order()
            if q_order == 1:
                return True
            for g in get_elements(G):
                is_gen = True
                for d in range(1, q_order):
                    if q_order % d == 0:
                        if (g**d) in K:
                            is_gen = False
                            break
                if is_gen and (g**q_order) in K:
                    return True
            return False
        except Exception:
            return False

    def is_metacyclic(G):
        if is_cyclic(G):
            return True
        try:
            normals = G.normal_subgroups()
        except Exception:
            return False
        for K in normals:
            if is_cyclic(K) and is_quotient_cyclic(G, K):
                return True
        return False

    try:
        h1_ok = bool(is_cyclic(N))
    except Exception:
        h1_ok = False

    try:
        h2_ok = bool(is_cyclic(H))
    except Exception:
        h2_ok = False

    try:
        neg_q_ok = not is_metacyclic(G)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: N is a cyclic group",
    "H_2: H is a cyclic group",
    "¬Q: G is not a metacyclic group"
]

N_HYP = 2
NEG_Q_INDEX = 2