import sympy as sp
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

# Top-level setup for potential witness references
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Isomorphic to the Klein four-group
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
    R_mod = 0
    n, m = None, None
    
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 2:
                n, m = witness
            elif len(witness) >= 3:
                R_ring = witness[0]
                n, m = witness[1], witness[2]
                try:
                    if hasattr(R_ring, 'order'):
                        R_mod = int(R_ring.order())
                    else:
                        R_mod = abs(int(R_ring))
                except Exception:
                    pass
        else:
            n, m = witness[0], witness[1]
    except Exception:
        pass

    # H_1: R is a commutative ring
    # We verify this by checking if the ideal generators n and m are valid integers or polynomials
    h1 = False
    if n is not None and m is not None:
        try:
            int(n)
            int(m)
            h1 = True
        except Exception:
            try:
                sp.sympify(n)
                sp.sympify(m)
                h1 = True
            except Exception:
                pass

    # ¬Q: There exists a non-zero R-module homomorphism from R/I to R/J
    neg_q = False
    if h1:
        try:
            # Try integer / Z_k logic
            n_int = abs(int(n))
            m_int = abs(int(m))
            
            if R_mod > 0:
                n_int = math.gcd(R_mod, n_int)
                m_int = math.gcd(R_mod, m_int)
                
            if m_int == 1:
                neg_q = False
            elif m_int == 0:
                neg_q = (n_int == 0)
            else:
                neg_q = math.gcd(n_int, m_int) > 1
                
        except Exception:
            # Try polynomial logic (e.g., over ZZ[x] or QQ[x])
            try:
                n_poly = sp.sympify(n)
                m_poly = sp.sympify(m)
                
                if m_poly == 1 or m_poly == -1:
                    neg_q = False
                elif m_poly == 0:
                    neg_q = (n_poly == 0)
                else:
                    g = sp.gcd(n_poly, m_poly)
                    if g == 1 or g == -1:
                        neg_q = False
                    else:
                        neg_q = True
            except Exception:
                neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: There exists a non-zero R-module homomorphism from R/I to R/J"
]

N_HYP = 1
NEG_Q_INDEX = 1