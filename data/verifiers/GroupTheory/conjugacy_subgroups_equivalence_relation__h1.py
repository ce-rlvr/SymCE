import sympy
from sympy.combinatorics import Permutation, PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import itertools

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_group(H_set):
    if not H_set:
        return False
    H_list = list(H_set)
    # Check closure
    for a in H_list:
        for b in H_list:
            try:
                if a * b not in H_set:
                    return False
            except Exception:
                return False
    # Check identity
    has_identity = False
    for e in H_list:
        try:
            if all(e * a == a and a * e == a for a in H_list):
                has_identity = True
                # Check inverses
                inverses_ok = True
                for a in H_list:
                    if not any(a * b == e and b * a == e for b in H_list):
                        inverses_ok = False
                        break
                if inverses_ok:
                    return True
        except Exception:
            continue
    return False

def get_all_subgroups_fast(G_set):
    G_list = list(G_set)
    if not G_list:
        return []
    
    # Check if all elements are permutations
    if all(isinstance(g, Permutation) for g in G_list):
        try:
            parent = PermutationGroup(G_list)
            if parent.order() < 10000:
                all_subs = parent.subgroups()
                subgroups = []
                for sg in all_subs:
                    sg_set = set(sg.elements)
                    if sg_set.issubset(G_set):
                        subgroups.append(sg_set)
                return subgroups
        except Exception:
            pass

    # Fallback for small sets
    if len(G_list) <= 12:
        subgroups = []
        for r in range(1, len(G_list) + 1):
            for subset in itertools.combinations(G_list, r):
                subset_set = set(subset)
                if is_group(subset_set):
                    subgroups.append(subset_set)
        return subgroups
    
    return None

def is_conjugate(H_set, K_set, G_set):
    for g in G_set:
        try:
            g_inv = g**-1
        except Exception:
            if hasattr(g, 'inv'):
                try:
                    g_inv = g.inv()
                except Exception:
                    continue
            else:
                continue
        
        conj = set()
        try:
            for h in H_set:
                conj.add(g * h * g_inv)
        except Exception:
            continue
            
        if conj == K_set:
            return True
    return False

def is_equivalence_relation(S_sets, G_set):
    # Reflexive
    for H in S_sets:
        if not is_conjugate(H, H, G_set):
            return False
    # Symmetric
    for H in S_sets:
        for K in S_sets:
            if is_conjugate(H, K, G_set):
                if not is_conjugate(K, H, G_set):
                    return False
    # Transitive
    for H in S_sets:
        for K in S_sets:
            for L in S_sets:
                if is_conjugate(H, K, G_set) and is_conjugate(K, L, G_set):
                    if not is_conjugate(H, L, G_set):
                        return False
    return True

def conditions(witness) -> list[bool]:
    try:
        G, S = witness
    except Exception:
        return [False, False]
    
    try:
        if hasattr(G, 'elements'):
            G_set = set(G.elements)
        else:
            G_set = set(G)
            
        S_sets = []
        for H in S:
            if hasattr(H, 'elements'):
                S_sets.append(set(H.elements))
            else:
                S_sets.append(set(H))
    except Exception:
        return [False, False]
        
    try:
        unique_S_sets = []
        for s in S_sets:
            if s not in unique_S_sets:
                unique_S_sets.append(s)
                
        expected_subgroups = get_all_subgroups_fast(G_set)
        if expected_subgroups is None:
            h1 = False
        else:
            def sets_equal(list1, list2):
                if len(list1) != len(list2):
                    return False
                for s1 in list1:
                    if s1 not in list2:
                        return False
                for s2 in list2:
                    if s2 not in list1:
                        return False
                return True
            
            h1 = sets_equal(unique_S_sets, expected_subgroups)
    except Exception:
        h1 = False

    try:
        neg_q = not is_equivalence_relation(unique_S_sets, G_set)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: S is the set of all subgroups of G",
    "¬Q: The relation H ~ K iff exists g in G, gHg^-1 = K is not an equivalence relation on S"
]

N_HYP = 1
NEG_Q_INDEX = 1