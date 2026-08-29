import math
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

# Standard group theory bindings
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

# Standard linear algebra bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: S_m and S_n are the symmetric groups of degree m and n, respectively",
    "¬Q: S_m \\wr S_n is not isomorphic to a subgroup of S_{mn}"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    try:
        # The witness should be a tuple of degrees (m, n) or a tuple of symmetric groups
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        
        m_obj, n_obj = witness
        
        # Check if the witness provides permutation groups
        if hasattr(m_obj, 'degree') and hasattr(n_obj, 'degree'):
            m = m_obj.degree
            n = n_obj.degree
            try:
                # A subgroup of S_k with order k! is exactly S_k
                is_sym_m = (m_obj.order() == math.factorial(m))
                is_sym_n = (n_obj.order() == math.factorial(n))
                h1 = is_sym_m and is_sym_n
            except Exception:
                h1 = False
        else:
            # Otherwise, assume the witness provides the degrees directly
            try:
                m = int(m_obj)
                n = int(n_obj)
                # Ensure they were actually integers (reject floats like 2.5)
                if m != m_obj or n != n_obj:
                    return [False, False]
                # Degrees of symmetric groups must be non-negative
                h1 = (m >= 0) and (n >= 0)
            except Exception:
                return [False, False]
            
        # Prevent DOS from excessively large degrees
        if m > 100 or n > 100:
            return [False, False]
            
    except Exception:
        return [False, False]
        
    try:
        if not h1:
            neg_q = False
        else:
            # Order of the wreath product S_m \wr S_n is (m!)^n * n!
            order_wreath = (math.factorial(m)**n) * math.factorial(n)
            # Order of the symmetric group S_{mn} is (mn)!
            order_s_mn = math.factorial(m * n)
            
            # If S_m \wr S_n is isomorphic to a subgroup of S_{mn}, its order must divide the order of S_{mn}.
            # For m >= 1, the standard imprimitive action guarantees it embeds.
            # For m = 0 and n >= 2, the order of the wreath product is n! > 1, while S_{0} has order 1,
            # making it impossible to embed.
            neg_q = (order_s_mn % order_wreath != 0) or (order_wreath > order_s_mn)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]
