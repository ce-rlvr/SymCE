import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Isomorphic to the Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_inv(a):
    if isinstance(a, Permutation):
        return ~a
    try:
        return a**-1
    except Exception:
        pass
    try:
        return a.inv()
    except Exception:
        pass
    try:
        return ~a
    except Exception:
        return None

def get_elements(obj):
    if hasattr(obj, 'elements'):
        gen = obj.elements
    elif hasattr(obj, 'generate'):
        gen = obj.generate()
    else:
        gen = obj
    
    res = set()
    for x in gen:
        try:
            hash(x)
            res.add(x)
        except TypeError:
            if hasattr(x, 'as_immutable'):
                res.add(x.as_immutable())
            else:
                raise
    return res

def is_group(elements):
    if not elements:
        return False
    for a in elements:
        try:
            a_inv = get_inv(a)
            if a_inv is None:
                return False
            try:
                hash(a_inv)
            except TypeError:
                if hasattr(a_inv, 'as_immutable'):
                    a_inv = a_inv.as_immutable()
            if a_inv not in elements:
                return False
                
            for b in elements:
                prod = a * b
                try:
                    hash(prod)
                except TypeError:
                    if hasattr(prod, 'as_immutable'):
                        prod = prod.as_immutable()
                if prod not in elements:
                    return False
        except Exception:
            return False
    return True

def is_normal_subgroup(G, N):
    if isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup):
        try:
            return G.is_normal(N)
        except Exception:
            pass
            
    # Fallback for sets, lists, or custom objects
    try:
        N_elements = get_elements(N)
        G_elements = get_elements(G)
        
        if not N_elements.issubset(G_elements):
            return False
            
        if not is_group(N_elements):
            return False
            
        for g in G_elements:
            g_inv = get_inv(g)
            if g_inv is None:
                return False
            for n in N_elements:
                prod = g * n * g_inv
                try:
                    hash(prod)
                except TypeError:
                    if hasattr(prod, 'as_immutable'):
                        prod = prod.as_immutable()
                if prod not in N_elements:
                    return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            N_list = witness.get('N_list')
        elif isinstance(witness, tuple) and len(witness) == 2:
            G, N_list = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
    
    # H1: I is a non-empty index set
    try:
        h1 = isinstance(N_list, (list, tuple, set)) and len(N_list) > 0
    except Exception:
        h1 = False

    # H2: For every i in I, N_i is a normal subgroup of G
    try:
        if not h1:
            h2 = False
        else:
            h2 = True
            for N in N_list:
                if not is_normal_subgroup(G, N):
                    h2 = False
                    break
    except Exception:
        h2 = False

    # neg_Q: The intersection of all N_i for i in I is NOT a normal subgroup of G
    try:
        if not h1:
            neg_q = False
        else:
            elements = get_elements(N_list[0])
            for N in N_list[1:]:
                elements = elements.intersection(get_elements(N))
            
            if not elements:
                neg_q = True
            else:
                neg_q = not is_normal_subgroup(G, elements)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: I is a non-empty index set",
    "H_2: For every i in I, N_i is a normal subgroup of G",
    "¬Q: The intersection of all N_i for i in I is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2