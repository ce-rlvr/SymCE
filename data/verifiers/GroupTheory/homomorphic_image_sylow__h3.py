import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.ntheory import isprime

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
        if isinstance(witness, dict):
            G = witness['G']
            H = witness['H']
            p = witness['p']
            P = witness['P']
            f = witness['f']
        else:
            G, H, p, P, f = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G and H are finite groups
    try:
        order_G = G.order()
        order_H = H.order()
        h1 = isinstance(order_G, (int, sympy.Integer)) and isinstance(order_H, (int, sympy.Integer))
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    # H_3: P is a Sylow p-subgroup of G
    try:
        h3 = False
        if hasattr(P, 'generators') and hasattr(P, 'order'):
            # Check if P is a subgroup of G
            is_sub = all(g in G for g in P.generators)
            if is_sub:
                order_P = P.order()
                order_G = G.order()
                
                # Calculate highest power of p dividing order_G
                k = 0
                temp = order_G
                while temp % p == 0:
                    k += 1
                    temp //= p
                    
                if order_P == p**k:
                    h3 = True
    except Exception:
        h3 = False

    # ¬Q: The image f(P) is not a Sylow p-subgroup of H
    try:
        neg_q = False
        img_P = set()
        
        if hasattr(P, 'generate'):
            elements = P.generate()
        elif hasattr(P, 'elements'):
            elements = P.elements
        else:
            elements = list(P)
            
        for x in elements:
            if isinstance(f, dict):
                img_P.add(f[x])
            else:
                img_P.add(f(x))
                
        is_sylow = True
        
        # 1. Check if all elements of f(P) are in H
        if is_sylow:
            for x in img_P:
                if x not in H:
                    is_sylow = False
                    break
                    
        # 2. Check if f(P) is closed under multiplication (hence a subgroup, since it's finite)
        if is_sylow:
            img_list = list(img_P)
            for a in img_list:
                for b in img_list:
                    if a * b not in img_P:
                        is_sylow = False
                        break
                if not is_sylow:
                    break
                    
        # 3. Check if the order of f(P) is the highest power of p dividing |H|
        if is_sylow:
            order_S = len(img_P)
            order_H = H.order()
            
            k = 0
            temp = order_H
            while temp % p == 0:
                k += 1
                temp //= p
                
            if order_S != p**k:
                is_sylow = False
                
        neg_q = not is_sylow
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are finite groups",
    "H_2: p is a prime number",
    "H_3: P is a Sylow p-subgroup of G",
    "¬Q: The image f(P) is not a Sylow p-subgroup of H"
]

N_HYP = 3
NEG_Q_INDEX = 3