import sympy
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

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
        p, G, x = witness
    except Exception:
        return [False, False, False]
        
    # H_1: p is a prime number
    try:
        h1_ok = bool(isprime(p))
    except Exception:
        h1_ok = False
        
    # H_2: x is an element of G
    try:
        h2_ok = bool(G.contains(x))
    except Exception:
        h2_ok = False
        
    # neg_Q: The size of the conjugacy class of x in G is not a power of p
    try:
        orbit = set()
        for g in G.generate():
            orbit.add(g * x * ~g)
        size = len(orbit)
        
        is_power = False
        if size == 1:
            is_power = True
        else:
            try:
                p_val = int(p)
                if p_val >= 2:
                    temp = size
                    while temp % p_val == 0:
                        temp = temp // p_val
                    if temp == 1:
                        is_power = True
            except Exception:
                pass
                
        neg_q_ok = not is_power
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: x is an element of G",
    "¬Q: The size of the conjugacy class of x in G is not a power of p"
]

N_HYP = 2
NEG_Q_INDEX = 2