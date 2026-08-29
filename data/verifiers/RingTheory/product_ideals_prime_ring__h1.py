import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: I is a non-zero ideal of R",
    "H_2: J is a non-zero ideal of R",
    "¬Q: The product ideal IJ is the zero ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    h1, h2, neg_q = False, False, False
    try:
        # The witness is expected to be a tuple (R, I, J)
        # R can be an integer n (representing the ring Z/nZ) 
        # or a list/tuple/set of elements (e.g., matrices) representing a finite ring.
        if len(witness) != 3:
            return [False, False, False]
        R, I, J = witness
        
        if isinstance(R, int):
            n = R
            if n > 1:
                def is_ideal(S):
                    if not S: return False
                    try:
                        S_mod = set(x % n for x in S)
                    except Exception:
                        return False
                    # Check closure under addition
                    for a in S_mod:
                        for b in S_mod:
                            if (a + b) % n not in S_mod:
                                return False
                    # Check closure under multiplication by any ring element
                    for a in S_mod:
                        for r in range(n):
                            if (a * r) % n not in S_mod:
                                return False
                    return True
                
                def is_nonzero(S):
                    try:
                        return any(x % n != 0 for x in S)
                    except Exception:
                        return False
                
                h1 = is_ideal(I) and is_nonzero(I)
                h2 = is_ideal(J) and is_nonzero(J)
                
                # Check if IJ is the zero ideal (all products i*j must be 0 mod n)
                neg_q = True
                for i in I:
                    for j in J:
                        if (i * j) % n != 0:
                            neg_q = False
                            break
                            
        elif isinstance(R, (list, tuple, set)):
            R_list = list(R)
            I_list = list(I)
            J_list = list(J)
            
            # Verify R is closed under addition and multiplication (a valid finite ring)
            is_ring = True
            for a in R_list:
                for b in R_list:
                    if (a + b) not in R_list:
                        is_ring = False
                        break
                    if (a * b) not in R_list:
                        is_ring = False
                        break
                if not is_ring:
                    break
            
            if is_ring:
                def is_zero_element(val):
                    if hasattr(val, 'is_zero') and val.is_zero is not None:
                        return val.is_zero
                    if isinstance(val, sympy.MatrixBase):
                        return all(v == 0 for v in val)
                    return val == 0

                def is_ideal(S):
                    if not S: return False
                    # Check subset
                    for s in S:
                        if s not in R_list: return False
                    # Check closure under addition
                    for a in S:
                        for b in S:
                            if (a + b) not in S: return False
                    # Check closure under left and right multiplication by R
                    for a in S:
                        for r in R_list:
                            if (a * r) not in S: return False
                            if (r * a) not in S: return False
                    return True
                    
                def is_nonzero(S):
                    return any(not is_zero_element(x) for x in S)
                    
                h1 = is_ideal(I_list) and is_nonzero(I_list)
                h2 = is_ideal(J_list) and is_nonzero(J_list)
                
                # Check if IJ is the zero ideal
                neg_q = True
                for i in I_list:
                    for j in J_list:
                        if not is_zero_element(i * j):
                            neg_q = False
                            break
    except Exception:
        pass
        
    return [bool(h1), bool(h2), bool(neg_q)]