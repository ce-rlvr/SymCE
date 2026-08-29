import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
import functools

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

def conditions(witness):
    try:
        # H_1: G is a finite group (and we can determine its order n)
        if not isinstance(witness, PermutationGroup):
            h1_ok = False
        else:
            n = witness.order()
            h1_ok = (n > 0)
    except Exception:
        h1_ok = False

    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            elements = list(witness.elements)
            n = len(elements)
            
            if n % 2 == 1:
                # n is odd
                prod = elements[0]
                for e in elements[1:]:
                    prod = prod * e
                expected = witness.identity
                conclusion_holds = (prod == expected)
            else:
                # n is even
                order_2 = [e for e in elements if e.order() == 2]
                if len(order_2) != 1:
                    # The conclusion assumes a unique element of order 2
                    conclusion_holds = False
                else:
                    expected = order_2[0]
                    prod = elements[0]
                    for e in elements[1:]:
                        prod = prod * e
                    conclusion_holds = (prod == expected)
                    
            neg_q_ok = not conclusion_holds
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: The product of all elements does not evaluate to the identity (if n is odd) or the unique element of order 2 (if n is even)"
]

N_HYP = 1
NEG_Q_INDEX = 1