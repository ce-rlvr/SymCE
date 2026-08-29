import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_alpha(alpha, g):
    if callable(alpha):
        return alpha(g)
    elif isinstance(alpha, dict):
        return alpha[g]
    else:
        raise ValueError("alpha must be callable or dict")

def get_quotient_table(G, M):
    elements = list(G.elements)
    id_el = G.identity
    if id_el in elements:
        elements.remove(id_el)
        elements.insert(0, id_el)
    else:
        elements.insert(0, id_el)
        
    coset_reps = []
    for g in elements:
        found = False
        for rep in coset_reps:
            if (rep**-1 * g) in M:
                found = True
                break
        if not found:
            coset_reps.append(g)
            
    n = len(coset_reps)
    table = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            prod = coset_reps[i] * coset_reps[j]
            for k in range(n):
                if (coset_reps[k]**-1 * prod) in M:
                    table[i][j] = k
                    break
    return table

def are_isomorphic(table1, table2):
    n = len(table1)
    if len(table2) != n:
        return False
    if n == 1:
        return True
        
    def get_orders(table):
        orders = []
        for i in range(n):
            curr = i
            order = 1
            while curr != 0:
                curr = table[i][curr]
                order += 1
                if order > n:
                    break
            orders.append(order)
        return orders
        
    orders1 = get_orders(table1)
    orders2 = get_orders(table2)
    if sorted(orders1) != sorted(orders2):
        return False
        
    def search(mapping, used):
        if len(mapping) == n:
            return True
        i = len(mapping)
        for j in range(n):
            if not used[j] and orders1[i] == orders2[j]:
                valid = True
                for x in range(i):
                    for y in range(i):
                        if table1[x][y] == i:
                            if table2[mapping[x]][mapping[y]] != j:
                                valid = False
                                break
                    if not valid: break
                if not valid: continue
                
                for x in range(i):
                    z = table1[x][i]
                    if z < i:
                        if table2[mapping[x]][j] != mapping[z]:
                            valid = False
                            break
                if not valid: continue
                
                for x in range(i):
                    z = table1[i][x]
                    if z < i:
                        if table2[j][mapping[x]] != mapping[z]:
                            valid = False
                            break
                if not valid: continue
                
                z = table1[i][i]
                if z < i:
                    if table2[j][j] != mapping[z]:
                        valid = False
                        continue
                        
                mapping.append(j)
                used[j] = True
                if search(mapping, used):
                    return True
                mapping.pop()
                used[j] = False
        return False

    return search([0], [True] + [False]*(n-1))

def conditions(witness) -> list[bool]:
    try:
        G, N, alpha = witness
    except Exception:
        return [False, False, False]
        
    # H_1: N is a normal subgroup of G
    try:
        h1 = bool(N.is_subgroup(G) and N.is_normal(G))
    except Exception:
        h1 = False
        
    # H_2: \alpha is an automorphism of G
    try:
        elements = list(G.elements)
        images = []
        h2 = True
        for g in elements:
            ag = get_alpha(alpha, g)
            if ag not in G:
                h2 = False
                break
            images.append(ag)
        if h2:
            if len(set(images)) != len(elements):
                h2 = False
        if h2:
            for g1 in elements:
                for g2 in elements:
                    if get_alpha(alpha, g1 * g2) != get_alpha(alpha, g1) * get_alpha(alpha, g2):
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False
        
    # neg_Q: The image \alpha(N) is not a normal subgroup of G, or G/N is not isomorphic to G/\alpha(N)
    try:
        gens = []
        for gen in N.generators:
            gens.append(get_alpha(alpha, gen))
        if not gens:
            gens = [G.identity]
        alpha_N = PermutationGroup(gens)
        
        q_holds = True
        if not alpha_N.is_subgroup(G):
            q_holds = False
        elif not alpha_N.is_normal(G):
            q_holds = False
        else:
            table_N = get_quotient_table(G, N)
            table_alpha_N = get_quotient_table(G, alpha_N)
            if not are_isomorphic(table_N, table_alpha_N):
                q_holds = False
                
        neg_q = not q_holds
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: \\alpha is an automorphism of G",
    "¬Q: The image \\alpha(N) is not a normal subgroup of G, or G/N is not isomorphic to G/\\alpha(N)"
]

N_HYP = 2
NEG_Q_INDEX = 2