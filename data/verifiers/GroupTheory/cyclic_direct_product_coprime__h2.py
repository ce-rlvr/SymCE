import math
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, CyclicGroup, DihedralGroup, AlternatingGroup, AbelianGroup
)

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, H, m, n) or a dictionary with these keys.
    """
    if isinstance(witness, dict):
        G = witness.get('G')
        H = witness.get('H')
        m = witness.get('m')
        n = witness.get('n')
    else:
        try:
            G, H, m, n = witness
        except Exception:
            return [False, False, False, False]

    # H_1: m and n are positive integers
    try:
        m_val = int(m)
        n_val = int(n)
        h1 = (m_val == m) and (n_val == n) and m_val > 0 and n_val > 0
        m, n = m_val, n_val
    except Exception:
        h1 = False

    # H_2: H is a cyclic group of order n
    try:
        h2 = isinstance(H, PermutationGroup) and H.is_cyclic and H.order() == n
    except Exception:
        h2 = False

    # H_3: gcd(m, n) = 1
    try:
        h3 = math.gcd(m, n) == 1
    except Exception:
        h3 = False

    # neg_Q: The direct product G x H is a cyclic group of order mn (must FAIL)
    try:
        if not isinstance(G, PermutationGroup) or not isinstance(H, PermutationGroup):
            neg_q = True
        else:
            order_eq = (G.order() * H.order() == m * n)
            if not order_eq:
                is_cyclic_mn = False
            else:
                is_cyclic_mn = False
                try:
                    g_elems = list(G.elements)
                except Exception:
                    g_elems = list(G.generate())
                try:
                    h_elems = list(H.elements)
                except Exception:
                    h_elems = list(H.generate())
                    
                for g in g_elems:
                    for h in h_elems:
                        go = g.order()
                        ho = h.order()
                        lcm_val = (go * ho) // math.gcd(go, ho)
                        if lcm_val == m * n:
                            is_cyclic_mn = True
                            break
                    if is_cyclic_mn:
                        break
            neg_q = not is_cyclic_mn
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: m and n are positive integers",
    "H_2: H is a cyclic group of order n",
    "H_3: gcd(m, n) = 1",
    "¬Q: The direct product G x H is not a cyclic group of order mn"
]

N_HYP = 3
NEG_Q_INDEX = 3