import math
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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
        is_list_of_tuples = isinstance(witness, (list, tuple)) and all(
            isinstance(c, tuple) and 
            all(isinstance(x, int) and x >= 0 for x in c) and 
            len(set(c)) == len(c) 
            for c in witness
        )
        is_list_of_perms = isinstance(witness, (list, tuple)) and all(isinstance(c, Permutation) for c in witness)
        h1 = is_list_of_tuples or is_list_of_perms
    except Exception:
        h1 = False

    try:
        h2 = h1
    except Exception:
        h2 = False

    try:
        if not h1:
            neg_q = False
        else:
            if is_list_of_tuples:
                max_val = -1
                for c in witness:
                    if c:
                        max_val = max(max_val, max(c))
                
                if max_val == -1:
                    order = 1
                    lcm = 1
                else:
                    size = max_val + 1
                    p = Permutation(list(range(size)))
                    for c in witness:
                        if not c:
                            continue
                        c_arr = list(range(size))
                        for i in range(len(c)):
                            c_arr[c[i]] = c[(i + 1) % len(c)]
                        p = p * Permutation(c_arr)
                    
                    order = p.order()
                    
                    lcm = 1
                    for c in witness:
                        m = len(c)
                        if m > 0:
                            lcm = (lcm * m) // math.gcd(lcm, m)
            else:
                p = Permutation()
                for c in witness:
                    p = p * c
                order = p.order()
                
                lcm = 1
                for c in witness:
                    m = c.order()
                    lcm = (lcm * m) // math.gcd(lcm, m)
                    
            neg_q = bool(order != lcm)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: sigma is decomposed into cycles c_1 ... c_k",
    "H_2: m_i is the length of the cycle c_i",
    "¬Q: The order of sigma is not the least common multiple of the cycle lengths"
]

N_HYP = 2
NEG_Q_INDEX = 2