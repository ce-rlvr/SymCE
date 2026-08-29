import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings that the witness expression may reference
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    """
    Given a witness (G, H, K), checks if it is a valid counterexample to the conjecture.
    The conjecture claims that if G is a group and K is a normal subgroup of G, 
    then the product HK is a normal subgroup of G.
    """
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: K is a normal subgroup of G
    try:
        h2 = isinstance(K, PermutationGroup) and K.is_subgroup(G) and K.is_normal(G)
    except Exception:
        h2 = False

    # neg_Q: HK is not a normal subgroup of G
    try:
        if hasattr(H, 'generate'):
            H_elems = list(H.generate())
        else:
            H_elems = list(H)
            
        if hasattr(K, 'generate'):
            K_elems = list(K.generate())
        else:
            K_elems = list(K)
            
        HK_elems = set()
        for h in H_elems:
            for k in K_elems:
                HK_elems.add(h * k)
                
        # Check if HK_elems forms a subgroup of G
        is_subgroup = True
        if not HK_elems:
            is_subgroup = False
        else:
            # For finite groups, closure under multiplication implies it's a subgroup
            for x in HK_elems:
                for y in HK_elems:
                    if x * y not in HK_elems:
                        is_subgroup = False
                        break
                if not is_subgroup:
                    break
                    
        if not is_subgroup:
            is_normal = False
        else:
            # Check if the subgroup HK is normal in G
            is_normal = True
            if hasattr(G, 'generate'):
                G_elems = list(G.generate())
            else:
                G_elems = list(G)
                
            for g in G_elems:
                g_inv = ~g
                for x in HK_elems:
                    if g * x * g_inv not in HK_elems:
                        is_normal = False
                        break
                if not is_normal:
                    break
                    
        neg_q = not is_normal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: K is a normal subgroup of G",
    "¬Q: HK is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2