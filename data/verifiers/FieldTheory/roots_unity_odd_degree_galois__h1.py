import sympy
import sympy.combinatorics
import sympy.matrices
from sympy import Symbol, cyclotomic_poly, factor_list
from sympy.ntheory import factorint

S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    H1 = False
    H2 = False
    H3 = False
    neg_Q = False

    try:
        if isinstance(witness, tuple) and len(witness) == 3 and all(isinstance(x, int) for x in witness):
            q, d, n = witness
            
            def is_prime_power(k):
                if k < 2: return False
                return len(factorint(k)) == 1
            
            if is_prime_power(q):
                H1 = (d % 2 == 1)
                H2 = (n >= 1)
                
                K_has_root = ((q - 1) % (2**n) == 0)
                H3 = not K_has_root
                
                L_has_root = ((q**d - 1) % (2**n) == 0)
                neg_Q = L_has_root
                
                return [H1, H2, H3, neg_Q]
    except Exception:
        pass

    try:
        K, L, n = witness
        
        try:
            deg_L = L.degree()
            deg_K = K.degree()
            H1 = (deg_L % deg_K == 0) and ((deg_L // deg_K) % 2 == 1)
        except Exception:
            H1 = False

        try:
            H2 = (isinstance(n, int) and n >= 1)
        except Exception:
            H2 = False

        try:
            x = Symbol('x')
            poly = cyclotomic_poly(2**n, x)
            
            facs_K = factor_list(poly, extension=K.ext)[1]
            K_has_root = any(fac.as_poly(x).degree() == 1 for fac, mult in facs_K)
            H3 = not K_has_root
        except Exception:
            H3 = False

        try:
            facs_L = factor_list(poly, extension=L.ext)[1]
            L_has_root = any(fac.as_poly(x).degree() == 1 for fac, mult in facs_L)
            neg_Q = L_has_root
        except Exception:
            neg_Q = False

    except Exception:
        pass

    return [H1, H2, H3, neg_Q]

CONDITION_LABELS = [
    "H_1: The degree of L over K is an odd integer",
    "H_2: n >= 1 is an integer",
    "H_3: K does not contain a primitive 2^n-th root of unity",
    "not Q: The field L DOES contain a primitive 2^n-th root of unity"
]

N_HYP = 3
NEG_Q_INDEX = 3