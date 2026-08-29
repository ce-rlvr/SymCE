import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (G, x) where G is a group and x is an element.
    """
    try:
        if not (isinstance(witness, tuple) and len(witness) == 2):
            return [False, False]
        G, x = witness
    except Exception:
        return [False, False]

    # H_1: G is a group
    try:
        h1_ok = hasattr(G, 'elements') and hasattr(G, 'generators')
    except Exception:
        h1_ok = False

    # neg_Q: The conclusion "x in Z(G) iff |Cl_G(x)| == 1" FAILS
    try:
        # Check if x is in the center Z(G)
        in_center = False
        try:
            if x in G:
                # If x is in G, it is in Z(G) iff it commutes with all generators of G
                in_center = all(g * x == x * g for g in G.generators)
        except Exception:
            pass
            
        # Compute the size of the conjugacy class of x under the action of G
        cl_G_x = set()
        for g in G.elements:
            try:
                inv_g = ~g
            except Exception:
                inv_g = g.inv()
            cl_G_x.add(g * x * inv_g)
            
        size_cl = len(cl_G_x)
        
        # The conclusion is: in_center <==> (size_cl == 1)
        # We want the negation of this conclusion
        neg_q_ok = (in_center != (size_cl == 1))
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: (x in Z(G)) is not equivalent to (|Cl_G(x)| == 1)"
]

N_HYP = 1
NEG_Q_INDEX = 1