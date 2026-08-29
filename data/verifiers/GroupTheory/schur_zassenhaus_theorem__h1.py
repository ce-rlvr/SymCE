import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math
import itertools

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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))

def conditions(witness) -> list[bool]:
    try:
        G, N = witness
    except Exception:
        return [False, False, False]

    # H_1: N is a normal subgroup of G
    h1 = None
    try:
        if hasattr(G, 'is_normal'):
            try:
                h1 = G.is_normal(N)
            except Exception:
                pass
        if h1 is None and hasattr(N, 'is_normal_in'):
            try:
                h1 = N.is_normal_in(G)
            except Exception:
                pass
        if h1 is None:
            h1 = True
            if hasattr(N, 'generators') and hasattr(G, 'generators'):
                for n in N.generators:
                    if n not in G:
                        h1 = False
                        break
                if h1:
                    for g in G.generators:
                        try:
                            inv_g = g**-1
                        except Exception:
                            inv_g = ~g
                        for n in N.generators:
                            if (g * n * inv_g) not in N:
                                h1 = False
                                break
                        if not h1:
                            break
            elif hasattr(N, 'elements') and hasattr(G, 'elements'):
                for n in N.elements:
                    if n not in G:
                        h1 = False
                        break
                if h1:
                    for g in G.elements:
                        try:
                            inv_g = g**-1
                        except Exception:
                            inv_g = ~g
                        for n in N.elements:
                            if (g * n * inv_g) not in N:
                                h1 = False
                                break
                        if not h1:
                            break
            else:
                h1 = False
    except Exception:
        h1 = False
    if h1 is None:
        h1 = False

    # H_2: The order |N| and the index [G:N] are coprime
    h2 = False
    try:
        order_N = N.order()
        index = None
        if hasattr(G, 'index'):
            try:
                index = G.index(N)
            except Exception:
                pass
        if index is None and hasattr(N, 'index'):
            try:
                index = N.index(G)
            except Exception:
                pass
        if index is None:
            order_G = G.order()
            index = order_G // order_N
        
        is_inf_N = False
        is_inf_index = False
        try:
            is_inf_N = float(order_N) == float('inf')
        except Exception:
            pass
        try:
            is_inf_index = float(index) == float('inf')
        except Exception:
            pass
            
        if is_inf_N and not is_inf_index:
            h2 = True
        elif is_inf_index and not is_inf_N:
            h2 = True
        elif is_inf_N and is_inf_index:
            h2 = False
        else:
            h2 = math.gcd(int(order_N), int(index)) == 1
    except Exception:
        h2 = False

    # neg_Q: There does NOT exist a subgroup H of G of order [G:N] such that G is the internal semidirect product of N and H
    neg_q = False
    try:
        index = None
        if hasattr(G, 'index'):
            try:
                index = G.index(N)
            except Exception:
                pass
        if index is None and hasattr(N, 'index'):
            try:
                index = N.index(G)
            except Exception:
                pass
        if index is None:
            index = G.order() // N.order()

        def check_neg_q():
            if index == 1:
                return False
            try:
                if index == G.order():
                    return False
            except Exception:
                pass
                
            if hasattr(G, 'has_subgroup_of_order'):
                return not G.has_subgroup_of_order(index)
            if hasattr(G, 'has_complement'):
                return not G.has_complement(N)
            if hasattr(G, 'subgroups'):
                for H in G.subgroups():
                    if H.order() == index:
                        return False
                return True
            if isinstance(G, PermutationGroup):
                return False
            return True

        neg_q = check_neg_q()
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: The order of N and the index of N in G are coprime",
    "¬Q: G does not have a subgroup H of order equal to the index of N in G such that G is the internal semidirect product of N and H"
]

N_HYP = 2
NEG_Q_INDEX = 2