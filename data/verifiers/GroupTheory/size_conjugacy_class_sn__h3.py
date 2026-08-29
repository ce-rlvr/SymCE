import sympy
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False]
        n, C, m = witness
    except Exception:
        return [False, False, False]
        
    # H1: n is a positive integer
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and int(n) > 0
    except Exception:
        h1 = False
        
    # H2: C is a conjugacy class in S_n
    try:
        h2 = False
        if hasattr(C, '__iter__') and not isinstance(C, (str, dict)):
            C_list = list(C)
            if len(C_list) > 0 and all(isinstance(p, Permutation) for p in C_list):
                valid_Sn = True
                for p in C_list:
                    supp = p.support()
                    if supp and max(supp) >= n:
                        valid_Sn = False
                        break
                if valid_Sn:
                    C_normalized = []
                    for p in C_list:
                        arr = tuple(p(i) for i in range(n))
                        C_normalized.append(arr)
                    if len(set(C_normalized)) == len(C_list):
                        def get_ct(p):
                            struct = p.cycle_structure
                            moved = sum(k * v for k, v in struct.items())
                            ct = {k: v for k, v in struct.items()}
                            ct[1] = n - moved
                            return ct
                        
                        ct0 = get_ct(C_list[0])
                        if all(get_ct(p) == ct0 for p in C_list):
                            denom = 1
                            for k, v in ct0.items():
                                denom *= (k**v) * math.factorial(v)
                            if math.factorial(n) % denom == 0:
                                expected_size = math.factorial(n) // denom
                                if len(C_list) == expected_size:
                                    h2 = True
    except Exception:
        h2 = False
        
    # neg_Q: The number of elements in C is not n! / ∏_{k=1}^n (k^{m_k} · m_k!)
    try:
        if callable(m):
            get_m = m
        elif hasattr(m, 'get'):
            get_m = lambda k: m.get(k, 0)
        else:
            m_list = list(m)
            get_m = lambda k: m_list[k-1] if k-1 < len(m_list) else 0
            
        denom = 1
        for k in range(1, n + 1):
            try:
                mk = int(get_m(k))
            except Exception:
                denom = 0
                break
            if mk < 0:
                denom = 0
                break
            denom *= (k**mk) * math.factorial(mk)
            
        if denom == 0:
            neg_q = True
        else:
            if math.factorial(n) % denom != 0:
                neg_q = True
            else:
                expected_formula_size = math.factorial(n) // denom
                neg_q = len(C) != expected_formula_size
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: C is a conjugacy class in the symmetric group S_n",
    "¬Q: The number of elements in C is not n! / ∏_{k=1}^n (k^{m_k} · m_k!)"
]

N_HYP = 2
NEG_Q_INDEX = 2