import sympy
from sympy.combinatorics.named_groups import AlternatingGroup, CyclicGroup, SymmetricGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
import itertools
import functools
import math

def direct_product(G1, G2):
    deg1 = G1.degree
    deg2 = G2.degree
    gens = []
    for g in G1.generators:
        arr = g.array_form
        arr = arr + list(range(len(arr), deg1))
        gens.append(Permutation(arr + list(range(deg1, deg1 + deg2))))
    for g in G2.generators:
        arr = g.array_form
        arr = arr + list(range(len(arr), deg2))
        gens.append(Permutation(list(range(deg1)) + [x + deg1 for x in arr]))
    return PermutationGroup(gens)

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
DirectProduct = direct_product

def get_normal_subgroup_of_index(G, p, elements):
    n_elements = len(elements)
    if p <= 0 or n_elements % p != 0:
        return False
    target_order = n_elements // p
    
    identity = None
    for e in elements:
        if getattr(e, 'is_Identity', False):
            identity = e
            break
    if identity is None:
        for e in elements:
            if all(e * x == x for x in elements):
                identity = e
                break
                
    if identity is None:
        return False
        
    classes = []
    unseen = set(elements)
    while unseen:
        x = unseen.pop()
        cclass = set()
        for g in elements:
            conj = g * x * (g**-1)
            cclass.add(conj)
        classes.append(list(cclass))
        unseen -= cclass
        
    id_class = None
    other_classes = []
    for c in classes:
        if len(c) == 1 and c[0] == identity:
            id_class = c
        else:
            other_classes.append(c)
            
    if id_class is None:
        return False
        
    other_classes.sort(key=len, reverse=True)
        
    def check_subgroup(subset_classes):
        subgroup_elements = set(id_class)
        for c in subset_classes:
            subgroup_elements.update(c)
        for a in subgroup_elements:
            for b in subgroup_elements:
                if a * b not in subgroup_elements:
                    return False
        return True

    def find_combinations(classes, target, current_combo, index):
        if target == 0:
            return check_subgroup(current_combo)
        if target < 0 or index >= len(classes):
            return False
        
        if find_combinations(classes, target - len(classes[index]), current_combo + [classes[index]], index + 1):
            return True
        if find_combinations(classes, target, current_combo, index + 1):
            return True
        return False

    return find_combinations(other_classes, target_order - 1, [], 0)

def conditions(witness):
    if isinstance(witness, tuple):
        G, p = witness
    else:
        G = witness
        p = None
        
    try:
        elements = list(G.generate())
        order = len(elements)
    except Exception:
        elements = []
        order = 0

    if p is None and order > 0:
        try:
            for test_p in range(2, order):
                temp = order
                n = 0
                while temp % test_p == 0:
                    temp //= test_p
                    n += 1
                if temp == 1 and n >= 1:
                    if not get_normal_subgroup_of_index(G, test_p, elements):
                        p = test_p
                        break
            if p is None:
                p = order
        except Exception:
            p = 2

    # H1: F is a field
    h1 = True
    
    # H2: E is a finite Galois extension of F
    try:
        h2 = order > 0
    except Exception:
        h2 = False
        
    # H3: The Galois group Gal(E/F) is a p-group of order p^n for some integer n >= 1
    try:
        if p is not None and p > 1 and order > 0:
            temp = order
            n = 0
            while temp % p == 0:
                temp //= p
                n += 1
            h3 = (temp == 1 and n >= 1)
        else:
            h3 = False
    except Exception:
        h3 = False
        
    # neg_Q: There does not exist an intermediate field K between F and E such that K/F is a Galois extension of degree p
    try:
        if p is not None and p > 1 and order > 0:
            has_norm = get_normal_subgroup_of_index(G, p, elements)
            neg_q = not has_norm
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: E is a finite Galois extension of F",
    "H_3: The Galois group Gal(E/F) is a p-group of order p^n for some integer n >= 1",
    "¬Q: There does not exist an intermediate field K between F and E such that K/F is a Galois extension of degree p"
]

N_HYP = 3
NEG_Q_INDEX = 3