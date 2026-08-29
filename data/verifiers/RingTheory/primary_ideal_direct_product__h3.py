import sympy
from sympy import *
import itertools
import math
import functools

# Top-level setup
# Witnesses are expected to be tuples (n1, n2, q1) representing the rings 
# R1 = Z/n1, R2 = Z/n2, and the ideal Q1 = <q1> in R1.
# Alternatively, Q1 can be provided as an explicit collection of elements.

def conditions(witness):
    try:
        if isinstance(witness, dict):
            if 'n1' in witness:
                n1 = int(witness['n1'])
                n2 = int(witness['n2'])
                if isinstance(witness['q1'], (list, set, tuple)):
                    Q1 = set(int(x) % n1 for x in witness['q1'])
                else:
                    q1 = int(witness['q1'])
                    Q1 = set((i * q1) % n1 for i in range(n1))
            else:
                n1 = len(witness['R1'])
                n2 = len(witness['R2'])
                Q1 = set(int(x) % n1 for x in witness['Q1'])
        else:
            w0, w1, w2 = witness
            if hasattr(w0, '__len__') and hasattr(w1, '__len__') and not isinstance(w0, str):
                n1 = len(w0)
                n2 = len(w1)
            else:
                n1 = int(w0)
                n2 = int(w1)
                
            if hasattr(w2, '__len__') and not isinstance(w2, str):
                Q1 = set(int(x) % n1 for x in w2)
            else:
                q1 = int(w2)
                Q1 = set((i * q1) % n1 for i in range(n1))
    except Exception:
        return [False, False, False]

    try:
        # H1: R1 and R2 are commutative rings with identity
        # We require n1 >= 2 and n2 >= 1 to ensure valid rings with identity.
        h1 = (n1 >= 2 and n2 >= 1)
        
        # H2: R = R1 x R2 is the direct product of R1 and R2
        # This is true by construction in our verifier.
        h2 = h1
        
        if not h1:
            return [False, False, False]
            
        # Prevent excessively large rings that would cause timeouts
        if n1 * n2 > 1000:
            return [False, False, False]
            
        # Check if Q1 is actually an ideal in R1
        is_ideal = True
        if 0 not in Q1:
            is_ideal = False
        else:
            for q in Q1:
                for r in range(n1):
                    if (q * r) % n1 not in Q1:
                        is_ideal = False
                        break
                if not is_ideal:
                    break
            for qa in Q1:
                for qb in Q1:
                    if (qa + qb) % n1 not in Q1:
                        is_ideal = False
                        break
                if not is_ideal:
                    break
                    
        if not is_ideal:
            return [False, False, False]
            
        R_elements = [(x, y) for x in range(n1) for y in range(n2)]
        I_elements = set((x, y) for x in Q1 for y in range(n2))
        
        # Precompute the radical of I to speed up the primary ideal check
        rad_I = set()
        for b in R_elements:
            b_k = b
            for _ in range(n1 * n2):
                if b_k in I_elements:
                    rad_I.add(b)
                    break
                b_k = ((b_k[0] * b[0]) % n1, (b_k[1] * b[1]) % n2)
        
        # Check if I = Q1 x R2 is a primary ideal in R
        # I is primary if I != R and for all a, b in R, ab in I => a in I or b in rad(I)
        is_primary = True
        if len(I_elements) == len(R_elements):
            is_primary = False
        else:
            for a in R_elements:
                for b in R_elements:
                    ab = ((a[0] * b[0]) % n1, (a[1] * b[1]) % n2)
                    if ab in I_elements:
                        if a not in I_elements and b not in rad_I:
                            is_primary = False
                            break
                if not is_primary:
                    break
                    
        neg_q = not is_primary
        return [h1, h2, neg_q]
        
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R1 and R2 are commutative rings with identity",
    "H_2: R = R1 x R2 is the direct product of R1 and R2",
    "¬Q: The ideal Q1 x R2 is not a primary ideal in R"
]

N_HYP = 2
NEG_Q_INDEX = 2