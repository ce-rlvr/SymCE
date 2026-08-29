import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.ntheory import isprime

# Top-level setup: standard finite groups
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
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])

def apply_f(f, x):
    if isinstance(f, dict):
        return f[x]
    return f(x)

def conditions(witness) -> list[bool]:
    try:
        G, H, p, f, P = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        if hasattr(P, 'generate'):
            P_elements = list(P.generate())
        else:
            P_elements = list(P)
    except Exception:
        P_elements = []

    # H_1: G and H are finite groups and P is a subgroup of G
    try:
        h1_G = hasattr(G, 'generate') and hasattr(G, 'order')
        h1_H = hasattr(H, 'generate') and hasattr(H, 'order')
        
        if hasattr(P, 'is_subgroup') and isinstance(G, PermutationGroup):
            P_is_subgroup = P.is_subgroup(G)
        else:
            G_elements_set = set(G.generate())
            P_is_subgroup = all(x in G_elements_set for x in P_elements)
            if P_is_subgroup and len(P_elements) > 0:
                P_set = set(P_elements)
                for a in P_set:
                    for b in P_set:
                        if a * b not in P_set:
                            P_is_subgroup = False
                            break
                    if not P_is_subgroup:
                        break
            elif len(P_elements) == 0:
                P_is_subgroup = False
                
        h1 = bool(h1_G and h1_H and P_is_subgroup)
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    # H_3: f: G -> H is a surjective group homomorphism
    try:
        G_elements = list(G.generate())
        H_elements = list(H.generate())
        
        is_hom = True
        for a in G_elements:
            for b in G_elements:
                if apply_f(f, a * b) != apply_f(f, a) * apply_f(f, b):
                    is_hom = False
                    break
            if not is_hom:
                break
        
        if is_hom:
            image_elements = set(apply_f(f, a) for a in G_elements)
            is_surj = (image_elements == set(H_elements))
        else:
            is_surj = False
            
        h3 = bool(is_hom and is_surj)
    except Exception:
        h3 = False

    # ¬Q: The image f(P) is not a Sylow p-subgroup of H
    try:
        f_P_elements = set(apply_f(f, a) for a in P_elements)
        
        order_H = H.order()
        highest_power = 1
        temp = order_H
        if isinstance(p, (int, sympy.Integer)) and p > 1:
            while temp % p == 0:
                highest_power *= p
                temp //= p
            is_sylow = (len(f_P_elements) == highest_power)
        else:
            is_sylow = False
            
        neg_q = not is_sylow
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are finite groups and P is a subgroup of G",
    "H_2: p is a prime number",
    "H_3: f: G -> H is a surjective group homomorphism",
    "¬Q: The image f(P) is not a Sylow p-subgroup of H"
]

N_HYP = 3
NEG_Q_INDEX = 3