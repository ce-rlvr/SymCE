import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import itertools

# Top-level setup
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

def get_elements(obj):
    if hasattr(obj, 'elements'):
        return list(obj.elements)
    elif hasattr(obj, 'generate'):
        return list(obj.generate())
    elif isinstance(obj, (list, set, tuple)):
        return list(obj)
    return []

def is_group(G):
    if isinstance(G, PermutationGroup):
        return True
    if hasattr(G, 'is_group') and G.is_group:
        return True
    els = get_elements(G)
    if not els: return False
    
    for a in els:
        for b in els:
            if a * b not in els:
                return False
                
    identities = []
    for e in els:
        if all(e * a == a and a * e == a for a in els):
            identities.append(e)
    if not identities:
        return False
    e = identities[0]
    
    for a in els:
        has_inv = False
        for b in els:
            if a * b == e and b * a == e:
                has_inv = True
                break
        if not has_inv:
            return False
            
    return True

def is_subgroup(sub, group_els):
    sub_els = get_elements(sub)
    if not sub_els: return False
    for s in sub_els:
        if s not in group_els: return False
    for s1 in sub_els:
        for s2 in sub_els:
            if s1 * s2 not in sub_els: return False
            
    identities = [e for e in group_els if all(e * a == a and a * e == a for a in group_els)]
    if not identities: return False
    e = identities[0]
    
    if e not in sub_els: return False
    
    for s in sub_els:
        has_inv = False
        for inv in sub_els:
            if s * inv == e and inv * s == e:
                has_inv = True
                break
        if not has_inv: return False
        
    return True

def conditions(witness):
    try:
        G = witness['G']
        H = witness['H']
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = is_group(G) and is_group(H)
    except Exception:
        h1 = False

    try:
        phi = witness['phi']
        G_els = get_elements(G)
        H_els = get_elements(H)
        h2 = True
        for g in G_els:
            val = phi(g) if callable(phi) else phi[g]
            if val not in H_els:
                h2 = False
                break
        if h2:
            for g1 in G_els:
                for g2 in G_els:
                    val1 = phi(g1) if callable(phi) else phi[g1]
                    val2 = phi(g2) if callable(phi) else phi[g2]
                    val12 = phi(g1 * g2) if callable(phi) else phi[g1 * g2]
                    if val12 != val1 * val2:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    try:
        A = witness['A']
        B = witness['B']
        G_els = get_elements(G)
        h3 = is_subgroup(A, G_els) and is_subgroup(B, G_els)
    except Exception:
        h3 = False

    try:
        A_els = get_elements(A)
        B_els = get_elements(B)
        
        AB = []
        for a in A_els:
            for b in B_els:
                AB.append(a * b)
                
        phi_AB = []
        for x in AB:
            val = phi(x) if callable(phi) else phi[x]
            if val not in phi_AB:
                phi_AB.append(val)
            
        phi_A = []
        for a in A_els:
            val = phi(a) if callable(phi) else phi[a]
            if val not in phi_A:
                phi_A.append(val)
            
        phi_B = []
        for b in B_els:
            val = phi(b) if callable(phi) else phi[b]
            if val not in phi_B:
                phi_B.append(val)
            
        phi_A_phi_B = []
        for x in phi_A:
            for y in phi_B:
                prod = x * y
                if prod not in phi_A_phi_B:
                    phi_A_phi_B.append(prod)
                    
        def is_equal_sets(list1, list2):
            for item in list1:
                if item not in list2: return False
            for item in list2:
                if item not in list1: return False
            return True
            
        q = is_equal_sets(phi_AB, phi_A_phi_B)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: phi: G -> H is a group homomorphism",
    "H_3: A and B are subgroups of G",
    "¬Q: The image phi(AB) is not equal to the set product phi(A)phi(B)"
]

N_HYP = 3
NEG_Q_INDEX = 3