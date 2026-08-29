import sympy
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
    # H_1: The nilpotency class of G is exactly 2
    try:
        is_nilp = getattr(witness, "is_nilpotent", False)
        if callable(is_nilp):
            is_nilp = is_nilp()
        
        if is_nilp:
            nc = getattr(witness, "nilpotency_class", None)
            if callable(nc):
                nc = nc()
            h1 = (nc == 2)
        else:
            h1 = False
    except Exception:
        h1 = False

    # neg_Q: The quotient group G/Z(G) is NOT a non-trivial abelian group
    # i.e., it is either trivial or not abelian.
    try:
        Z = getattr(witness, "center")
        if callable(Z): 
            Z = Z()
        
        D = getattr(witness, "derived_subgroup")
        if callable(D): 
            D = D()
        
        g_order = getattr(witness, "order")
        if callable(g_order): 
            g_order = g_order()
        
        z_order = getattr(Z, "order")
        if callable(z_order): 
            z_order = z_order()
        
        # G/Z(G) is non-trivial iff |G| > |Z(G)|
        is_non_trivial = (g_order > z_order)
        
        # G/Z(G) is abelian iff the derived subgroup [G, G] is a subgroup of Z(G)
        is_abelian = all((g in Z) for g in D.generators)
        
        q = is_non_trivial and is_abelian
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The nilpotency class of G is exactly 2",
    "¬Q: The quotient group G/Z(G) is trivial or not abelian"
]

N_HYP = 1
NEG_Q_INDEX = 1