import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1) * Permutation(2, 3), Permutation(0, 2) * Permutation(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: L/K is a finite Galois extension",
    "H_2: E is an intermediate field between K and L",
    "H_3: H is the subgroup of G fixing E",
    "¬Q: The number of distinct intermediate fields conjugate to E over K is NOT equal to the index of N_G(H) in G"
]

N_HYP = 3
NEG_Q_INDEX = 3

def make_immutable(e):
    try:
        hash(e)
        return e
    except TypeError:
        if hasattr(e, 'as_immutable'):
            return e.as_immutable()
        try:
            return tuple(e)
        except Exception:
            return str(e)

def get_inverse(g):
    try:
        return ~g
    except Exception:
        return g**-1

def get_elements_and_check_group(group):
    if hasattr(group, 'generate'):
        elements = []
        for e in group.generate():
            elements.append(e)
            if len(elements) > 1000:
                raise ValueError("Group too large")
        return elements, True
    else:
        elements = list(group)
        if not elements:
            return elements, False
        if len(elements) > 500:
            raise ValueError("Group too large")
        
        imm_elements = set(make_immutable(e) for e in elements)
        for a in elements:
            for b in elements:
                if make_immutable(a * b) not in imm_elements:
                    return elements, False
        return elements, True

def is_subset(sub_elements, super_elements):
    super_imm = set(make_immutable(e) for e in super_elements)
    for e in sub_elements:
        if make_immutable(e) not in super_imm:
            return False
    return True

def get_intersection(elements1, elements2):
    imm2 = set(make_immutable(e) for e in elements2)
    intersection = []
    for e in elements1:
        if make_immutable(e) in imm2:
            intersection.append(e)
    return intersection

def are_equal_sets(elements1, elements2):
    imm1 = set(make_immutable(e) for e in elements1)
    imm2 = set(make_immutable(e) for e in elements2)
    return imm1 == imm2

def conditions(witness):
    """
    Expected witness format:
    A tuple (Gal, E_group, G, H) or a dict with these keys, where:
    - Gal is a PermutationGroup representing Gal(L/K)
    - E_group is a subgroup of Gal representing Gal(L/E)
    - G is a subgroup of Gal representing the group G
    - H is a subgroup of G representing the subgroup fixing E (i.e., G \cap E_group)
    """
    try:
        if isinstance(witness, dict):
            Gal = witness.get('Gal')
            E_group = witness.get('E_group')
            G = witness.get('G')
            H = witness.get('H')
        elif isinstance(witness, tuple):
            if len(witness) == 4:
                Gal, E_group, G, H = witness
            elif len(witness) == 3:
                Gal, E_group, G = witness
                H = None
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: L/K is a finite Galois extension
    try:
        Gal_elements, gal_is_group = get_elements_and_check_group(Gal)
        h1 = gal_is_group and len(Gal_elements) > 0
    except Exception:
        h1 = False

    # H2: E is an intermediate field between K and L
    try:
        E_elements, e_is_group = get_elements_and_check_group(E_group)
        h2 = e_is_group and is_subset(E_elements, Gal_elements)
    except Exception:
        h2 = False

    # H3: H is the subgroup of G fixing E
    try:
        G_elements, g_is_group = get_elements_and_check_group(G)
        g_is_sub = g_is_group and is_subset(G_elements, Gal_elements)
        
        if H is not None:
            H_elements, h_is_group = get_elements_and_check_group(H)
            intersection = get_intersection(G_elements, E_elements)
            h_is_intersection = are_equal_sets(H_elements, intersection)
            h3 = g_is_sub and h_is_group and h_is_intersection
        else:
            H_elements = get_intersection(G_elements, E_elements)
            h3 = g_is_sub
    except Exception:
        h3 = False

    # Conclusion: The number of distinct intermediate fields conjugate to E over K 
    # is equal to the index [G : N_G(H)]
    try:
        if not (h1 and h2 and h3):
            neg_q = False
        else:
            # Number of distinct intermediate fields conjugate to E over K
            # This corresponds to the number of conjugate subgroups of E_group in Gal
            conjugates = set()
            for g in Gal_elements:
                g_inv = get_inverse(g)
                conj = frozenset([make_immutable(g * e * g_inv) for e in E_elements])
                conjugates.add(conj)
            num_conjugate_fields = len(conjugates)
            
            # Index [G : N_G(H)]
            n_g_h_size = 0
            H_imm = set([make_immutable(h) for h in H_elements])
            for g in G_elements:
                g_inv = get_inverse(g)
                conj = set([make_immutable(g * h * g_inv) for h in H_elements])
                if conj == H_imm:
                    n_g_h_size += 1
                    
            index = len(G_elements) // n_g_h_size
            
            neg_q = (num_conjugate_fields != index)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]