import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime

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

def conditions(witness):
    try:
        G, M = witness
    except Exception:
        return [False, False, False]

    # H1: G is a nilpotent group
    try:
        h1 = False
        if hasattr(G, 'is_nilpotent'):
            if callable(G.is_nilpotent):
                h1 = bool(G.is_nilpotent())
            else:
                h1 = bool(G.is_nilpotent)
    except Exception:
        h1 = False

    # H2: M is a maximal subgroup of G
    try:
        h2 = False
        if hasattr(M, 'is_maximal_subgroup_of'):
            if callable(M.is_maximal_subgroup_of):
                h2 = bool(M.is_maximal_subgroup_of(G))
            else:
                h2 = bool(M.is_maximal_subgroup_of)
        elif hasattr(M, 'is_maximal_subgroup'):
            if callable(M.is_maximal_subgroup):
                h2 = bool(M.is_maximal_subgroup(G))
            else:
                h2 = bool(M.is_maximal_subgroup)
        elif hasattr(G, 'is_maximal_subgroup'):
            if callable(G.is_maximal_subgroup):
                h2 = bool(G.is_maximal_subgroup(M))
            else:
                h2 = bool(G.is_maximal_subgroup)
        else:
            if hasattr(M, 'is_subgroup') and M.is_subgroup(G):
                go = G.order() if callable(G.order) else G.order
                mo = M.order() if callable(M.order) else M.order
                if mo < go:
                    if go < 1000:
                        is_max = True
                        for g in G.elements:
                            if hasattr(M, 'contains'):
                                in_M = M.contains(g)
                            elif hasattr(M, 'elements'):
                                in_M = g in M.elements
                            else:
                                in_M = g in M
                            if not in_M:
                                gens = list(M.generators) + [g]
                                H = PermutationGroup(gens)
                                ho = H.order() if callable(H.order) else H.order
                                if ho != go:
                                    is_max = False
                                    break
                        h2 = is_max
    except Exception:
        h2 = False

    # neg_Q: The index of M in G is NOT a prime number
    try:
        neg_q = False
        idx = None
        if hasattr(G, 'index'):
            if callable(G.index):
                idx = G.index(M)
            else:
                idx = G.index
        elif hasattr(G, 'order') and hasattr(M, 'order'):
            go = G.order() if callable(G.order) else G.order
            mo = M.order() if callable(M.order) else M.order
            idx = go / mo
            
        if idx is not None:
            if idx == sympy.oo or idx == float('inf'):
                neg_q = True
            else:
                if float(idx).is_integer():
                    neg_q = not isprime(int(idx))
                else:
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = ["H_1: G is a nilpotent group", "H_2: M is a maximal subgroup of G", "¬Q: The index of M in G is not a prime number"]

N_HYP = 2
NEG_Q_INDEX = 2