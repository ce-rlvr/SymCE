import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
import math

# Standard group theory objects for witnesses
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # DihedralGroup(2) in SymPy is the Klein four-group V4
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness should be a tuple of two groups (G, H).
    """
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]

    # H_1: G is a cyclic group of order n
    try:
        if not hasattr(G, 'elements') or not hasattr(H, 'elements'):
            h1 = False
        else:
            n = int(G.order())
            # A group is cyclic if it contains an element whose order equals the group's order
            h1 = any(g.order() == n for g in G.elements)
    except Exception:
        h1 = False

    # ¬Q: Hom(G,H) is NOT isomorphic to the cyclic group of order gcd(n,m)
    try:
        n = int(G.order())
        m = int(H.order())
        k = math.gcd(n, m)
        
        # A homomorphism from a cyclic group G = <g> of order n to H is uniquely determined
        # by the image of g, which must be an element h in H such that h^n = e.
        # Thus, the elements of Hom(G,H) correspond bijectively to {h in H | h^n = e}.
        hom_elements = [h for h in H.elements if (h**n).is_Identity]
        
        # For Hom(G,H) to be isomorphic to C_k, the set of homomorphisms must form a group
        # of size k, and it must be cyclic (i.e., contain an element of order k).
        if len(hom_elements) != k:
            neg_q = True
        else:
            has_gen = any(h.order() == k for h in hom_elements)
            neg_q = not has_gen
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a cyclic group of order n",
    "¬Q: Hom(G,H) is not isomorphic to the cyclic group of order gcd(n,m)"
]

N_HYP = 1
NEG_Q_INDEX = 1