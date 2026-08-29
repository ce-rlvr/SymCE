import sympy
import math
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def exact_log(n, b):
    d = 0
    curr = 1
    while curr < n:
        curr *= b
        d += 1
    if curr == n:
        return d
    return -1

def get_p_d(witness):
    """
    Parses the witness to extract the characteristic p and the degree d of the extension L/K.
    The witness is expected to be a tuple representing (K, L) or (p, d).
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            K, L = witness
            
            # Case 1: witness is (p, d)
            if isinstance(K, int) and (isinstance(L, int) or L == sympy.oo):
                if sympy.isprime(K) and (L == sympy.oo or L >= 1):
                    return K, L
                    
            p = None
            
            # Extract characteristic p from K
            if hasattr(K, 'characteristic'):
                p = K.characteristic
                if callable(p): p = p()
            elif isinstance(K, int) and sympy.isprime(K):
                p = K
                
            if p is not None and sympy.isprime(p):
                # Extract degree d from L
                if hasattr(L, 'order'):
                    order_L = L.order
                    if callable(order_L): order_L = order_L()
                    d_L = exact_log(order_L, p)
                    
                    if hasattr(K, 'order'):
                        order_K = K.order
                        if callable(order_K): order_K = order_K()
                        d_K = exact_log(order_K, p)
                    else:
                        d_K = 1
                        
                    if d_L != -1 and d_K != -1 and d_L % d_K == 0:
                        return p, d_L // d_K
                elif isinstance(L, int) or L == sympy.oo:
                    if L == sympy.oo or L >= 1:
                        return p, L
    except Exception:
        pass
    return None, None

def conditions(witness) -> list[bool]:
    p, d = get_p_d(witness)
    
    # H_1: Let K be a field of prime characteristic p.
    try:
        h1 = (p is not None and sympy.isprime(p))
    except Exception:
        h1 = False
        
    # ¬Q: The conclusion fails.
    # Conclusion: There exists an element alpha in L such that L = K(alpha) 
    # and alpha is a root of the polynomial x^p - x - a for some a in K.
    # By Artin-Schreier theory, for a in K, x^p - x - a either splits completely in K (if a = 0)
    # or is irreducible over K with a splitting field of degree p (if a != 0).
    # Thus, K(alpha) can only have degree 1 or p over K.
    # The conclusion holds if and only if the degree d of L/K is 1 or p.
    # Therefore, the conclusion FAILS (neg_Q is True) iff d != 1 and d != p.
    try:
        if p is not None and d is not None:
            neg_q = (d != 1) and (d != p)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field of prime characteristic p",
    "¬Q: There is no alpha in L such that L = K(alpha) and alpha is a root of x^p - x - a for some a in K"
]

N_HYP = 1
NEG_Q_INDEX = 1