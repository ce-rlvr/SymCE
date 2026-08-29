import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def closure(gens, id_el):
    S = set(gens)
    S.add(id_el)
    queue = list(S)
    while queue:
        x = queue.pop(0)
        for y in list(S):
            xy = x * y
            if xy not in S:
                S.add(xy)
                queue.append(xy)
    return frozenset(S)

def get_all_subgroups(elements, id_el):
    trivial_sub = frozenset([id_el])
    subgroups = {trivial_sub}
    queue = [trivial_sub]
    
    while queue:
        current = queue.pop(0)
        for g in elements:
            if g not in current:
                S = set(current)
                q2 = [g]
                S.add(g)
                while q2:
                    x = q2.pop(0)
                    for y in list(S):
                        xy = x * y
                        if xy not in S:
                            S.add(xy)
                            q2.append(xy)
                        yx = y * x
                        if yx not in S:
                            S.add(yx)
                            q2.append(yx)
                new_sub = frozenset(S)
                if new_sub not in subgroups:
                    subgroups.add(new_sub)
                    queue.append(new_sub)
    return subgroups

def conditions(witness):
    try:
        G, H_gens, n, d = witness
    except Exception:
        return [False, False, False]
        
    G_elements = None
    H_set = None
    id_el = None
    
    try:
        G_elements = list(G.generate_dimino())
        if len(G_elements) > 60:
            h1_ok = False
        else:
            for g in G_elements:
                if g * g == g:
                    id_el = g
                    break
            
            H_set = closure(H_gens, id_el)
            
            if not all(g in G_elements for g in H_gens):
                h1_ok = False
            else:
                N_elements = []
                for g in G_elements:
                    g_inv = ~g
                    is_norm = True
                    for h in H_set:
                        if g * h * g_inv not in H_set:
                            is_norm = False
                            break
                    if is_norm:
                        N_elements.append(g)
                N_set = frozenset(N_elements)
                
                if len(N_set) % len(H_set) != 0:
                    h1_ok = False
                else:
                    actual_n = len(N_set) // len(H_set)
                    if actual_n != n:
                        h1_ok = False
                    else:
                        is_cyclic = False
                        for x in N_set:
                            k = 1
                            xk = x
                            while xk not in H_set:
                                xk = xk * x
                                k += 1
                            if k == n:
                                is_cyclic = True
                                break
                        h1_ok = is_cyclic
    except Exception:
        h1_ok = False

    try:
        h2_ok = isinstance(d, int) and d > 0 and isinstance(n, int) and n > 0 and n % d == 0
    except Exception:
        h2_ok = False

    try:
        if G_elements is not None and H_set is not None and isinstance(d, int) and d > 0:
            all_subgroups = get_all_subgroups(G_elements, id_el)
            if len(G_elements) % d != 0:
                count = 0
            else:
                target_order = len(G_elements) // d
                count = 0
                for U in all_subgroups:
                    if len(U) == target_order and H_set.issubset(U):
                        count += 1
            neg_q = (count != 1)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: The Galois group Gal(E/F) is a cyclic group of order n",
    "H_2: d is a positive integer that divides n",
    "¬Q: It is NOT the case that there exists a unique intermediate field K such that F <= K <= E and degree of K over F is d"
]

N_HYP = 2
NEG_Q_INDEX = 2