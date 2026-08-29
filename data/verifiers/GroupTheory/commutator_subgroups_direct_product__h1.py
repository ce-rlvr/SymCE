import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]])])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def is_subgroup(sub, supergroup):
    try:
        if sub.is_trivial:
            return True
        return all(supergroup.contains(g) for g in sub.generators)
    except Exception:
        return False

def commutator_subgroup(U, V, degree):
    try:
        if U.is_trivial or V.is_trivial:
            return PermutationGroup([Permutation(degree - 1)]) if degree > 0 else PermutationGroup([Permutation()])
        
        U_gens = list(U.generators)
        V_gens = list(V.generators)
        
        comm_gens = []
        for u in U_gens:
            for v in V_gens:
                c = u**-1 * v**-1 * u * v
                if not c.is_Identity:
                    comm_gens.append(c)
                    
        if not comm_gens:
            return PermutationGroup([Permutation(degree - 1)]) if degree > 0 else PermutationGroup([Permutation()])
            
        UV_gens = U_gens + V_gens
        
        closure_gens = list(comm_gens)
        closure_set = set(closure_gens)
        queue = list(comm_gens)
        
        while queue:
            curr = queue.pop(0)
            for g in UV_gens:
                conj1 = g**-1 * curr * g
                if conj1 not in closure_set:
                    closure_set.add(conj1)
                    closure_gens.append(conj1)
                    queue.append(conj1)
                conj2 = g * curr * g**-1
                if conj2 not in closure_set:
                    closure_set.add(conj2)
                    closure_gens.append(conj2)
                    queue.append(conj2)
                    
        aligned_gens = []
        for g in closure_gens:
            arr = g.array_form
            if len(arr) < degree:
                arr += list(range(len(arr), degree))
            aligned_gens.append(Permutation(arr))
            
        return PermutationGroup(aligned_gens)
    except Exception:
        return None

def direct_product(G1, G2, deg1, deg2):
    try:
        gens = []
        for g in G1.generators:
            if g.is_Identity:
                continue
            arr = g.array_form
            if len(arr) < deg1:
                arr += list(range(len(arr), deg1))
            arr += list(range(deg1, deg1 + deg2))
            gens.append(Permutation(arr))
        for g in G2.generators:
            if g.is_Identity:
                continue
            arr = list(range(deg1))
            arr2 = g.array_form
            if len(arr2) < deg2:
                arr2 += list(range(len(arr2), deg2))
            arr += [x + deg1 for x in arr2]
            gens.append(Permutation(arr))
            
        if not gens:
            if deg1 + deg2 <= 1:
                return PermutationGroup([Permutation()])
            return PermutationGroup([Permutation(deg1 + deg2 - 1)])
        return PermutationGroup(gens)
    except Exception:
        return None

def groups_equal(G1, G2):
    try:
        if G1 is None or G2 is None:
            return False
        return G1.is_subgroup(G2) and G2.is_subgroup(G1)
    except Exception:
        return False

def conditions(witness):
    try:
        G, H, A, B, C, D = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = is_subgroup(A, G) and is_subgroup(C, G)
    except Exception:
        h1 = False

    try:
        h2 = is_subgroup(B, H) and is_subgroup(D, H)
    except Exception:
        h2 = False

    try:
        degG = G.degree
        degH = H.degree
        
        AB = direct_product(A, B, degG, degH)
        CD = direct_product(C, D, degG, degH)
        
        LHS = commutator_subgroup(AB, CD, degG + degH)
        
        AC = commutator_subgroup(A, C, degG)
        BD = commutator_subgroup(B, D, degH)
        
        RHS = direct_product(AC, BD, degG, degH)
        
        neg_q = not groups_equal(LHS, RHS)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A and C are subgroups of G",
    "H_2: B and D are subgroups of H",
    "¬Q: commutator of A x B and C x D is not equal to commutator of A and C x commutator of B and D"
]

N_HYP = 2
NEG_Q_INDEX = 2