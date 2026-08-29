import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness should be a tuple (m, f_dict, g_dict) where:
      - m is an integer >= 2 representing the ring R = Z/mZ.
      - f_dict is a dictionary {degree: coefficient} representing the formal Laurent series f(x).
      - g_dict is a dictionary {degree: coefficient} representing the inverse series g(x).
    """
    try:
        m, f_dict, g_dict = witness
    except Exception:
        return [False, False, False]
        
    # H1: R is a commutative ring with identity
    try:
        m = int(m)
        h1 = (m >= 2)
    except Exception:
        h1 = False
        
    # H2: f(x) is a formal Laurent series over R
    try:
        f_dict_clean = {int(k): int(v) for k, v in f_dict.items()}
        g_dict_clean = {int(k): int(v) for k, v in g_dict.items()}
        h2 = True
    except Exception:
        h2 = False
        
    # Negated Conclusion: f(x) is a unit in R((x)) AND its lowest degree non-zero coefficient is NOT a unit in R
    try:
        if not h1 or not h2:
            neg_q = False
        else:
            # Reduce coefficients modulo m and remove zero terms
            f_mod = {k: v % m for k, v in f_dict_clean.items() if v % m != 0}
            g_mod = {k: v % m for k, v in g_dict_clean.items() if v % m != 0}
            
            if not f_mod or not g_mod:
                neg_q = False
            else:
                # Multiply f(x) and g(x) in R((x))
                prod = {}
                for k1, v1 in f_mod.items():
                    for k2, v2 in g_mod.items():
                        prod[k1+k2] = (prod.get(k1+k2, 0) + v1 * v2) % m
                prod_clean = {k: v for k, v in prod.items() if v != 0}
                
                # Check if f(x) * g(x) == 1
                is_unit = (prod_clean == {0: 1})
                
                # Find the lowest degree non-zero coefficient a_k
                k_min = min(f_mod.keys())
                a_k = f_mod[k_min]
                
                # Check if a_k is a unit in Z/mZ
                ak_is_unit = (math.gcd(a_k, m) == 1)
                
                neg_q = is_unit and not ak_is_unit
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: f(x) is a formal Laurent series over R",
    "¬Q: f(x) is a unit in R((x)) but its lowest degree non-zero coefficient is not a unit in R"
]

N_HYP = 2
NEG_Q_INDEX = 2