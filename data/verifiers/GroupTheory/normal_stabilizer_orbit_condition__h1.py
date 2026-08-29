import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks whether it is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (G, x) or (G, X, x) where G is a permutation group.
    """
    try:
        if len(witness) == 2:
            G, x = witness
            X = list(range(G.degree))
        elif len(witness) == 3:
            G, X, x = witness
        else:
            return [False, False, False, False]
            
        # H_1: x is an element of X
        h1 = x in X
        
        # H_2: G_x is the stabilizer of x in G
        try:
            Gx = G.stabilizer(x)
            h2 = True
        except Exception:
            h2 = False
            
        # H_3: O_x is the orbit of x under the action of G
        try:
            Ox = G.orbit(x)
            h3 = True
        except Exception:
            h3 = False
            
        # Conclusion: The stabilizer G_x is a normal subgroup of G if and only if G_x <= G_y for all y in O_x
        try:
            is_normal = Gx.is_normal(G)
            
            all_subset = True
            for y in Ox:
                Gy = G.stabilizer(y)
                if not Gx.is_subset(Gy):
                    all_subset = False
                    break
                    
            # The conjecture claims the equivalence holds. We want it to FAIL.
            neg_Q = not (is_normal == all_subset)
        except Exception:
            neg_Q = False
            
        return [h1, h2, h3, neg_Q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: x is an element of X",
    "H_2: G_x is the stabilizer of x in G",
    "H_3: O_x is the orbit of x under the action of G",
    "¬Q: It is not the case that (G_x is normal in G iff G_x <= G_y for all y in O_x)"
]

N_HYP = 3
NEG_Q_INDEX = 3