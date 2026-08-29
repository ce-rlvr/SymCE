import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

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

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (G, x) where G is a group and x is an element.
    """
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, x = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # ¬Q: x is in Z(G) iff the cardinality of the conjugacy class of x is 1 (Conclusion FAILS)
    try:
        # x is in G
        in_G = x in G
        
        # x commutes with all elements of G (sufficient to check generators)
        # This also means the conjugacy class of x under G has cardinality 1
        commutes_with_all = all(g * x * ~g == x for g in G.generators)
        
        # x is in the center of G if it is in G and commutes with all elements of G
        in_center = in_G and commutes_with_all
        
        # The cardinality of the conjugacy class of x with respect to G is 1
        card_is_1 = commutes_with_all
        
        # The conclusion states: in_center <==> card_is_1
        # We want the negation of the conclusion
        neg_q = (in_center != card_is_1)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: x is in Z(G) is not equivalent to |Cl(x)| == 1"
]

N_HYP = 1
NEG_Q_INDEX = 1