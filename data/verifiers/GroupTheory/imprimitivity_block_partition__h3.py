import itertools
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import Integer

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

def conditions(witness):
    try:
        G, B = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(B, (set, list, tuple))
        if h1:
            for b in B:
                if not (isinstance(b, (int, Integer)) and 0 <= int(b) < G.degree):
                    h1 = False
                    break
    except Exception:
        h1 = False
        
    try:
        if callable(G.is_transitive):
            h2 = bool(G.is_transitive())
        else:
            h2 = bool(G.is_transitive)
    except Exception:
        h2 = False
        
    try:
        translates = set()
        try:
            elements = list(G.generate_dimino())
        except AttributeError:
            elements = list(G.elements)
            
        for g in elements:
            translate = frozenset(g(int(b)) for b in B)
            translates.add(translate)
            
        union = set()
        for t in translates:
            union.update(t)
            
        is_partition = True
        if union != set(range(G.degree)):
            is_partition = False
        else:
            t_list = list(translates)
            for i in range(len(t_list)):
                for j in range(i + 1, len(t_list)):
                    if t_list[i].intersection(t_list[j]):
                        is_partition = False
                        break
                if not is_partition:
                    break
            if frozenset() in translates:
                is_partition = False
                
        neg_q = not is_partition
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a permutation group and B is a subset of its domain",
    "H_2: The action of G is transitive",
    "¬Q: The translates of B do not form a partition of the domain"
]

N_HYP = 2
NEG_Q_INDEX = 2