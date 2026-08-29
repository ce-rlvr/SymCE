import math
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup
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
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be either a PermutationGroup G, or a tuple (n, G).
    """
    # H1: n is a positive integer (and G is a permutation group on n elements)
    try:
        if isinstance(witness, tuple):
            n, G = witness
        else:
            G = witness
            n = G.degree
        h1 = isinstance(n, int) and n > 0 and hasattr(G, 'degree') and G.degree <= n
    except Exception:
        h1 = False

    # H2: G contains a 3-cycle
    try:
        if isinstance(witness, tuple):
            _, G = witness
        else:
            G = witness
        
        has_3_cycle = False
        if hasattr(G, 'generate'):
            for i, p in enumerate(G.generate()):
                if i > 100000:  # Safety break for extremely large groups
                    break
                cycles = [c for c in p.cyclic_form if len(c) > 1]
                if len(cycles) == 1 and len(cycles[0]) == 3:
                    has_3_cycle = True
                    break
        h2 = has_3_cycle
    except Exception:
        h2 = False

    # neg_Q: G is neither the alternating group A_n nor the symmetric group S_n
    try:
        if isinstance(witness, tuple):
            n, G = witness
        else:
            G = witness
            n = G.degree
        
        if not isinstance(n, int) or n <= 0:
            neg_q = False
        elif not hasattr(G, 'degree') or not hasattr(G, 'order'):
            neg_q = False
        elif G.degree > n:
            neg_q = True
        else:
            order_G = G.order()
            fact_n = math.factorial(n)
            
            is_Sn = (order_G == fact_n)
            is_An = (order_G == fact_n // 2) if n > 1 else (order_G == 1)
            
            neg_q = not (is_Sn or is_An)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: G contains a 3-cycle",
    "¬Q: G is neither the alternating group A_n nor the symmetric group S_n"
]

N_HYP = 2
NEG_Q_INDEX = 2