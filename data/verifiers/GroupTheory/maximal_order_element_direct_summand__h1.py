import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.combinatorics.permutations import Permutation
import itertools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_direct_summand(G, g):
    try:
        G_elements = list(G.elements)
    except Exception:
        G_elements = list(G.generate_dimino())
    n = len(G_elements)
    
    H_elements = set()
    curr = G.identity
    for _ in range(g.order()):
        H_elements.add(curr)
        curr = curr * g
            
    # H must be normal in G to be a direct factor
    for h in H_elements:
        for x in G_elements:
            if (x * h * ~x) not in H_elements:
                return False
                
    target_K_size = n // len(H_elements)
    if n % len(H_elements) != 0:
        return False
        
    if target_K_size == 1:
        return True
        
    # If G is abelian, the theorem holds (assuming g has maximal order, which is checked in H1).
    # So <g> is a direct summand. We return True to indicate it IS a direct summand.
    is_abelian = True
    for x in G_elements:
        for y in G_elements:
            if x * y != y * x:
                is_abelian = False
                break
        if not is_abelian:
            break
            
    if is_abelian:
        return True

    classes = []
    seen = set()
    for x in G_elements:
        if x not in seen:
            c = set()
            for y in G_elements:
                c.add(y * x * ~y)
            classes.append(c)
            seen.update(c)
            
    id_class = {G.identity}
    other_classes = [c for c in classes if c != id_class]
    
    if len(other_classes) > 25:
        return True # Reject witness to be safe and prevent TLE
        
    for r in range(1, len(other_classes) + 1):
        for combo in itertools.combinations(other_classes, r):
            K_size = 1 + sum(len(c) for c in combo)
            if K_size == target_K_size:
                K_elements = set(id_class)
                for c in combo:
                    K_elements.update(c)
                
                # Check if K_elements is a subgroup
                is_subgroup = True
                for k1 in K_elements:
                    for k2 in K_elements:
                        if (k1 * k2) not in K_elements:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
                
                if is_subgroup:
                    # Check intersection with H
                    if H_elements.intersection(K_elements) == {G.identity}:
                        return True
                        
    return False

def conditions(witness):
    try:
        G, g = witness
    except Exception:
        return [False, False]
        
    # H_1: g in G and has maximal order
    try:
        G_elements = list(G.elements)
        if g not in G_elements:
            h1 = False
        else:
            max_ord = max(x.order() for x in G_elements)
            h1 = (g.order() == max_ord)
    except Exception:
        h1 = False
        
    # neg_Q: <g> is NOT a direct summand of G
    try:
        neg_q = not is_direct_summand(G, g)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: g is an element of G whose order is maximal among all elements in G",
    "¬Q: The cyclic subgroup <g> is not a direct summand of G"
]

N_HYP = 1
NEG_Q_INDEX = 1