import sympy
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: P is a Sylow 2-subgroup of G
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, P = witness
        else:
            G = witness
            P = G.sylow_subgroup(2)
            
        is_sub = all(G.contains(h) for h in P.generators)
        if not is_sub:
            h1 = False
        else:
            order_G = G.order()
            order_P = P.order()
            # Check if order_P is a power of 2
            if order_P > 0 and (order_P & (order_P - 1)) == 0:
                # Check if it's the highest power of 2 dividing order_G
                if order_G % order_P == 0 and (order_G // order_P) % 2 != 0:
                    h1 = True
                else:
                    h1 = False
            else:
                h1 = False
    except Exception:
        h1 = False

    # ¬Q: P is not a normal subgroup of G or P is not isomorphic to the Klein four-group V_4
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, P = witness
        else:
            G = witness
            P = G.sylow_subgroup(2)
            
        # Check if P is a normal subgroup of G
        normal = True
        for g in G.generators:
            for h in P.generators:
                if not P.contains(g * h * ~g):
                    normal = False
                    break
            if not normal:
                break
        
        # Check if P is isomorphic to V_4
        # V_4 has order 4 and all its elements have order 1 or 2
        is_V4 = False
        if P.order() == 4:
            is_V4 = True
            for elem in P.generate():
                if elem.order() not in (1, 2):
                    is_V4 = False
                    break
                    
        q = normal and is_V4
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P is a Sylow 2-subgroup of G",
    "¬Q: P is not a normal subgroup of G or P is not isomorphic to the Klein four-group V_4"
]

N_HYP = 1
NEG_Q_INDEX = 1