import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

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

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        G, p = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    # neg_Q: G does NOT contain an element of order p
    try:
        if not h1 or not h2:
            neg_q = False
        else:
            try:
                order_val = G.order()
            except TypeError:
                order_val = G.order
                
            # For very large groups, avoid iterating over all elements and use Cauchy's Theorem directly
            if order_val > 2000:
                has_order_p = (order_val % p == 0)
            else:
                try:
                    elements = G.elements
                    if callable(elements):
                        elements = elements()
                except Exception:
                    elements = []
                
                has_order_p = False
                for g in elements:
                    try:
                        g_order = g.order()
                    except TypeError:
                        g_order = g.order
                        
                    if g_order == p:
                        has_order_p = True
                        break
                        
            neg_q = not has_order_p
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "¬Q: G does not contain an element of order p"
]

N_HYP = 2
NEG_Q_INDEX = 2