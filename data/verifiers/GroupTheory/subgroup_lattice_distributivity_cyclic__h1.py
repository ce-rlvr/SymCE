import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def join_subgroups(A, B):
    gens = list(A | B)
    if not gens:
        return frozenset()
    closure = set(gens)
    queue = list(gens)
    while queue:
        x = queue.pop(0)
        for y in gens:
            xy = x * y
            if xy not in closure:
                closure.add(xy)
                queue.append(xy)
    return frozenset(closure)

def get_all_subgroups(G):
    elements = list(G.elements)
    subgroups = set()
    for g in elements:
        sg = set()
        curr = g
        while curr not in sg:
            sg.add(curr)
            curr = curr * g
        subgroups.add(frozenset(sg))
    
    while True:
        new_subgroups = set(subgroups)
        for A in subgroups:
            for B in subgroups:
                J = join_subgroups(A, B)
                new_subgroups.add(J)
        if len(new_subgroups) == len(subgroups):
            break
        subgroups = new_subgroups
    return list(subgroups)

def conditions(witness):
    try:
        H1 = isinstance(witness, PermutationGroup)
    except Exception:
        H1 = False

    try:
        if not H1:
            neg_Q = False
        else:
            try:
                order = witness.order()
            except Exception:
                try:
                    order = witness.order
                except Exception:
                    order = len(list(witness.elements))
            
            if int(order) > 60:
                neg_Q = False
            else:
                subgroups = get_all_subgroups(witness)
                
                join_cache = {}
                def get_join(X, Y):
                    if (X, Y) not in join_cache:
                        join_cache[(X, Y)] = join_subgroups(X, Y)
                    return join_cache[(X, Y)]
                
                is_dist = True
                for A in subgroups:
                    for B in subgroups:
                        for C in subgroups:
                            B_and_C = B.intersection(C)
                            left = get_join(A, B_and_C)
                            
                            A_or_B = get_join(A, B)
                            A_or_C = get_join(A, C)
                            right = A_or_B.intersection(A_or_C)
                            
                            if left != right:
                                is_dist = False
                                break
                        if not is_dist:
                            break
                    if not is_dist:
                        break
                
                neg_Q = not is_dist
    except Exception:
        neg_Q = False

    return [H1, neg_Q]

CONDITION_LABELS = [
    "H_1: L(G) is the lattice of subgroups of G ordered by inclusion",
    "¬Q: L(G) is not a distributive lattice"
]

N_HYP = 1
NEG_Q_INDEX = 1