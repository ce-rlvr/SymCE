import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    G, N, M = None, None, None
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            N = witness.get('N')
            M = witness.get('M')
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 3:
                G, N, M = witness
            elif len(witness) == 2:
                G, N = witness
    except Exception:
        pass

    def is_finite_group(grp):
        return hasattr(grp, 'elements') and hasattr(grp, 'generators') and hasattr(grp, 'order')

    # H1: G is a finite group
    h1 = False
    try:
        if is_finite_group(G):
            h1 = True
    except Exception:
        pass

    # H2: G is a semisimple group
    # A finite group is semisimple if it has no non-trivial abelian normal subgroups.
    h2 = False
    try:
        if h1:
            if G.order() == 1:
                h2 = True
            else:
                id_el = None
                for g in G.elements:
                    if g * g == g:
                        id_el = g
                        break
                
                seen = set()
                G_els = list(G.elements)
                is_semi = True
                for g in G_els:
                    if g in seen:
                        continue
                    if g == id_el:
                        seen.add(g)
                        continue
                        
                    # Find the conjugacy class of g
                    conj_class = set([g])
                    queue = [g]
                    while queue:
                        curr = queue.pop(0)
                        for gen in G.generators:
                            c1 = gen * curr * ~gen
                            if c1 not in conj_class:
                                conj_class.add(c1)
                                queue.append(c1)
                            c2 = ~gen * curr * gen
                            if c2 not in conj_class:
                                conj_class.add(c2)
                                queue.append(c2)
                                
                    seen.update(conj_class)
                    
                    # If the conjugacy class mutually commutes, its normal closure is an abelian normal subgroup
                    is_abelian = True
                    conj_list = list(conj_class)
                    for i in range(len(conj_list)):
                        for j in range(i + 1, len(conj_list)):
                            if conj_list[i] * conj_list[j] != conj_list[j] * conj_list[i]:
                                is_abelian = False
                                break
                        if not is_abelian:
                            break
                    
                    if is_abelian:
                        is_semi = False
                        break
                h2 = is_semi
    except Exception:
        pass

    # H3: N is a normal subgroup of G
    h3 = False
    try:
        if h1 and is_finite_group(N):
            G_els = set(G.elements)
            is_subgroup = True
            for gen in N.generators:
                if gen not in G_els:
                    is_subgroup = False
                    break
            if is_subgroup:
                N_els = set(N.elements)
                is_normal = True
                for g in G_els:
                    for n in N.generators:
                        if (g * n * ~g) not in N_els:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                h3 = is_normal
    except Exception:
        pass

    # neg_Q: C_G(N) != M
    neg_q = False
    try:
        if h1 and is_finite_group(N) and is_finite_group(M):
            cents = set()
            for g in list(G.elements):
                commutes = True
                for n in N.generators:
                    if g * n != n * g:
                        commutes = False
                        break
                if commutes:
                    cents.add(g)
            M_els = set(M.elements)
            neg_q = (cents != M_els)
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a semisimple group",
    "H_3: N is a normal subgroup of G",
    "¬Q: The centralizer C_G(N) is not equal to M"
]

N_HYP = 3
NEG_Q_INDEX = 3