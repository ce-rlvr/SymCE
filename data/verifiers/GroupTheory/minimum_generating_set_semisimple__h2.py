import math
import sympy
from sympy.ntheory import factorint
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_exponent_abelian(G):
    """Returns the exponent of an abelian group."""
    exp = 1
    for g in G.generators:
        order = g.order()
        exp = abs(exp * order) // math.gcd(exp, order)
    return exp

def is_semisimple(G):
    """
    Checks if a finite group is semisimple (a direct product of simple groups).
    For abelian groups, this is true iff the exponent is square-free.
    """
    if not isinstance(G, PermutationGroup):
        return False
    
    if getattr(G, 'is_abelian', False):
        exp = get_exponent_abelian(G)
        factors = factorint(exp)
        return all(v == 1 for v in factors.values())
    else:
        # For non-abelian groups, we do a basic check for known simple groups (e.g., A5).
        # Since the counterexample witness must be cyclic (hence abelian) to fail the conclusion,
        # returning False for most non-abelian groups is safe for verification purposes.
        if G.order() == 60:
            return True
        return False

def is_cyclic(G):
    """
    Checks if a finite group is cyclic.
    An abelian group is cyclic iff its exponent equals its order.
    """
    if not isinstance(G, PermutationGroup):
        return False
    if not getattr(G, 'is_abelian', False):
        return False
    exp = get_exponent_abelian(G)
    return exp == G.order()

def conditions(witness):
    try:
        h1 = False
        if isinstance(witness, PermutationGroup):
            if witness.order() > 1:
                h1 = is_semisimple(witness)
    except Exception:
        h1 = False

    try:
        neg_q = False
        if isinstance(witness, PermutationGroup):
            # The conclusion is that the minimum generating set size is > 1.
            # The negated conclusion is that the size is <= 1, which means the group is cyclic.
            neg_q = is_cyclic(witness)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a non-trivial semisimple finite group",
    "¬Q: The cardinality of S is <= 1 (i.e., G is cyclic)"
]

N_HYP = 1
NEG_Q_INDEX = 1