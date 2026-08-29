import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.abc
import math
import itertools
import functools
import z3

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
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
    G, x, N = None, None, None
    if isinstance(witness, dict):
        G = witness.get('G')
        x = witness.get('x')
        N = witness.get('N')
    elif isinstance(witness, (tuple, list)):
        if len(witness) == 3:
            groups = [item for item in witness if hasattr(item, 'is_group') and item.is_group]
            elements = [item for item in witness if hasattr(item, '__mul__') and hasattr(item, 'order') and not (hasattr(item, 'is_group') and item.is_group)]
            
            if len(groups) == 2:
                if groups[0].is_subgroup(groups[1]) and not groups[1].is_subgroup(groups[0]):
                    N, G = groups[0], groups[1]
                elif groups[1].is_subgroup(groups[0]) and not groups[0].is_subgroup(groups[1]):
                    G, N = groups[0], groups[1]
                else:
                    G, N = groups[0], groups[1]
            elif len(groups) == 1:
                G = groups[0]
                
            if len(elements) >= 1:
                x = elements[0]
                
            remaining = [item for item in witness if item is not G and item is not x]
            
            if N is None and x is None and len(remaining) == 2:
                if G is not None:
                    if remaining[0] in G:
                        x, N = remaining[0], remaining[1]
                    elif remaining[1] in G:
                        x, N = remaining[1], remaining[0]
            elif N is None and len(remaining) >= 1:
                N = remaining[0]
            elif x is None and len(remaining) >= 1:
                x = remaining[0]
        elif len(witness) == 2:
            groups = [item for item in witness if hasattr(item, 'is_group') and item.is_group]
            if len(groups) == 1:
                G = groups[0]
            remaining = [item for item in witness if item is not G]
            if remaining:
                x = remaining[0]

    # H1: G is a group
    try:
        h1 = hasattr(G, 'is_group') and G.is_group
    except Exception:
        h1 = False

    # H2: x is an element of G having finite order k
    try:
        h2 = False
        if h1 and x is not None:
            if x in G:
                k = x.order()
                if k > 0 and k != float('inf'):
                    h2 = True
    except Exception:
        h2 = False

    # neg_Q: The order of the coset xN in the quotient group G/N divides k.
    # This fails (neg_Q is True) if G/N is not a quotient group (i.e., N is not a normal subgroup)
    # or if the order does not divide k.
    try:
        neg_q = False
        if h1 and h2:
            if N is None:
                neg_q = True
            else:
                if not hasattr(N, 'is_subgroup') and isinstance(N, (list, set, tuple)):
                    try:
                        N = PermutationGroup(list(N))
                    except Exception:
                        pass

                is_normal = False
                if hasattr(N, 'is_subgroup') and N.is_subgroup(G):
                    if hasattr(G, 'is_normal'):
                        is_normal = G.is_normal(N)
                
                if not is_normal:
                    neg_q = True
                else:
                    # G/N is a quotient group
                    m = 1
                    curr = x
                    while curr not in N:
                        curr = curr * x
                        m += 1
                        if m > 10000:
                            break
                    k = x.order()
                    if k % m != 0:
                        neg_q = True
    except Exception:
        neg_q = True

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: x is an element of G having finite order k",
    "¬Q: The order of the coset xN in the quotient group G/N does not divide k (or G/N is not a quotient group)"
]

N_HYP = 2
NEG_Q_INDEX = 2