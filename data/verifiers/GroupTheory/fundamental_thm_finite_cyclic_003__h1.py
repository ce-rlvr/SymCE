import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
import itertools

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

CONDITION_LABELS = [
    "H_1: d is a positive integer that divides n",
    "¬Q: G does not have exactly one subgroup of order d"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                G, n, d = witness
            elif len(witness) == 2:
                G, d = witness
                n = G.order()
            else:
                return [False, False]
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: d is a positive integer that divides n
    try:
        h1 = isinstance(d, int) and d > 0 and isinstance(n, int) and n > 0 and n % d == 0
    except Exception:
        h1 = False

    # neg_Q: G does NOT have exactly one subgroup of order d
    try:
        order = G.order()
        if order % d != 0:
            count = 0
        elif d == 1 or d == order:
            count = 1
        else:
            elements = list(set(G.generate()))
            id_el = next(p for p in elements if p.order() == 1)
            
            if sympy.isprime(d):
                elements_of_order_d = sum(1 for x in elements if x.order() == d)
                count = elements_of_order_d // (d - 1)
            else:
                elements.remove(id_el)
                count = 0
                for subset in itertools.combinations(elements, d - 1):
                    full_set = set(subset)
                    full_set.add(id_el)
                    closed = True
                    for a in subset:
                        if ~a not in full_set:
                            closed = False
                            break
                        for b in subset:
                            if a * b not in full_set:
                                closed = False
                                break
                        if not closed:
                            break
                    if closed:
                        count += 1
        neg_q = (count != 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]