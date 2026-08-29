import itertools
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    try:
        if len(witness) == 2:
            G, A = witness
        elif len(witness) >= 3:
            G, A = witness[0], witness[1]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(A.is_abelian)
    except Exception:
        h1 = False

    try:
        is_subgroup = True
        for g in A.generators:
            if not G.contains(g):
                is_subgroup = False
                break
                
        if is_subgroup:
            is_normal = True
            for g in G.generators:
                for a in A.generators:
                    if not A.contains(g * a * g**-1):
                        is_normal = False
                        break
                if not is_normal:
                    break
        else:
            is_normal = False
            
        h2 = bool(is_subgroup and is_normal)
    except Exception:
        h2 = False

    try:
        if not h2:
            neg_q = False
        else:
            A_elements = list(A.elements)
            A_set = set(A_elements)
            G_elements = list(G.elements)
            
            transversals = []
            for g in G_elements:
                found = False
                for t in transversals:
                    if (g * t**-1) in A_set:
                        found = True
                        break
                if not found:
                    transversals.append(g)
                    
            Q_size = len(transversals)
            
            Q_mult = {}
            for i in range(Q_size):
                for j in range(Q_size):
                    prod = transversals[i] * transversals[j]
                    for k in range(Q_size):
                        if (prod * transversals[k]**-1) in A_set:
                            Q_mult[(i, j)] = k
                            break
                            
            coset_elements = []
            for i in range(Q_size):
                coset_elements.append([a * transversals[i] for a in A_elements])
                
            splits = False
            for section in itertools.product(*coset_elements):
                is_hom = True
                for i in range(Q_size):
                    for j in range(Q_size):
                        if section[i] * section[j] != section[Q_mult[(i, j)]]:
                            is_hom = False
                            break
                    if not is_hom:
                        break
                if is_hom:
                    splits = True
                    break
                    
            c = {}
            for i in range(Q_size):
                for j in range(Q_size):
                    c[(i, j)] = transversals[i] * transversals[j] * transversals[Q_mult[(i, j)]]**-1
                    
            c_is_zero = False
            for f in itertools.product(A_elements, repeat=Q_size):
                is_coboundary = True
                for i in range(Q_size):
                    for j in range(Q_size):
                        expected = f[i] * f[j] * f[Q_mult[(i, j)]]**-1
                        if c[(i, j)] != expected:
                            is_coboundary = False
                            break
                    if not is_coboundary:
                        break
                if is_coboundary:
                    c_is_zero = True
                    break
                    
            neg_q = bool(splits != c_is_zero)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = ["H_1: A is an abelian group", "H_2: 1 -> A -> G -> Q -> 1 is a short exact sequence", "¬Q: The sequence splits iff c is the identity element in H^2(Q, A) is FALSE"]
N_HYP = 2
NEG_Q_INDEX = 2