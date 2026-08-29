import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory

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

def get_size(F):
    if isinstance(F, int):
        return F
    try:
        if hasattr(F, 'order'):
            o = F.order
            if callable(o): return o()
            return o
        if hasattr(F, 'p') and hasattr(F, 'deg'):
            return F.p ** F.deg
    except Exception:
        pass
    try:
        return int(F)
    except Exception:
        return None

def is_prime_power(n):
    try:
        if n < 2:
            return False
        factors = sympy.ntheory.factorint(n)
        return len(factors) == 1
    except Exception:
        return False

def is_power(a, b):
    if not isinstance(a, int) or not isinstance(b, int):
        return False
    if b <= 1 or a < b:
        return False
    p = b
    while p < a:
        p *= b
    return p == a

def trace(alpha, size_base, size_ext):
    d = 0
    p = 1
    while p < size_ext:
        p *= size_base
        d += 1
    if p != size_ext:
        raise ValueError("size_ext is not a power of size_base")
    
    res = alpha
    for i in range(1, d):
        res = res + alpha**(size_base**i)
    return res

def check_equal(lhs, rhs):
    if lhs == rhs:
        return True
    try:
        diff = lhs - rhs
        if hasattr(diff, 'is_zero_matrix') and diff.is_zero_matrix:
            return True
        if hasattr(diff, 'simplify'):
            diff = diff.simplify()
        if diff == 0:
            return True
        if sympy.simplify(diff) == 0:
            return True
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    h1, h2, h3, neg_q = False, False, False, False
    try:
        if isinstance(witness, dict):
            q = witness.get('q', witness.get('F_q'))
            K = witness.get('K')
            L = witness.get('L')
            alpha = witness.get('alpha')
        else:
            q, K, L, alpha = witness
            
        if isinstance(alpha, str):
            alpha = sympy.Symbol(alpha)
            
        q_val = get_size(q)
        K_val = get_size(K)
        L_val = get_size(L)
        
        if q_val is not None and K_val is not None and L_val is not None:
            # Fallback: if K and L are not powers, they might be degrees instead of sizes
            if not (is_power(K_val, q_val) and is_power(L_val, K_val)):
                try:
                    K_size = q_val ** K_val
                    L_size = K_size ** L_val
                    if is_power(K_size, q_val) and is_power(L_size, K_size):
                        K_val = K_size
                        L_val = L_size
                except Exception:
                    pass
                    
            h1 = bool(is_prime_power(q_val))
            h2 = bool(is_power(K_val, q_val))
            h3 = bool(is_power(L_val, K_val))
    except Exception:
        pass

    try:
        if h1 and h2 and h3:
            lhs = trace(alpha, q_val, L_val)
            inner = trace(alpha, K_val, L_val)
            rhs = trace(inner, q_val, K_val)
            neg_q = not check_equal(lhs, rhs)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: K is a finite field extension of F_q",
    "H_3: L is a finite field extension of K",
    "¬Q: Tr_{L/F_q}(alpha) != Tr_{K/F_q}(Tr_{L/K}(alpha))"
]

N_HYP = 3
NEG_Q_INDEX = 3