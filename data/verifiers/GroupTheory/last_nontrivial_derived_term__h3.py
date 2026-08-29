import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
    try:
        G, d = witness
    except Exception:
        return [False, False, False]
    
    try:
        ds = G.derived_series()
    except Exception:
        ds = None

    # H_1: G is a solvable group
    try:
        h1 = bool(G.is_solvable)
    except Exception:
        h1 = False
        
    # H_2: d is the derived length of G
    try:
        if ds is not None:
            actual_d = len(ds) - 1
            h2 = (d == actual_d)
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # ¬Q: G^{(d-1)} is not a non-trivial abelian normal subgroup of G
    try:
        if ds is None:
            neg_q = False
        else:
            d_int = int(d)
            if d_int - 1 < 0:
                # For the trivial group, d=0, so G^{(-1)} is not defined / not a non-trivial subgroup.
                q = False
            else:
                H = ds[d_int - 1]
                is_non_trivial = (H.order() > 1)
                is_abelian = bool(H.is_abelian)
                
                is_normal = True
                for g in G.generators:
                    for h in H.generators:
                        # Check if g * h * g^-1 is in H
                        if not H.contains(g * h * ~g):
                            is_normal = False
                            break
                        # Check if g^-1 * h * g is in H
                        if not H.contains(~g * h * g):
                            is_normal = False
                            break
                    if not is_normal:
                        break
                
                q = is_non_trivial and is_abelian and is_normal
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a solvable group",
    "H_2: d is the derived length of G",
    "¬Q: G^{(d-1)} is not a non-trivial abelian normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2