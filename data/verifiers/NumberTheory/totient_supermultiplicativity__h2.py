import sympy
from sympy import gcd
from sympy.ntheory import totient as sympy_totient
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            m = witness.get('m')
            n = witness.get('n')
        else:
            m, n = witness
    except Exception:
        return [False, False]

    # H_1: m is a positive integer
    try:
        h1_ok = isinstance(m, (int, sympy.Integer)) and not isinstance(m, bool) and int(m) > 0
    except Exception:
        h1_ok = False

    # neg_Q: Conclusion fails
    try:
        if not (isinstance(m, (int, sympy.Integer)) and not isinstance(m, bool) and 
                isinstance(n, (int, sympy.Integer)) and not isinstance(n, bool)):
            neg_q_ok = False
        else:
            m_int = int(m)
            n_int = int(n)
            
            def totient(x):
                if x == 0:
                    return 0
                return int(sympy_totient(abs(x)))
            
            t_mn = totient(m_int * n_int)
            t_m = totient(m_int)
            t_n = totient(n_int)
            
            part1 = (t_mn >= t_m * t_n)
            equality = (t_mn == t_m * t_n)
            gcd_is_1 = (gcd(m_int, n_int) == 1)
            part2 = (equality == gcd_is_1)
            
            Q = part1 and part2
            neg_q_ok = not Q
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: m is a positive integer",
    "¬Q: phi(mn) < phi(m)phi(n) or (equality holds XOR gcd(m, n) == 1)"
]

N_HYP = 1
NEG_Q_INDEX = 1