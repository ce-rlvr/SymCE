import math
import itertools
import functools

import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy import abc

# Top-level setup
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

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The order of N and the index of N in G are coprime",
    "H_3: Either N or G/N is a solvable group",
    "¬Q: There exist two complements of N in G that are not conjugate"
]
N_HYP = 3
NEG_Q_INDEX = 3

def get_elements(G):
    if hasattr(G, 'generate') and callable(G.generate):
        return list(G.generate())
    elif hasattr(G, 'elements'):
        return list(G.elements)
    else:
        elements = {G.identity}
        queue = [G.identity]
        while queue:
            curr = queue.pop(0)
            for g in G.generators:
                nxt = curr * g
                if nxt not in elements:
                    elements.add(nxt)
                    queue.append(nxt)
        return list(elements)

def is_normal_subgroup(G, N):
    for g in G.generators:
        for n in N.generators:
            if (g * n * ~g) not in N:
                return False
    return True

def check_solvable(G):
    if hasattr(G, 'is_solvable'):
        val = G.is_solvable
        if callable(val):
            return val()
        return val
    series = G.derived_series()
    return int(series[-1].order()) == 1

def are_conjugate(G, H1, H2):
    for g in get_elements(G):
        if all((g * h * ~g) in H2 for h in H1.generators):
            return True
    return False

def is_comp(H, G, N, index_N):
    if not isinstance(H, PermutationGroup): return False
    if not all(g in G for g in H.generators): return False
    if int(H.order()) != index_N: return False
    for h in get_elements(H):
        if h != G.identity and h in N:
            return False
    return True

def find_complements(G, N, index_N):
    elements = [g for g in get_elements(G) if index_N % int(g.order()) == 0]
    complements = []
    
    for g in elements:
        if int(g.order()) == index_N:
            try:
                H = PermutationGroup(g)
                intersect_trivial = True
                for h in get_elements(H):
                    if h != G.identity and h in N:
                        intersect_trivial = False
                        break
                if intersect_trivial:
                    is_conj = False
                    for C in complements:
                        if are_conjugate(G, H, C):
                            is_conj = True
                            break
                    if not is_conj:
                        complements.append(H)
                        if len(complements) >= 2:
                            return complements
            except Exception:
                pass

    if len(complements) >= 2:
        return complements

    count = 0
    for gens in itertools.combinations(elements, 2):
        count += 1
        if count > 2000:
            break
        try:
            H = PermutationGroup(*gens)
            if int(H.order()) == index_N:
                intersect_trivial = True
                for h in get_elements(H):
                    if h != G.identity and h in N:
                        intersect_trivial = False
                        break
                if intersect_trivial:
                    is_conj = False
                    for C in complements:
                        if are_conjugate(G, H, C):
                            is_conj = True
                            break
                    if not is_conj:
                        complements.append(H)
                        if len(complements) >= 2:
                            return complements
        except Exception:
            pass
            
    return complements

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 4:
                G, N, H1, H2 = witness
            elif len(witness) == 2:
                G, N = witness
                H1, H2 = None, None
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup) and int(G.order()) > 0
    except Exception:
        h1 = False

    # H2: The order of N and the index of N in G are coprime
    try:
        if h1 and isinstance(N, PermutationGroup) and all(g in G for g in N.generators):
            order_N = int(N.order())
            index_N = int(G.order()) // order_N
            h2 = math.gcd(order_N, index_N) == 1
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: Either N or G/N is a solvable group
    try:
        if h2:
            if check_solvable(N):
                h3 = True
            else:
                if is_normal_subgroup(G, N):
                    series = G.derived_series()
                    h3 = all(g in N for g in series[-1].generators)
                else:
                    h3 = False
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: There exist two complements of N in G that are not conjugate
    try:
        neg_q = False
        if h2:
            if H1 is not None and H2 is not None:
                if is_comp(H1, G, N, index_N) and is_comp(H2, G, N, index_N):
                    neg_q = not are_conjugate(G, H1, H2)
            else:
                complements = find_complements(G, N, index_N)
                if len(complements) >= 2:
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]