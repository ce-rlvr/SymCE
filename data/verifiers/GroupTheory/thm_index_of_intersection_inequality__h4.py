import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

# Top-level setup for standard algebra objects
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

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: K is a subgroup of G",
    "not Q: The index of H intersect K in H is infinite or strictly greater than the index of K in G"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    h1, h2, h3, neg_q = False, False, False, False
    
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False, False, False]
        G, H, K = witness
    except Exception:
        return [False, False, False, False]

    # 1. Integer tuple representing subgroups of Z: G = nZ, H = aZ, K = bZ
    if isinstance(G, int) and isinstance(H, int) and isinstance(K, int):
        n, a, b = G, H, K
        
        try:
            h1 = True
            
            if n == 0:
                h2 = (a == 0)
                h3 = (b == 0)
            else:
                h2 = (a % n == 0)
                h3 = (b % n == 0)
                
            # H intersect K = lcm(a, b)
            if a == 0 and b == 0:
                hk = 0
            else:
                hk = abs(a * b) // math.gcd(a, b)
                
            # index of H intersect K in H = index of hk Z in aZ
            if hk == 0 and a != 0:
                idx_H_HK = float('inf')
            elif a == 0:
                idx_H_HK = 1
            else:
                idx_H_HK = abs(hk) // abs(a)
                
            # index of K in G = index of bZ in nZ
            if b == 0 and n != 0:
                idx_G_K = float('inf')
            elif n == 0:
                idx_G_K = 1
            else:
                idx_G_K = abs(b) // abs(n)
                
            neg_q = (idx_H_HK == float('inf')) or (idx_H_HK > idx_G_K)
            
            return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
        except Exception:
            pass

    # 2. Sympy groups
    try:
        if hasattr(G, 'order') and hasattr(G, 'is_subgroup'):
            h1 = True
            
            if hasattr(H, 'is_subgroup'):
                h2 = H.is_subgroup(G)
            
            if hasattr(K, 'is_subgroup'):
                h3 = K.is_subgroup(G)
                
            if h1 and h2 and h3:
                H_int_K = None
                if hasattr(H, 'intersect'):
                    H_int_K = H.intersect(K)
                elif hasattr(H, 'intersection'):
                    H_int_K = H.intersection(K)
                    
                if H_int_K is not None:
                    oH = H.order()
                    oHK = H_int_K.order()
                    
                    if oHK == 0:
                        idx_H_HK = float('inf')
                    elif oH == sympy.oo:
                        if oHK != sympy.oo:
                            idx_H_HK = float('inf')
                        else:
                            idx_H_HK = 1
                    else:
                        idx_H_HK = oH / oHK
                        
                    oG = G.order()
                    oK = K.order()
                    
                    if oK == 0:
                        idx_G_K = float('inf')
                    elif oG == sympy.oo:
                        if oK != sympy.oo:
                            idx_G_K = float('inf')
                        else:
                            idx_G_K = 1
                    else:
                        idx_G_K = oG / oK
                        
                    neg_q = (idx_H_HK == float('inf') or idx_H_HK == sympy.oo) or (idx_H_HK > idx_G_K)
                    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        pass
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]