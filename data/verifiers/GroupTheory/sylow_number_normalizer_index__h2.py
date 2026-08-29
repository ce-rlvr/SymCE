import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
import math
import itertools
import functools

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
    "H_2: P is a Sylow p-subgroup of G",
    "¬Q: The number of Sylow p-subgroups of G is not equal to the index of N_G(P) in G"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_order(obj):
    return obj.order() if callable(obj.order) else obj.order

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                G, P, p_val = witness
            elif len(witness) == 2:
                G, P = witness
                p_val = None
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group
    try:
        h1 = hasattr(G, 'order') and get_order(G) > 0 and hasattr(G, 'generate')
    except Exception:
        h1 = False

    # H_2: P is a Sylow p-subgroup of G
    try:
        h2 = False
        if h1 and hasattr(P, 'order') and hasattr(P, 'generate'):
            P_elements = set(P.generate())
            G_elements = set(G.generate())
            if P_elements.issubset(G_elements):
                order_G = get_order(G)
                order_P = get_order(P)
                
                if p_val is not None:
                    try:
                        p_int = int(p_val)
                        if p_int >= 2:
                            k = 0
                            while order_G % (p_int**(k+1)) == 0:
                                k += 1
                            if p_int**k == order_P:
                                h2 = True
                    except Exception:
                        pass
                else:
                    for p_test in range(2, order_G + 1):
                        k = 0
                        while order_G % (p_test**(k+1)) == 0:
                            k += 1
                        if p_test**k == order_P:
                            h2 = True
                            break
    except Exception:
        h2 = False

    # ¬Q: The number of Sylow p-subgroups of G is not equal to the index of N_G(P) in G
    try:
        neg_q = False
        if h1 and h2:
            order_G = get_order(G)
            order_P = get_order(P)
            
            p_to_check = None
            if p_val is not None:
                try:
                    p_to_check = int(p_val)
                except Exception:
                    pass
            else:
                for p_test in range(2, order_G + 1):
                    k = 0
                    while order_G % (p_test**(k+1)) == 0:
                        k += 1
                    if p_test**k == order_P:
                        p_to_check = p_test
                        break
            
            if p_to_check is not None:
                if isprime(p_to_check):
                    neg_q = False
                else:
                    G_elements = list(G.generate())
                    P_elements = set(P.generate())
                    
                    conjugates_of_P = []
                    for g in G_elements:
                        conj = set(g * p * ~g for p in P_elements)
                        if conj not in conjugates_of_P:
                            conjugates_of_P.append(conj)
                    
                    K = order_P
                    found_other = False
                    
                    for g in G_elements:
                        if get_order(g) == K:
                            H = set()
                            curr = g
                            while curr not in H:
                                H.add(curr)
                                curr = curr * g
                            if H not in conjugates_of_P:
                                found_other = True
                                break
                    
                    if not found_other:
                        valid_elements = [g for g in G_elements if K % get_order(g) == 0 and get_order(g) > 1]
                        for i in range(len(valid_elements)):
                            if found_other: break
                            for j in range(i + 1, len(valid_elements)):
                                a = valid_elements[i]
                                b = valid_elements[j]
                                H = set([a, b])
                                queue = [a, b]
                                while queue:
                                    curr = queue.pop(0)
                                    for gen in (a, b):
                                        prod = curr * gen
                                        if prod not in H:
                                            H.add(prod)
                                            queue.append(prod)
                                            if len(H) > K:
                                                break
                                    if len(H) > K:
                                        break
                                if len(H) == K and H not in conjugates_of_P:
                                    is_subgroup = True
                                    for x in H:
                                        for y in H:
                                            if x * y not in H:
                                                is_subgroup = False
                                                break
                                        if not is_subgroup:
                                            break
                                    if is_subgroup:
                                        found_other = True
                                        break

                    if not found_other and K >= 8:
                        for i in range(len(valid_elements)):
                            if found_other: break
                            for j in range(i + 1, len(valid_elements)):
                                if found_other: break
                                for k in range(j + 1, len(valid_elements)):
                                    a = valid_elements[i]
                                    b = valid_elements[j]
                                    c = valid_elements[k]
                                    H = set([a, b, c])
                                    queue = [a, b, c]
                                    while queue:
                                        curr = queue.pop(0)
                                        for gen in (a, b, c):
                                            prod = curr * gen
                                            if prod not in H:
                                                H.add(prod)
                                                queue.append(prod)
                                                if len(H) > K:
                                                    break
                                        if len(H) > K:
                                            break
                                    if len(H) == K and H not in conjugates_of_P:
                                        is_subgroup = True
                                        for x in H:
                                            for y in H:
                                                if x * y not in H:
                                                    is_subgroup = False
                                                    break
                                            if not is_subgroup:
                                                break
                                        if is_subgroup:
                                            found_other = True
                                            break
                    
                    if found_other:
                        neg_q = True
                    else:
                        neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]