import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple: (N, H, G, e_N, action)
    or (N, H, G, action) where e_N is implicitly N.identity.
    """
    try:
        if len(witness) == 5:
            N, H, G, e_N, action = witness
        elif len(witness) == 4:
            N, H, G, action = witness
            e_N = N.identity if hasattr(N, 'identity') else None
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: N and H are groups
    try:
        h1 = isinstance(N, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H2: G = N \rtimes H is the semidirect product of N and H
    try:
        h2 = False
        if isinstance(G, PermutationGroup):
            # Check if N and H are subgroups of G
            N_sub = all(g in G for g in N.generators)
            H_sub = all(g in G for g in H.generators)
            
            if N_sub and H_sub:
                # Check if N is a normal subgroup of G
                normal = True
                for n in N.generators:
                    for g in G.generators:
                        if (g * n * ~g) not in N:
                            normal = False
                            break
                    if not normal:
                        break
                
                if normal:
                    # Check if N \cap H = {e}
                    N_elems = set(N.elements)
                    H_elems = set(H.elements)
                    if len(N_elems.intersection(H_elems)) == 1:
                        # Check if G = NH (order condition)
                        if G.order() == N.order() * H.order():
                            h2 = True
    except Exception:
        h2 = False

    # H3: e_N is the identity element of N
    try:
        h3 = (e_N == N.identity)
    except Exception:
        h3 = False

    # neg_Q: The stabilizer of e_N under this action is NOT exactly H
    try:
        stab = set()
        for g in G.elements:
            if callable(action):
                res = action(g, e_N)
            else:
                res = action[g][e_N]
            
            if res == e_N:
                stab.add(g)
                
        neg_q = (stab != set(H.elements))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: N and H are groups",
    "H_2: G is the semidirect product of N and H",
    "H_3: e_N is the identity element of N",
    "¬Q: The stabilizer of e_N under the action is not exactly H"
]

N_HYP = 3
NEG_Q_INDEX = 3