import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

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

def conditions(witness):
    try:
        G, p, P = witness
    except Exception:
        return [False, False, False]
    
    # H1: G is a finite group, p is a prime, and P is a group
    try:
        h1 = isinstance(G, PermutationGroup) and isprime(p) and isinstance(P, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: P is a subgroup of G and Z(G) is the center of G
    try:
        h2 = h1 and P.is_subgroup(G)
    except Exception:
        h2 = False
        
    # neg_Q: P \cap Z(G) is NOT the unique Sylow p-subgroup of Z(G)
    try:
        if not h2:
            neg_q = False
        else:
            Z_G = G.center()
            
            def get_elements(group):
                try:
                    return set(group.generate_dimino())
                except Exception:
                    return set(group.elements)
            
            elems_P = get_elements(P)
            elems_ZG = get_elements(Z_G)
            
            # Intersection of P and Z(G)
            common_elems = elems_P.intersection(elems_ZG)
            
            # Unique Sylow p-subgroup of the abelian group Z(G)
            sylow_elems = set()
            for g in elems_ZG:
                o = g.order()
                temp = o
                while temp > 1 and temp % p == 0:
                    temp //= p
                if temp == 1:
                    sylow_elems.add(g)
                    
            # The conclusion holds if the intersection equals the Sylow p-subgroup
            is_same = (common_elems == sylow_elems)
            neg_q = not is_same
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group, p is a prime, and P is a group",
    "H_2: P is a subgroup of G and Z(G) is the center of G",
    "¬Q: P \\cap Z(G) is not the unique Sylow p-subgroup of Z(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2