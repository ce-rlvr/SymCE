import math
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness expressions
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
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The dropped hypothesis was that the cycles must be disjoint.
    
    Expected witness format: (sigma, cycles)
    where `sigma` is a sympy Permutation and `cycles` is a list of lists of integers.
    Example of a counterexample: (Permutation(1, 3, 2), [[1, 2], [2, 3]])
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        
        sigma, cycles = witness
        
        # H_1: sigma is a permutation in S_n
        h1 = isinstance(sigma, Permutation)
        
        # H_2: sigma = c_1 c_2 ... c_k is a decomposition of sigma into cycles
        # We verify that sigma is indeed the product of the provided cycles.
        # We do NOT enforce disjointness, as that is the dropped hypothesis.
        h2 = False
        if isinstance(cycles, list) and all(isinstance(c, list) for c in cycles):
            if all(all(isinstance(x, int) for x in c) for c in cycles):
                # Ensure each cycle is well-formed (contains distinct elements)
                if all(len(c) == len(set(c)) for c in cycles):
                    p_lr = Permutation()
                    p_rl = Permutation()
                    for c in cycles:
                        if len(c) > 0:
                            pc = Permutation([c])
                            p_lr = p_lr * pc
                            p_rl = pc * p_rl
                    # Accept either left-to-right or right-to-left multiplication conventions
                    if sigma == p_lr or sigma == p_rl:
                        h2 = True
                        
        # neg_Q: The order of sigma is NOT the least common multiple of the cycle lengths
        lcm = 1
        if isinstance(cycles, list):
            for c in cycles:
                if isinstance(c, list):
                    l = len(c)
                    if l > 0:
                        lcm = (lcm * l) // math.gcd(lcm, l)
                        
        neg_q = False
        if isinstance(sigma, Permutation):
            neg_q = sigma.order() != lcm
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: sigma is a permutation in S_n",
    "H_2: sigma = c_1 c_2 ... c_k is a decomposition of sigma into cycles",
    "¬Q: The order of sigma is not the least common multiple of the cycle lengths"
]

N_HYP = 2
NEG_Q_INDEX = 2