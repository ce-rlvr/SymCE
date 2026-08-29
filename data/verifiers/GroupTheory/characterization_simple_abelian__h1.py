import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.ntheory import isprime

# Top-level setup: named object bindings for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a counterexample to the conjecture:
    "G is simple if and only if G is isomorphic to Z/pZ for some prime p."
    
    Since all groups of prime order are simple, the only way the conclusion 
    can fail is if G is simple but NOT of prime order.
    """
    try:
        order = witness.order()
        is_prime_order = isprime(order)
    except Exception:
        return [False]
        
    if is_prime_order:
        # If order is prime, the group is simple and isomorphic to Z/pZ.
        # The conclusion holds, so its negation is False.
        return [False]
        
    try:
        # If order is not prime, the group is not isomorphic to Z/pZ.
        # The conclusion fails (neg_Q is True) if and only if the group IS simple.
        # A group is simple iff it has exactly 2 normal subgroups (itself and trivial).
        is_simple = (len(witness.normal_subgroups()) == 2)
        neg_q = bool(is_simple)
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: G is simple but not isomorphic to a cyclic group of prime order"
]

N_HYP = 0
NEG_Q_INDEX = 0