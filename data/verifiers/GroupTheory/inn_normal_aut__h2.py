import sympy
from sympy.combinatorics import PermutationGroup, Permutation, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from itertools import permutations

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_inn(G, elements):
    inns = []
    for g in elements:
        mapping = []
        for x in elements:
            val = g * x * g**-1
            mapping.append(elements.index(val))
        inns.append(Permutation(mapping))
    return PermutationGroup(inns)

def get_aut(G, elements):
    n = len(elements)
    auts = []
    
    id_idx = -1
    for i, e in enumerate(elements):
        if e * elements[0] == elements[0]:
            id_idx = i
            break
            
    mult_table = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            mult_table[i][j] = elements.index(elements[i] * elements[j])
            
    for p in permutations(range(n)):
        if p[id_idx] != id_idx:
            continue
            
        is_homo = True
        for i in range(n):
            pi = p[i]
            for j in range(n):
                if mult_table[pi][p[j]] != p[mult_table[i][j]]:
                    is_homo = False
                    break
            if not is_homo:
                break
                
        if is_homo:
            auts.append(Permutation(list(p)))
            
    if not auts:
        return None
    return PermutationGroup(auts)

def conditions(witness):
    # Check if witness is provided as a tuple (G, Inn_G, Aut_G)
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, Inn_G, Aut_G = witness
            h1 = isinstance(G, PermutationGroup)
            h2 = isinstance(Inn_G, PermutationGroup) and isinstance(Aut_G, PermutationGroup)
            if h2:
                is_sub = True
                for gen in Inn_G.generators:
                    if gen not in Aut_G:
                        is_sub = False
                        break
                if is_sub:
                    neg_q = not Aut_G.is_normal(Inn_G)
                else:
                    neg_q = True
            else:
                neg_q = False
            return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    # Otherwise, assume witness is just the group G
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    h2 = h1

    neg_q = False
    try:
        if h1:
            elements = list(witness.generate())
            n = len(elements)
            # Compute Aut(G) only for small groups to avoid timeouts.
            # For any valid group, Inn(G) is mathematically guaranteed to be a normal subgroup of Aut(G),
            # so neg_q will always correctly evaluate to False.
            if n <= 8:
                Inn_G = get_inn(witness, elements)
                Aut_G = get_aut(witness, elements)
                if Aut_G is not None:
                    is_sub = True
                    for gen in Inn_G.generators:
                        if gen not in Aut_G:
                            is_sub = False
                            break
                    if is_sub:
                        neg_q = not Aut_G.is_normal(Inn_G)
                    else:
                        neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: Inn(G) is the group of inner automorphisms of G",
    "¬Q: Inn(G) is not a normal subgroup of Aut(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2