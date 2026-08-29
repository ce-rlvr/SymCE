import sympy
from sympy.combinatorics import Permutation, Cycle
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple of two objects (sigma, tau) representing functions/transformations.
    """
    try:
        sigma, tau = witness
    except Exception:
        return [False, False]
        
    def get_moved_elements(p):
        if hasattr(p, 'support'):
            supp = p.support
            if callable(supp):
                return set(supp())
            return set(supp)
        if hasattr(p, 'moved'):
            moved = p.moved
            if callable(moved):
                return set(moved())
            return set(moved)
        if isinstance(p, dict):
            return {k for k, v in p.items() if k != v}
        if isinstance(p, (list, tuple)):
            return {i for i, v in enumerate(p) if i != v}
        raise ValueError("Cannot determine moved elements")

    # H_1: Assume that the sets of elements moved by sigma and tau are disjoint
    try:
        moved_sigma = get_moved_elements(sigma)
        moved_tau = get_moved_elements(tau)
        h1 = moved_sigma.isdisjoint(moved_tau)
    except Exception:
        h1 = False

    # neg_Q: The permutations sigma and tau DO NOT commute (sigma * tau != tau * sigma)
    try:
        neg_q = (sigma * tau) != (tau * sigma)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The sets of elements moved by sigma and tau are disjoint",
    "¬Q: sigma and tau do not commute (sigma * tau != tau * sigma)"
]

N_HYP = 1
NEG_Q_INDEX = 1