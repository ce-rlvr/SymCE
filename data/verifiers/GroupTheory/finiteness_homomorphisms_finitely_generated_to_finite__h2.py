import sympy
from sympy.combinatorics import PermutationGroup, free_group
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

# Z is the infinite cyclic group, which is a free group on 1 generator
Z, (_x,) = free_group('x')

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, H) of two SymPy groups.
    """
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]

    # H_1: G is a finitely generated group
    try:
        # In SymPy, PermutationGroup and FreeGroup are finitely generated.
        h1_ok = hasattr(G, 'generators') and len(list(G.generators)) >= 0
    except Exception:
        h1_ok = False

    # neg_Q: The set of all group homomorphisms from G to H is infinite
    try:
        def maps_onto_Z(grp):
            if type(grp).__name__ == 'FreeGroup':
                return len(grp.generators) > 0
            return False
            
        def has_infinite_order_elements(grp):
            if type(grp).__name__ == 'FreeGroup':
                return len(grp.generators) > 0
            return False
        
        # If G maps onto Z, and H has elements of infinite order (like Z),
        # we can construct infinitely many homomorphisms by mapping the generator of G's Z quotient
        # to any power of an infinite-order element in H.
        neg_q_ok = maps_onto_Z(G) and has_infinite_order_elements(H)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finitely generated group",
    "¬Q: The set of all group homomorphisms from G to H is infinite"
]

N_HYP = 1
NEG_Q_INDEX = 1