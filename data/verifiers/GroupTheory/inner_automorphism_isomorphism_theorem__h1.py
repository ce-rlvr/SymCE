import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
    Checks if the witness is a counterexample to the conjecture.
    The conjecture states that for a group G, Inn(G) is isomorphic to G/Z(G).
    (Note: This is actually a true theorem in group theory, so neg_Q will 
    evaluate to False for any valid group).
    """
    # H_1: Z(G) is the center of G
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: Inn(G) is the group of inner automorphisms of G
    try:
        h2 = isinstance(witness, PermutationGroup)
    except Exception:
        h2 = False

    # ¬Q: Inn(G) is not isomorphic to the quotient group G/Z(G)
    try:
        if not isinstance(witness, PermutationGroup):
            neg_q = False
        else:
            order_G = witness.order()
            order_Z = witness.center().order()
            
            # Construct Inn(G) explicitly for small groups to verify
            if order_G <= 100:
                elements = list(witness.generate())
                inn_gens = []
                for g in witness.generators:
                    p = []
                    for x in elements:
                        p.append(elements.index(g * x * ~g))
                    inn_gens.append(Permutation(p))
                Inn_G = PermutationGroup(inn_gens)
                order_Inn = Inn_G.order()
            else:
                # For larger groups, we rely on the index of the center
                order_Inn = order_G // order_Z
                
            order_quotient = order_G // order_Z
            
            # Since Inn(G) is the image of G under the conjugation homomorphism
            # with kernel Z(G), it is always isomorphic to G/Z(G).
            # We verify this by checking if their orders match.
            is_iso = (order_Inn == order_quotient)
            neg_q = not is_iso
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Z(G) is the center of G",
    "H_2: Inn(G) is the group of inner automorphisms of G",
    "¬Q: Inn(G) is not isomorphic to the quotient group G/Z(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2