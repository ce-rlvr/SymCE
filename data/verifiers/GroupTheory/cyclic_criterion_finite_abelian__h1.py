import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.ntheory import factorint
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

def conditions(witness) -> list[bool]:
    try:
        if not hasattr(witness, 'order') or not hasattr(witness, 'elements'):
            return [False, False]
        
        order_val = witness.order
        if callable(order_val):
            order_val = order_val()
            
        if order_val == 1:
            h1 = True
        else:
            factors = factorint(order_val)
            h1 = True
            
            elements = witness.elements
            if callable(elements):
                elements = elements()
                
            for p, k in factors.items():
                if k == 1:
                    continue
                pk = p**k
                has_element_of_order_pk = False
                for g in elements:
                    g_order = g.order
                    if callable(g_order):
                        g_order = g_order()
                    if g_order == pk:
                        has_element_of_order_pk = True
                        break
                if not has_element_of_order_pk:
                    h1 = False
                    break
    except Exception:
        h1 = False

    try:
        order_val = witness.order
        if callable(order_val):
            order_val = order_val()
            
        elements = witness.elements
        if callable(elements):
            elements = elements()

        if hasattr(witness, 'is_abelian') and not witness.is_abelian:
            neg_q = True
        else:
            is_cyclic = False
            for g in elements:
                g_order = g.order
                if callable(g_order):
                    g_order = g_order()
                if g_order == order_val:
                    is_cyclic = True
                    break
            neg_q = not is_cyclic
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: For every prime p dividing the order of G, the Sylow p-subgroup of G is cyclic",
    "¬Q: G is not a cyclic group"
]

N_HYP = 1
NEG_Q_INDEX = 1