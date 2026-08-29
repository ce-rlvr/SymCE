import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # Parse witness
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            x = witness.get('x')
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                G, H, x = witness
            elif len(witness) == 4:
                G, X, H, x = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a group acting on a set X
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(x, (int, sympy.Integer)) and 0 <= x < G.degree
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        h2 = isinstance(H, PermutationGroup) and all(g in G for g in H.generators)
    except Exception:
        h2 = False

    # ¬Q: It is not the case that H acts transitively on the G-orbit of x if and only if G = H G_x
    try:
        G_orbit = set(G.orbit(x))
        
        # Handle potential degree mismatch if H was defined on a smaller domain
        try:
            H_orbit = set(H.orbit(x))
        except Exception:
            H_orbit = {x}
            
        H_acts_transitively = (H_orbit == G_orbit)
        
        G_x = G.stabilizer(x)
        
        try:
            H_x = H.stabilizer(x)
        except Exception:
            H_x = H
            
        # The size of the set product H G_x is |H| * |G_x| / |H \cap G_x|
        H_G_x_size = (H.order() * G_x.order()) // H_x.order()
        
        # Since H G_x is a subset of G, it equals G if and only if their sizes are equal
        G_eq_H_G_x = (H_G_x_size == G.order())
        
        Q = (H_acts_transitively == G_eq_H_G_x)
        neg_q = not Q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: H is a subgroup of G",
    "¬Q: It is not the case that H acts transitively on the G-orbit of x if and only if G = H G_x"
]

N_HYP = 2
NEG_Q_INDEX = 2