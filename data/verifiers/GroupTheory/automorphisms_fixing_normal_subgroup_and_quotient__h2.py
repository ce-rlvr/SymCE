import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import itertools

# Top-level setup for named objects
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

CONDITION_LABELS = [
    "H_1: G is a group and N is a normal subgroup",
    "H_2: A is the set of automorphisms fixing N and G/N",
    "¬Q: A is not an abelian subgroup of Aut(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        G, N = witness
    except Exception:
        return [False, False, False]
        
    try:
        is_groups = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup)
        if is_groups:
            elements_G = list(G.generate())
            elements_N = list(N.generate())
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a group and N is a normal subgroup
    try:
        is_sub = N.is_subgroup(G)
        if is_sub:
            is_norm = True
            for g in elements_G:
                g_inv = g**-1
                for n in elements_N:
                    if g * n * g_inv not in elements_N:
                        is_norm = False
                        break
                if not is_norm:
                    break
            h1 = is_norm
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: A is the set of automorphisms fixing N and G/N
    try:
        if h1:
            gens = G.generators
            A = []
            for imgs in itertools.product(elements_G, repeat=len(gens)):
                mapping = {G.identity: G.identity}
                queue = [G.identity]
                is_homo = True
                
                while queue:
                    curr = queue.pop(0)
                    curr_img = mapping[curr]
                    for g, img in zip(gens, imgs):
                        nxt = curr * g
                        nxt_img = curr_img * img
                        if nxt in mapping:
                            if mapping[nxt] != nxt_img:
                                is_homo = False
                                break
                        else:
                            mapping[nxt] = nxt_img
                            queue.append(nxt)
                    if not is_homo:
                        break
                        
                if not is_homo:
                    continue
                    
                if len(mapping) != len(elements_G):
                    continue
                    
                if len(set(mapping.values())) != len(elements_G):
                    continue
                    
                cond1 = True
                for n in elements_N:
                    if mapping[n] != n:
                        cond1 = False
                        break
                if not cond1:
                    continue
                    
                cond2 = True
                for g in elements_G:
                    val = (g**-1) * mapping[g]
                    if val not in elements_N:
                        cond2 = False
                        break
                if not cond2:
                    continue
                    
                A.append(mapping)
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: A is not an abelian subgroup of Aut(G)
    try:
        if h1 and h2:
            is_ab = True
            for alpha in A:
                for beta in A:
                    for g in elements_G:
                        if alpha[beta[g]] != beta[alpha[g]]:
                            is_ab = False
                            break
                    if not is_ab:
                        break
                if not is_ab:
                    break
            neg_q = not is_ab
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]