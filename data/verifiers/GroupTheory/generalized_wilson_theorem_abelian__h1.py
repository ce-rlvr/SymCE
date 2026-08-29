import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup, Permutation
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
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

# Quaternion group Q8 (smallest non-abelian group with exactly one element of order 2)
_i = Permutation(0, 2, 1, 3)(4, 6, 5, 7)
_j = Permutation(0, 4, 1, 5)(2, 7, 3, 6)
Q8 = PermutationGroup(_i, _j)

# Klein four-group V4
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if hasattr(witness, 'elements'):
            elements = list(witness.elements)
        else:
            elements = list(witness)
        if not elements:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: G contains exactly one element x of order 2.
    try:
        order_2_elems = []
        for g in elements:
            if hasattr(g, 'order'):
                if g.order() == 2:
                    order_2_elems.append(g)
        h1 = (len(order_2_elems) == 1)
    except Exception:
        h1 = False

    # ¬Q: The sum of all elements in G is not equal to x.
    try:
        if len(order_2_elems) == 1:
            x = order_2_elems[0]
        else:
            x = None
            
        is_abelian = True
        if hasattr(witness, 'is_abelian'):
            is_abelian = witness.is_abelian
        else:
            # Check manually if not provided
            try:
                for a in elements:
                    for b in elements:
                        if a * b != b * a:
                            is_abelian = False
                            break
                    if not is_abelian:
                        break
            except Exception:
                try:
                    for a in elements:
                        for b in elements:
                            if a + b != b + a:
                                is_abelian = False
                                break
                        if not is_abelian:
                            break
                except Exception:
                    pass
                    
        # If the group is non-abelian, the "sum" (product) of all elements is not well-defined 
        # (it depends on the order), so the conclusion that it equals x fails.
        if not is_abelian:
            neg_q = True
        else:
            # For abelian groups, compute the product (or sum)
            try:
                prod = elements[0]
                for g in elements[1:]:
                    prod = prod * g
                neg_q = bool(prod != x)
            except Exception:
                # Fallback to addition if multiplication is not supported
                prod = elements[0]
                for g in elements[1:]:
                    prod = prod + g
                neg_q = bool(prod != x)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G contains exactly one element x of order 2",
    "¬Q: The sum of all elements in G is not equal to x"
]

N_HYP = 1
NEG_Q_INDEX = 1