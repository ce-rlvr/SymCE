import sympy
from sympy.matrices import Matrix, eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
import itertools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_elements(G):
    if hasattr(G, 'elements'):
        return list(G.elements)
    elif hasattr(G, 'is_Group') and G.is_Group:
        return list(G.elements)
    else:
        return list(G)

def conditions(witness):
    try:
        G, a, b = witness
    except Exception:
        return [False, False, False]
        
    try:
        G_elements = get_elements(G)
    except Exception:
        return [False, False, False]
        
    try:
        h1 = a in G_elements
    except Exception:
        h1 = False
        
    try:
        h2 = b in G_elements
    except Exception:
        h2 = False
        
    try:
        # Find the identity element in G
        identities = []
        for e in G_elements:
            is_id = True
            for z in G_elements:
                if e * z != z or z * e != z:
                    is_id = False
                    break
            if is_id:
                identities.append(e)
                
        if not identities:
            is_conj = False
        else:
            e = identities[0]
            # Find all invertible elements in G
            invertibles = []
            for g in G_elements:
                for h in G_elements:
                    if g * h == e and h * g == e:
                        invertibles.append((g, h))
                        break
            
            # Check if a and b are conjugate in G
            is_conj = False
            for g, h in invertibles:
                if a == g * b * h:
                    is_conj = True
                    break
                    
        # Check if there exist x, y in G such that a = xy and b = yx
        exists = False
        for x in G_elements:
            for y in G_elements:
                if a == x * y and b == y * x:
                    exists = True
                    break
            if exists:
                break
                
        # The conclusion fails if the equivalence does not hold
        neg_q = bool(is_conj != exists)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a is an element of G",
    "H_2: b is an element of G",
    "¬Q: The equivalence between conjugacy in G and the existence of x, y in G such that a=xy and b=yx does not hold"
]

N_HYP = 2
NEG_Q_INDEX = 2