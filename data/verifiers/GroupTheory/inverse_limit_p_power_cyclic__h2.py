import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: The transition maps of the inverse system are the natural projections",
    "¬Q: The inverse limit of {G_n} is not isomorphic to the additive group of p-adic integers Z_p"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        p, m_obj = witness
    except Exception:
        return [False, False, False]
        
    def get_m(n):
        try:
            if callable(m_obj):
                val = m_obj(n)
            elif isinstance(m_obj, (list, tuple)):
                idx = n - 1
                if len(m_obj) == 0:
                    val = 1
                else:
                    val = m_obj[idx] if idx < len(m_obj) else m_obj[-1]
            else:
                val = m_obj
                
            if hasattr(val, 'order'):
                return int(val.order())
            return int(val)
        except Exception:
            return -1

    # H_1: p is a prime number
    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False

    # H_2: The transition maps of the inverse system are the natural projections
    # For G_n = Z/m_n Z, the natural projection to Z/m_{n-1} Z exists iff m_{n-1} divides m_n
    try:
        h2 = True
        for n in range(1, 51):
            mn = get_m(n)
            mn1 = get_m(n+1)
            if mn == -1 or mn1 == -1:
                h2 = False
                break
            if mn == 0:
                if mn1 != 0:
                    h2 = False
                    break
            else:
                if mn1 % mn != 0:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # ¬Q: The inverse limit of {G_n} is not isomorphic to Z_p
    try:
        is_Zp = True
        if not isinstance(p, int):
            is_Zp = False
        else:
            powers = []
            for n in range(1, 51):
                val = get_m(n)
                if val <= 0:
                    is_Zp = False
                    break
                cnt = 0
                while val > 0 and val % p == 0:
                    cnt += 1
                    val //= p
                if val != 1:
                    # Has prime factors other than p
                    is_Zp = False
                    break
                powers.append(cnt)
                
            if is_Zp and len(powers) == 50:
                # If the sequence of p-powers eventually stabilizes, the inverse limit is finite, not Z_p
                if powers[-1] == powers[-10]:
                    is_Zp = False
                    
        neg_q = not is_Zp
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]