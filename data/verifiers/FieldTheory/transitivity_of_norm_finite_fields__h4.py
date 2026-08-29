import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint
import math

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

def get_degree(base, target):
    if base <= 1 or target < base:
        if target == 1 and base > 1:
            return 0
        return -1
    deg = 0
    val = 1
    while val < target:
        val *= base
        deg += 1
    if val == target:
        return deg
    return -1

def get_order(F):
    if isinstance(F, int):
        return F
    if hasattr(F, 'order'):
        val = F.order
        return val() if callable(val) else val
    if hasattr(F, 'mod'):
        val = F.mod
        return val() if callable(val) else val
    if hasattr(F, 'p') and hasattr(F, 'd'):
        return (F.p ** F.d)
    raise ValueError("Cannot determine order")

def check_eq(a, b):
    if a == b:
        return True
    try:
        from sympy import simplify
        if simplify(a - b) == 0:
            return True
    except Exception:
        pass
    return False

def is_primepower(n):
    if not isinstance(n, int) or n < 2:
        return False
    factors = factorint(n)
    return len(factors) == 1

def conditions(witness):
    try:
        if isinstance(witness, dict):
            if 'm' in witness and 'n' in witness:
                q = witness['q']
                qK = q ** witness['m']
                qL = qK ** witness['n']
                alpha = witness['alpha']
            else:
                q = get_order(witness['Fq'])
                qK = get_order(witness['K'])
                qL = get_order(witness['L'])
                alpha = witness['alpha']
        else:
            Fq, K, L, alpha = witness
            q = get_order(Fq)
            qK = get_order(K)
            qL = get_order(L)
    except Exception:
        return [False, False, False, False]

    # H1: F_q is a finite field with q elements
    try:
        h1 = bool(is_primepower(q))
    except Exception:
        h1 = False

    # H2: K is a finite field extension of F_q
    try:
        m = get_degree(q, qK)
        h2 = bool(m >= 1)
    except Exception:
        h2 = False

    # H3: L is a finite field extension of K
    try:
        n = get_degree(qK, qL)
        h3 = bool(n >= 1)
    except Exception:
        h3 = False

    # Conclusion: N_{L/F_q}(alpha) == N_{K/F_q}(N_{L/K}(alpha))
    try:
        # For the norm map N_{L/K} to be well-defined, alpha must be an element of L.
        # In a finite field L of order qL, elements satisfy x**qL == x.
        if not check_eq(alpha ** qL, alpha):
            raise ValueError("alpha is not in L")
        
        norm_L_Fq = alpha ** ((qL - 1) // (q - 1))
        norm_L_K = alpha ** ((qL - 1) // (qK - 1))
        
        # The result of N_{L/K}(alpha) must be in K for N_{K/F_q} to be applicable.
        if not check_eq(norm_L_K ** qK, norm_L_K):
            raise ValueError("N_{L/K}(alpha) is not in K")
            
        norm_K_Fq = norm_L_K ** ((qK - 1) // (q - 1))
        
        q_holds = check_eq(norm_L_Fq, norm_K_Fq)
    except Exception:
        # If the norm is undefined (e.g. alpha not in L), the equation fails to hold.
        q_holds = False

    neg_q = not q_holds

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: K is a finite field extension of F_q",
    "H_3: L is a finite field extension of K",
    "¬Q: N_{L/F_q}(alpha) != N_{K/F_q}(N_{L/K}(alpha))"
]

N_HYP = 3
NEG_Q_INDEX = 3