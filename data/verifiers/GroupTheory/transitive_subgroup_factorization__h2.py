import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: The restricted action of H on X is transitive",
    "H_3: x is an element of X, and G_x is the stabilizer of x in G",
    "¬Q: G cannot be factored as G = H G_x"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        # Extract G, H, and x from the witness
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            x = witness.get('x')
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                G, H, x = witness
            elif len(witness) == 4:
                G, _, H, x = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
            
        # H_1: Let G be a group acting on a set X.
        try:
            h1 = isinstance(G, PermutationGroup)
        except Exception:
            h1 = False
            
        # H_2: The restricted action of H on X is transitive.
        # We ensure H acts on the same set X by checking degrees.
        try:
            h2 = isinstance(H, PermutationGroup) and H.is_transitive and H.degree == G.degree
        except Exception:
            h2 = False
            
        # H_3: Let x be an element of X, and let G_x denote the stabilizer of x in G.
        try:
            h3 = isinstance(x, int) and 0 <= x < G.degree
        except Exception:
            h3 = False
            
        # ¬Q: The group G can be factored as G = H G_x. (We want this to FAIL)
        try:
            if not (h1 and h2 and h3):
                neg_q = False
            else:
                # Guard against unreasonably large groups to ensure fast execution
                if G.order() > 5000 or H.order() > 5000:
                    neg_q = False
                else:
                    G_x = G.stabilizer(x)
                    
                    G_elements = set(G.generate())
                    H_elements = set(H.generate())
                    Gx_elements = set(G_x.generate())
                    
                    # Compute the set product H * G_x
                    HGx_elements = {h * k for h in H_elements for k in Gx_elements}
                    
                    # The conclusion fails if the sets are not equal
                    neg_q = (G_elements != HGx_elements)
        except Exception:
            neg_q = False
            
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]