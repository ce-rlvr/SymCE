import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import factorint

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

def conditions(witness):
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    try:
        if not isinstance(witness, PermutationGroup):
            neg_q = False
        else:
            try:
                n = int(witness.order())
            except TypeError:
                n = int(witness.order)
                
            factors = factorint(n)
            if len(factors) != 1:
                is_cpp = False
            else:
                is_cpp = False
                elems = witness.elements
                if callable(elems):
                    elems = elems()
                for g in elems:
                    try:
                        g_ord = int(g.order())
                    except TypeError:
                        g_ord = int(g.order)
                        
                    if g_ord == n:
                        is_cpp = True
                        break
            neg_q = not is_cpp
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: G is not a cyclic group of prime power order"
]

N_HYP = 1
NEG_Q_INDEX = 1