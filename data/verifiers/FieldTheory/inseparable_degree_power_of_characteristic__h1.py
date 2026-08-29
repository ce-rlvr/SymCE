import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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

def is_power_of_p(n, p):
    try:
        if n == sympy.oo or n == float('inf'):
            return False
        if int(n) != n:
            return False
        n = int(n)
        p = int(p)
        if n <= 0:
            return False
        while n > 1:
            if n % p != 0:
                return False
            n = n // p
        return True
    except Exception:
        return False

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            p = witness.get('char', 0)
            is_fin = witness.get('is_finite_extension', False)
            deg_i = witness.get('inseparable_degree', 0)
        elif isinstance(witness, (list, tuple)) and len(witness) >= 3:
            p = witness[0]
            is_fin = witness[1]
            deg_i = witness[2]
        else:
            p = getattr(witness, 'char', 0)
            is_fin = getattr(witness, 'is_finite_extension', False)
            deg_i = getattr(witness, 'inseparable_degree', 0)
            
        try:
            p_val = int(p)
            if p_val > 0 and sympy.isprime(p_val):
                h1 = True
        except Exception:
            h1 = False
            
        try:
            h2 = bool(is_fin)
        except Exception:
            h2 = False
            
        try:
            if h1:
                neg_q = not is_power_of_p(deg_i, p_val)
            else:
                neg_q = False
        except Exception:
            neg_q = False
            
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The characteristic of F is a prime p > 0",
    "H_2: E/F is a finite field extension",
    "¬Q: The inseparable degree is not an integer power of p"
]

N_HYP = 2
NEG_Q_INDEX = 2