import math
from sympy.combinatorics import Permutation, SymmetricGroup
from sympy.combinatorics.named_groups import AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup
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

def conditions(witness):
    try:
        # The witness is expected to be a tuple (n, sigma) or (S_n, sigma)
        if isinstance(witness, tuple) and len(witness) == 2:
            n_or_G, sigma = witness
            if isinstance(n_or_G, int):
                n = n_or_G
            elif hasattr(n_or_G, 'degree'):
                n = n_or_G.degree
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: S_n is the symmetric group on n letters
    try:
        h1 = isinstance(n, int) and n >= 1
    except Exception:
        h1 = False

    # H2: sigma is a permutation in S_n
    try:
        h2 = isinstance(sigma, Permutation)
        if h2:
            # A permutation is in S_n if it only moves elements in {0, 1, ..., n-1}
            if sigma.support():
                max_element = max(sigma.support())
                if max_element >= n:
                    h2 = False
    except Exception:
        h2 = False

    # neg_Q: The size of the centralizer of \sigma in S_n is \prod_{k=1}^n k^{m_k} (m_k!).
    # The conjecture is false because it drops the hypothesis that \sigma has no fixed points,
    # or equivalently, it evaluates the formula using the disjoint cycle decomposition of \sigma 
    # (which omits 1-cycles), thus missing the m_1! factor for the fixed points in S_n.
    try:
        # Compute formula size using disjoint cycle decomposition (omitting 1-cycles)
        m = {k: 0 for k in range(1, n + 1)}
        for cycle in sigma.cyclic_form:
            if len(cycle) > 1:
                m[len(cycle)] += 1
        
        formula_size = 1
        for k, count in m.items():
            formula_size *= (k ** count) * math.factorial(count)
            
        # Compute actual centralizer size in S_n (which includes the fixed points)
        elements_in_cycles = sum(len(c) for c in sigma.cyclic_form if len(c) > 1)
        actual_m1 = n - elements_in_cycles
        
        actual_size = math.factorial(actual_m1)
        for k, count in m.items():
            if k > 1:
                actual_size *= (k ** count) * math.factorial(count)
                
        neg_q = (actual_size != formula_size)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S_n is the symmetric group on n letters",
    "H_2: sigma is a permutation in S_n",
    "¬Q: The actual centralizer size differs from the formula (which omits fixed points)"
]

N_HYP = 2
NEG_Q_INDEX = 2