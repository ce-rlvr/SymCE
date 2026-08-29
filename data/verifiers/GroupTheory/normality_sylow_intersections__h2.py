import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.ntheory import isprime, primefactors

# Top-level setup: named object bindings
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

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is the intersection of all Sylow p-subgroups of G",
    "¬Q: N is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, p, N = witness
            p_list = [p]
        elif isinstance(witness, tuple) and len(witness) == 2:
            G, N = witness
            p_list = None
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: N is the intersection of all Sylow p-subgroups of G
    h2 = False
    try:
        if h1:
            if p_list is None:
                p_list = primefactors(G.order())
            
            N_elements = set(N.generate()) if hasattr(N, 'generate') else set(N)
            
            for p_val in p_list:
                if not isprime(p_val):
                    continue
                
                P = G.sylow_subgroup(p_val)
                P_elements = set(P.generate())
                intersection = set(P_elements)
                
                for g in G.generate():
                    conj = {g * x * ~g for x in P_elements}
                    intersection = intersection.intersection(conj)
                    if len(intersection) == 1:
                        break
                
                if N_elements == intersection:
                    h2 = True
                    break
    except Exception:
        h2 = False

    # ¬Q: N is not a normal subgroup of G
    neg_q = False
    try:
        if h1:
            N_elements = set(N.generate()) if hasattr(N, 'generate') else set(N)
            G_elements = set(G.generate())
            
            if not N_elements.issubset(G_elements):
                is_subgroup = False
            else:
                id_elem = None
                for e in G_elements:
                    if e * e == e:
                        id_elem = e
                        break
                
                if id_elem not in N_elements:
                    is_subgroup = False
                else:
                    is_subgroup = True
                    for x in N_elements:
                        if ~x not in N_elements:
                            is_subgroup = False
                            break
                        for y in N_elements:
                            if x * y not in N_elements:
                                is_subgroup = False
                                break
                        if not is_subgroup:
                            break
            
            if not is_subgroup:
                neg_q = True
            else:
                is_normal = True
                for g in G_elements:
                    for n in N_elements:
                        if g * n * ~g not in N_elements:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                neg_q = not is_normal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]