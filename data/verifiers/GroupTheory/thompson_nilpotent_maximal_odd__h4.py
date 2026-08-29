import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime, factorint
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    def is_maximal(G, M):
        from sympy.combinatorics import PermutationGroup
        from sympy.ntheory import isprime

        def get_order(grp):
            return grp.order() if callable(grp.order) else grp.order

        def get_elements(grp):
            return grp.elements() if callable(grp.elements) else grp.elements

        if get_order(M) >= get_order(G):
            return False
        for gen in M.generators:
            if gen not in G:
                return False
                
        G_order = get_order(G)
        M_order = get_order(M)
        
        index = G_order // M_order
        if isprime(index):
            return True

        M_elements = list(get_elements(M))
        visited = set(M_elements)
        
        for g in get_elements(G):
            if g in visited:
                continue
                
            H = PermutationGroup(*(list(M.generators) + [g]))
            if get_order(H) != G_order:
                return False
                
            for m in M_elements:
                visited.add(m * g)
                
        return True

    if isinstance(witness, tuple) and len(witness) == 2:
        G, M_obj = witness
    else:
        G = witness
        M_obj = None

    from sympy.combinatorics import PermutationGroup
    
    if isinstance(M_obj, (list, tuple)):
        try:
            M = PermutationGroup(*M_obj)
        except Exception:
            M = None
    else:
        M = M_obj

    def get_order(grp):
        return grp.order() if callable(grp.order) else grp.order

    try:
        h1 = isinstance(G, PermutationGroup) and get_order(G) < float('inf')
    except Exception:
        h1 = False

    try:
        h2 = False
        if M is None and isinstance(G, PermutationGroup):
            from sympy.ntheory import factorint
            factors = factorint(get_order(G))
            for p in factors:
                try:
                    S = G.sylow_subgroup(p)
                    if is_maximal(G, S):
                        M = S
                        h2 = True
                        break
                except Exception:
                    continue
                    
        if not h2:
            if M is not None and isinstance(M, PermutationGroup):
                h2 = is_maximal(G, M)
    except Exception:
        h2 = False

    try:
        if M is None or not isinstance(M, PermutationGroup):
            h3 = False
        else:
            h3 = M.is_nilpotent() if callable(M.is_nilpotent) else M.is_nilpotent
            h3 = bool(h3)
    except Exception:
        h3 = False

    try:
        is_solv = G.is_solvable() if callable(G.is_solvable) else G.is_solvable
        neg_q = not bool(is_solv)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G contains a maximal subgroup M",
    "H_3: M is a nilpotent group",
    "¬Q: G is not a solvable group"
]

N_HYP = 3
NEG_Q_INDEX = 3