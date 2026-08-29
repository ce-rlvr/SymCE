import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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

def conditions(witness) -> list[bool]:
    try:
        N = list(witness['N'])
        H = list(witness['H'])
        G = list(witness['G'])
        e_N = witness['e_N']
    except Exception:
        return [False] * 3 + [False]

    # H1: N and H are groups
    def is_group(elements):
        if not elements: return False
        for x in elements:
            for y in elements:
                if (x * y) not in elements:
                    return False
            if (x ** -1) not in elements:
                return False
        return True

    try:
        h1 = is_group(N) and is_group(H)
    except Exception:
        h1 = False

    # H2: G acts on N via the action (n, h) . x = n h x h^{-1}
    try:
        h2 = True
        if not G:
            h2 = False
        else:
            def op_G(g1, g2):
                n1, h1 = g1
                n2, h2 = g2
                return (n1 * h1 * n2 * (h1 ** -1), h1 * h2)

            # Check G is a group under op_G
            for g1 in G:
                for g2 in G:
                    if op_G(g1, g2) not in G:
                        h2 = False
                        break
                if not h2: break
            
            if h2:
                # Find identity of G
                e_G = None
                for g in G:
                    if all(op_G(g, x) == x and op_G(x, g) == x for x in G):
                        e_G = g
                        break
                if e_G is None:
                    h2 = False
                else:
                    # Check inverses
                    for g in G:
                        has_inv = False
                        for x in G:
                            if op_G(g, x) == e_G and op_G(x, g) == e_G:
                                has_inv = True
                                break
                        if not has_inv:
                            h2 = False
                            break
            
            if h2:
                # Check action well-defined and properties
                def action(g, x):
                    n, h = g
                    return n * h * x * (h ** -1)
                
                for g in G:
                    for x in N:
                        if action(g, x) not in N:
                            h2 = False
                            break
                    if not h2: break
                
                if h2:
                    for x in N:
                        if action(e_G, x) != x:
                            h2 = False
                            break
                    
                    if h2:
                        for g1 in G:
                            for g2 in G:
                                for x in N:
                                    if action(g1, action(g2, x)) != action(op_G(g1, g2), x):
                                        h2 = False
                                        break
                                if not h2: break
                            if not h2: break
    except Exception:
        h2 = False

    # H3: e_N is the identity element of N
    try:
        h3 = (e_N in N) and all(e_N * x == x and x * e_N == x for x in N)
    except Exception:
        h3 = False

    # Conclusion: Stabilizer of e_N is exactly {e_N} x H
    try:
        def action(g, x):
            n, h = g
            return n * h * x * (h ** -1)
        
        stabilizer = [g for g in G if action(g, e_N) == e_N]
        expected = [(e_N, h) for h in H]
        
        def is_equal_unordered(list1, list2):
            if len(list1) != len(list2):
                return False
            list2_copy = list(list2)
            for item in list1:
                if item in list2_copy:
                    list2_copy.remove(item)
                else:
                    return False
            return True
        
        neg_q = not is_equal_unordered(stabilizer, expected)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: N and H are groups",
    "H_2: G acts on N via the action (n, h) . x = n h x h^{-1}",
    "H_3: e_N is the identity element of N",
    "¬Q: The stabilizer of e_N is not exactly {e_N} x H"
]

N_HYP = 3
NEG_Q_INDEX = 3