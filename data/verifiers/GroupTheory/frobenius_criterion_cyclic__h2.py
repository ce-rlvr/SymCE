import math
import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
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

def conditions(witness) -> list[bool]:
    try:
        # The dropped hypothesis was "of order n", leaving n as a free variable.
        # The witness can provide n explicitly, or we default to n=1 which trivially satisfies H_2.
        if isinstance(witness, dict) and 'G' in witness and 'n' in witness:
            G = witness['G']
            n = witness['n']
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            G, n = witness
        else:
            G = witness
            n = 1
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: For every positive integer d dividing n, the equation x^d = e has at most d solutions in G
    try:
        if not isinstance(n, int) or n < 1:
            h2_ok = False
        else:
            h2_ok = True
            elements = list(G.elements)
            identity = G.identity
            
            # Find all divisors of n
            divisors = []
            for i in range(1, int(math.sqrt(n)) + 1):
                if n % i == 0:
                    divisors.append(i)
                    if i * i != n:
                        divisors.append(n // i)
            
            for d in divisors:
                solutions = sum(1 for g in elements if g**d == identity)
                if solutions > d:
                    h2_ok = False
                    break
    except Exception:
        h2_ok = False

    # ¬Q: G is not a cyclic group
    try:
        order = G.order()
        is_cyclic = any(g.order() == order for g in list(G.elements))
        neg_q_ok = not is_cyclic
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: For every positive integer d dividing n, the equation x^d = e has at most d solutions in G",
    "¬Q: G is not a cyclic group"
]

N_HYP = 2
NEG_Q_INDEX = 2