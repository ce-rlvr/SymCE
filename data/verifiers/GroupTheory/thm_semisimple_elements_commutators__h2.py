import sympy
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
import itertools

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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, g = witness
            target_g_specified = True
        else:
            G = witness
            target_g_specified = False
            g = None
            
        if not hasattr(G, 'elements') or not hasattr(G, 'normal_subgroups'):
            h1_ok = False
        else:
            h1_ok = True
            for N in G.normal_subgroups():
                if N.order() > 1 and N.is_abelian:
                    h1_ok = False
                    break
    except Exception:
        h1_ok = False

    try:
        if not h1_ok:
            neg_q = False
        else:
            elements = list(G.elements)
            commutators = set()
            for x in elements:
                for y in elements:
                    commutators.add(x * y * (x**-1) * (y**-1))
            
            if target_g_specified:
                neg_q = g not in commutators
            else:
                neg_q = len(commutators) < G.order()
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite semisimple group",
    "¬Q: The specified element g (or some element in G) cannot be represented as a commutator x*y*x^-1*y^-1"
]

N_HYP = 1
NEG_Q_INDEX = 1