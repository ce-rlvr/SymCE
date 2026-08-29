import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    # Unpack witness. Expected to be a tuple (A, B, G) or a dict with these keys.
    try:
        if isinstance(witness, dict):
            A = witness['A']
            B = witness['B']
            G = witness['G']
        else:
            A, B, G = witness
    except Exception:
        return [False, False, False]
        
    # H_1: B is a finite abelian group
    try:
        h1 = bool(B.is_abelian)
    except Exception:
        h1 = False
        
    # H_2: G is a semidirect product of A and B
    try:
        h2 = False
        
        def get_order(grp):
            return grp.order() if callable(grp.order) else grp.order
            
        order_G = get_order(G)
        order_A = get_order(A)
        order_B = get_order(B)
        
        # For G to be a semidirect product of A and B, their orders must multiply to |G|
        if order_G == order_A * order_B:
            # A and B must be subgroups of G
            a_sub = all(G.contains(a) for a in A.generators)
            b_sub = all(G.contains(b) for b in B.generators)
            
            if a_sub and b_sub:
                # Check if A is normal in G
                a_normal = True
                for g in G.generators:
                    for a in A.generators:
                        if not A.contains(g * a * ~g):
                            a_normal = False
                            break
                    if not a_normal:
                        break
                
                # Check if B is normal in G (in case the roles are swapped)
                b_normal = True
                for g in G.generators:
                    for b in B.generators:
                        if not B.contains(g * b * ~g):
                            b_normal = False
                            break
                    if not b_normal:
                        break
                
                # If either is normal, and |G| = |A||B| with A, B <= G, 
                # then G is a semidirect product of A and B.
                if a_normal or b_normal:
                    h2 = True
    except Exception:
        h2 = False
        
    # ¬Q: G is not solvable
    try:
        neg_q = not bool(G.is_solvable)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: B is a finite abelian group",
    "H_2: G is a semidirect product of A and B",
    "¬Q: G is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2