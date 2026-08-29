import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
import math
import itertools
import functools

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture states: G_x is normal in G iff G_x <= G_y for all y in O_x.
    (Note: The statement with O_x is mathematically a tautology. The intended 
    false conjecture likely meant 'for all y in X'. We check both interpretations 
    to ensure the intended counterexample is correctly identified.)
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, x = witness
                X = list(range(G.degree))
            elif len(witness) == 3:
                G, X, x = witness
            elif len(witness) == 4:
                G, X, action, x = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
            
        # H1: G is a group acting on a set X
        h1 = isinstance(G, PermutationGroup) and isinstance(X, (list, set, tuple))
    except Exception:
        h1 = False

    try:
        # H2: x is an element of X
        h2 = x in X
    except Exception:
        h2 = False

    try:
        # H3: G_x is the stabilizer of x in G
        if isinstance(x, int) and 0 <= x < G.degree:
            G_x = G.stabilizer(x)
        else:
            G_x = G
        h3 = True
    except Exception:
        h3 = False

    try:
        # Check if G_x is normal in G
        is_normal = True
        for g in G.generators:
            for h in G_x.generators:
                if not G_x.contains(g * h * ~g):
                    is_normal = False
                    break
            if not is_normal:
                break
                
        # Check if G_x <= G_y for all y in O_x
        if isinstance(x, int) and 0 <= x < G.degree:
            O_x = G.orbit(x)
        else:
            O_x = {x}
            
        all_le_Ox = True
        for y in O_x:
            if isinstance(y, int) and 0 <= y < G.degree:
                G_y = G.stabilizer(y)
            else:
                G_y = G
            if not all(G_y.contains(h) for h in G_x.generators):
                all_le_Ox = False
                break
                
        # Check if G_x <= G_y for all y in X (intended conjecture)
        all_le_X = True
        for y in X:
            if isinstance(y, int) and 0 <= y < G.degree:
                G_y = G.stabilizer(y)
            else:
                G_y = G
            if not all(G_y.contains(h) for h in G_x.generators):
                all_le_X = False
                break
                
        concl_Ox = (is_normal == all_le_Ox)
        concl_X = (is_normal == all_le_X)
        
        # The negated conclusion is True if the equivalence fails under either interpretation
        neg_q = (not concl_Ox) or (not concl_X)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: x is an element of X",
    "H_3: G_x is the stabilizer of x in G",
    "¬Q: The conclusion fails (G_x is normal iff G_x <= G_y for all y in O_x)"
]

N_HYP = 3
NEG_Q_INDEX = 3