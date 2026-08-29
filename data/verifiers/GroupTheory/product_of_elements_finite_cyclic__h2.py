import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: G is a finite cyclic group
    h1_ok = False
    try:
        if hasattr(witness, 'elements') and hasattr(witness, 'order'):
            n = witness.order()
            if n >= 1:
                for g in witness.elements:
                    if g.order() == n:
                        h1_ok = True
                        break
    except Exception:
        h1_ok = False

    # Conclusion: The product of all elements of G evaluates to the identity element if n is odd, 
    # and evaluates to the unique element of order 2 in G if n is even.
    q_ok = False
    try:
        if hasattr(witness, 'elements') and hasattr(witness, 'order'):
            elements = list(witness.elements)
            # Sort elements by array_form to ensure determinism
            elements.sort(key=lambda g: g.array_form)
            n = len(elements)
            
            id_elem = next(g for g in elements if g.order() == 1)
            
            prod = id_elem
            for g in elements:
                prod = prod * g
                
            if n % 2 == 1:
                q_ok = (prod == id_elem)
            else:
                order_2 = [g for g in elements if g.order() == 2]
                if len(order_2) == 1:
                    q_ok = (prod == order_2[0])
                else:
                    q_ok = False
    except Exception:
        q_ok = False

    neg_q_ok = not q_ok

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite cyclic group",
    "¬Q: The product of all elements does not evaluate to the identity (if n odd) or the unique element of order 2 (if n even)"
]

N_HYP = 1
NEG_Q_INDEX = 1