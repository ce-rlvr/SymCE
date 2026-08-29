import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def conditions(witness) -> list[bool]:
    # Expected witness format:
    # witness = (n, m, f_dict, k)
    # where:
    #   n: integer (1 <= n <= 100), representing the ring R = Z/nZ
    #   m: integer (1 <= m <= 100), representing the ring S = Z/mZ
    #   f_dict: dictionary mapping each x in 0..n-1 to an element in 0..m-1, representing f: R -> S
    #   k: integer (1 <= k <= n) dividing n, representing the ideal I = kZ/nZ
    
    try:
        n, m, f_dict, k = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = isinstance(n, int) and 1 <= n <= 100 and isinstance(m, int) and 1 <= m <= 100
        h1 = h1 and isinstance(f_dict, dict)
        h1 = h1 and all(x in f_dict for x in range(n))
        h1 = h1 and all(isinstance(y, int) and 0 <= y < m for y in f_dict.values())
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(k, int) and 1 <= k <= n and n % k == 0
        if h2:
            for x in range(n):
                if x % k == 0:
                    if f_dict[x] != 0:
                        h2 = False
                        break
    except Exception:
        h2 = False
        
    # pi: R -> R/I is inherently the canonical projection x -> x mod k in our model
    h3 = True
    
    try:
        factors = True
        f_bar = {}
        for x in range(n):
            rem = x % k
            if rem in f_bar:
                if f_bar[rem] != f_dict[x]:
                    factors = False
                    break
            else:
                f_bar[rem] = f_dict[x]
        
        valid_f_bars = 0
        if factors:
            is_hom = True
            # Check if f_bar preserves addition and multiplication
            for a in range(k):
                for b in range(k):
                    if f_bar[(a + b) % k] != (f_bar[a] + f_bar[b]) % m:
                        is_hom = False
                        break
                    if f_bar[(a * b) % k] != (f_bar[a] * f_bar[b]) % m:
                        is_hom = False
                        break
                if not is_hom:
                    break
            
            # Check if f_bar preserves the multiplicative identity
            id_R = 1 % k
            id_S = 1 % m
            if f_bar[id_R] != id_S:
                is_hom = False
                
            if is_hom:
                valid_f_bars = 1
                
        neg_q = (valid_f_bars != 1)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: I is an ideal of R such that I is a subset of ker(f)",
    "H_3: pi: R -> R/I is the canonical projection homomorphism",
    "¬Q: There does not exist a unique ring homomorphism f_bar: R/I -> S such that f = f_bar o pi"
]

N_HYP = 3
NEG_Q_INDEX = 3