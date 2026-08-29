import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
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

def is_semisimple(G):
    """
    A finite group is semisimple if it has no non-trivial abelian normal subgroups.
    This is equivalent to having a trivial solvable radical.
    We check this by verifying that no non-trivial conjugacy class has mutually commuting elements.
    """
    if G.order() == 1:
        return True
    
    tested = set()
    
    for g in G.generate():
        if g.is_Identity or g in tested:
            continue
            
        # Find the conjugacy class of g
        conjugates = {g}
        queue = [g]
        while queue:
            curr = queue.pop(0)
            for h in G.generators:
                conj1 = h * curr * ~h
                if conj1 not in conjugates:
                    conjugates.add(conj1)
                    queue.append(conj1)
                conj2 = ~h * curr * h
                if conj2 not in conjugates:
                    conjugates.add(conj2)
                    queue.append(conj2)
                    
        tested.update(conjugates)
        
        # Check if all elements in the conjugacy class commute with each other.
        # If they do, they generate an abelian normal subgroup.
        conjugates_list = list(conjugates)
        is_abelian = True
        for i in range(len(conjugates_list)):
            for j in range(i + 1, len(conjugates_list)):
                if conjugates_list[i] * conjugates_list[j] != conjugates_list[j] * conjugates_list[i]:
                    is_abelian = False
                    break
            if not is_abelian:
                break
                
        if is_abelian:
            return False
            
    return True

def is_subgroup(H, G):
    try:
        if H.order() > G.order():
            return False
        if G.order() % H.order() != 0:
            return False
        for g in H.generators:
            if g not in G:
                return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: G is a semisimple group
    try:
        h2 = h1 and is_semisimple(G)
    except Exception:
        h2 = False
        
    # H_3: H is a proper subgroup of G
    try:
        h3 = isinstance(H, PermutationGroup) and is_subgroup(H, G) and H.order() < G.order()
    except Exception:
        h3 = False
        
    # neg_Q: The index of H in G is <= 4
    try:
        if h1 and h3:
            index = G.order() // H.order()
            neg_q = bool(index <= 4)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a semisimple group",
    "H_3: H is a proper subgroup of G",
    "¬Q: The index of H in G is <= 4"
]

N_HYP = 3
NEG_Q_INDEX = 3