import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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

def get_identity(G):
    if hasattr(G, 'identity'):
        return G.identity
    for g in G.elements:
        if g * g == g:
            return g
    return list(G.elements)[0] ** 0

def closure(subset):
    sub = list(subset)
    sub_set = set(subset)
    i = 0
    while i < len(sub):
        x = sub[i]
        for j in range(i + 1):
            y = sub[j]
            xy = x * y
            if xy not in sub_set:
                sub_set.add(xy)
                sub.append(xy)
            yx = y * x
            if yx not in sub_set:
                sub_set.add(yx)
                sub.append(yx)
        i += 1
    return frozenset(sub_set)

def all_subgroups(G):
    elements = list(G.elements)
    identity = get_identity(G)
    
    subgroups = set()
    for g in elements:
        sub = [identity]
        sub_set = {identity}
        curr = g
        while curr not in sub_set:
            sub.append(curr)
            sub_set.add(curr)
            curr = curr * g
        subgroups.add(frozenset(sub_set))
        
    frontier = list(subgroups)
    
    while frontier:
        curr = frontier.pop()
        for g in elements:
            if g not in curr:
                new_subset = list(curr) + [g]
                new_sub = closure(new_subset)
                if new_sub not in subgroups:
                    subgroups.add(new_sub)
                    frontier.append(new_sub)
    return subgroups

def maximal_subgroups(G):
    subs = all_subgroups(G)
    G_set = frozenset(G.elements)
    if G_set in subs:
        subs.remove(G_set)
    maximals = []
    for M in subs:
        is_maximal = True
        for H in subs:
            if M != H and M.issubset(H):
                is_maximal = False
                break
        if is_maximal:
            maximals.append(M)
    return maximals

def frattini_subgroup(G):
    maximals = maximal_subgroups(G)
    if not maximals:
        return frozenset(G.elements)
    frattini_elements = set(maximals[0])
    for M in maximals[1:]:
        frattini_elements.intersection_update(M)
    return frattini_elements

def conditions(witness):
    try:
        h1 = isinstance(witness, PermutationGroup)
        if h1:
            _ = witness.elements
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            frattini_els = frattini_subgroup(witness)
            H = PermutationGroup(list(frattini_els))
            neg_q = not H.is_nilpotent
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: \\Phi(G) is not a nilpotent group"
]

N_HYP = 1
NEG_Q_INDEX = 1