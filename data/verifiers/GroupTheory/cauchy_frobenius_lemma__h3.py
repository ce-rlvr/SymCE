import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy import Rational

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

def conditions(witness) -> list[bool]:
    try:
        G, X, action = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group
    try:
        if isinstance(G, PermutationGroup):
            h1_ok = True
        elif isinstance(G, (list, set, tuple)) and len(G) > 0:
            h1_ok = True
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    # H_2: X is a finite set
    try:
        X_list = list(X)
        h2_ok = True
    except Exception:
        h2_ok = False

    # ¬Q: The number of distinct orbits of the action is NOT \frac{1}{|G|} \sum_{g \in G} |X^g|
    try:
        if isinstance(G, PermutationGroup):
            G_elements = list(G.generate())
        else:
            G_elements = list(G)
            
        def get_action(g, x):
            if callable(action):
                return action(g, x)
            else:
                return action[(g, x)]
                
        # Calculate the set of distinct orbits
        orbits = set()
        for x in X_list:
            orbit = frozenset(get_action(g, x) for g in G_elements)
            orbits.add(orbit)
        num_orbits = len(orbits)
        
        # Calculate the sum of the number of fixed points for each g in G
        sum_fixed = 0
        for g in G_elements:
            fixed_count = sum(1 for x in X_list if get_action(g, x) == x)
            sum_fixed += fixed_count
            
        lhs = num_orbits
        rhs = Rational(sum_fixed, len(G_elements))
        
        neg_q_ok = (lhs != rhs)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: X is a finite set",
    "¬Q: The number of distinct orbits is not equal to 1/|G| sum_{g in G} |X^g|"
]

N_HYP = 2
NEG_Q_INDEX = 2