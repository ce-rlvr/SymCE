import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        G, x = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1 = False
        
    try:
        if isinstance(x, Permutation):
            h2 = x in G
        elif isinstance(x, PermutationGroup):
            h2 = all(gen in G for gen in x.generators)
        elif isinstance(x, (list, tuple, set, frozenset)):
            h2 = all(isinstance(elem, Permutation) and elem in G for elem in x)
        else:
            h2 = False
    except Exception:
        h2 = False
        
    try:
        c_size = 0
        if isinstance(x, Permutation):
            for g in list(G.generate()):
                if g * x == x * g:
                    c_size += 1
        elif isinstance(x, PermutationGroup):
            for g in list(G.generate()):
                if all(g * h == h * g for h in list(x.generate())):
                    c_size += 1
        elif isinstance(x, (list, tuple, set, frozenset)):
            for g in list(G.generate()):
                if all(g * h == h * g for h in x):
                    c_size += 1
        else:
            c_size = -1
            
        if isinstance(x, Permutation):
            orbit = set()
            for g in list(G.generate()):
                orbit.add(g * x * ~g)
            conj_size = len(orbit)
        elif isinstance(x, PermutationGroup):
            orbit = set()
            for g in list(G.generate()):
                conj_elems = frozenset([g * h * ~g for h in list(x.generate())])
                orbit.add(conj_elems)
            conj_size = len(orbit)
        elif isinstance(x, (list, tuple, set, frozenset)):
            orbit = set()
            for g in list(G.generate()):
                conj_elems = frozenset([g * h * ~g for h in x])
                orbit.add(conj_elems)
            conj_size = len(orbit)
        else:
            conj_size = -1
            
        if c_size > 0 and conj_size >= 0:
            neg_q = (conj_size * c_size != G.order())
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: C_G(x) is the centralizer of x in G",
    "not Q: The size of the conjugacy class of x is not equal to the index of C_G(x) in G"
]

N_HYP = 2
NEG_Q_INDEX = 2