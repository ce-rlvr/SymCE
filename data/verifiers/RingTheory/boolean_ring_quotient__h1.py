import math
from sympy import Integer, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    try:
        # Case 1: witness is a single integer m -> R = Z, I = mZ
        if isinstance(witness, (int, Integer)):
            n = 0
            m = int(witness)
            k = math.gcd(n, m)
            
            # H1: I is an ideal of R (mZ is always an ideal of Z)
            h1 = True
            
            # neg_Q: R/I is NOT a Boolean ring
            # R/I is isomorphic to Z_k
            if k == 0:
                neg_q = True # Z is not Boolean
            elif k == 1:
                neg_q = False # Z_1 is Boolean
            else:
                neg_q = any((x * x) % k != x for x in range(k))
                
            return [h1, neg_q]
            
        # Case 2: witness is a tuple or list
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            
            # Subcase 2a: integers (n, m) -> R = Z_n, I = mZ_n
            if isinstance(witness[0], (int, Integer)) and isinstance(witness[1], (int, Integer)):
                n = int(witness[0])
                m = int(witness[1])
                k = math.gcd(n, m)
                
                # H1: I is an ideal of R (mZ_n is always an ideal of Z_n)
                h1 = True
                
                # neg_Q: R/I is NOT a Boolean ring
                # R/I is isomorphic to Z_k
                if k == 0:
                    neg_q = True
                elif k == 1:
                    neg_q = False
                else:
                    neg_q = any((x * x) % k != x for x in range(k))
                    
                return [h1, neg_q]
                
            # Subcase 2b: SymPy ring and ideal
            R_obj, I_obj = witness
            if hasattr(R_obj, 'gens') and hasattr(I_obj, 'contains'):
                # H1: I is an ideal of R
                h1 = True
                
                # neg_Q: R/I is NOT a Boolean ring
                neg_q = False
                
                # Check if g^2 - g is in I for all generators
                for g in R_obj.gens:
                    if not I_obj.contains(g**2 - g):
                        neg_q = True
                        break
                        
                # Check sum of generators
                if not neg_q and len(R_obj.gens) > 1:
                    g_sum = sum(R_obj.gens)
                    if not I_obj.contains(g_sum**2 - g_sum):
                        neg_q = True
                        
                # Check 2 * g
                if not neg_q and len(R_obj.gens) > 0:
                    g2 = 2 * R_obj.gens[0]
                    if not I_obj.contains(g2**2 - g2):
                        neg_q = True
                        
                return [h1, neg_q]
                
        return [False, False]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "¬Q: R/I is not a Boolean ring"
]

N_HYP = 1
NEG_Q_INDEX = 1