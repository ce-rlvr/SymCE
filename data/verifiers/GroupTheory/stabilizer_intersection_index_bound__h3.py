import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy import eye, zeros
import math

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

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: x and y are elements of X",
    "¬Q: The index of the intersection of stabilizers is not finite or exceeds the product of indices"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            x = witness.get('x')
            y = witness.get('y')
            
            if G == 'Z':
                action = witness.get('action')
                X_sample = list(witness.get('X_sample', [x, y]))
                if not X_sample:
                    X_sample = [x, y]
                if x not in X_sample:
                    X_sample.append(x)
                if y not in X_sample:
                    X_sample.append(y)
                
                # H1: G is a group acting on a set X
                h1 = False
                try:
                    id_ok = all(action(0, p) == p for p in X_sample)
                    comp_ok = True
                    for p in X_sample:
                        for g1 in [-2, -1, 1, 2]:
                            for g2 in [-2, -1, 1, 2]:
                                if action(g1, action(g2, p)) != action(g1 + g2, p):
                                    comp_ok = False
                                    break
                    h1 = id_ok and comp_ok
                except Exception:
                    h1 = False
                    
                # H2: x and y are elements of X
                h2 = (x is not None) and (y is not None)
                
                # Compute indices
                def get_idx(p):
                    for g in range(1, 101):
                        if action(g, p) == p:
                            return g
                    return float('inf')
                
                try:
                    idx_x = get_idx(x)
                    idx_y = get_idx(y)
                    
                    if idx_x == float('inf') or idx_y == float('inf'):
                        idx_int = float('inf')
                    else:
                        idx_int = (idx_x * idx_y) // math.gcd(idx_x, idx_y)
                        
                    if idx_int == float('inf'):
                        neg_q = True
                    else:
                        neg_q = not (idx_int <= idx_x * idx_y)
                except Exception:
                    neg_q = False
                    
                return [h1, h2, neg_q]
                
            elif hasattr(G, 'is_PermutationGroup') and G.is_PermutationGroup:
                h1 = True
                domain = set(range(G.degree))
                h2 = x in domain and y in domain
                
                if not h2:
                    return [h1, False, False]
                    
                try:
                    stab_x = G.stabilizer(x)
                    stab_y = G.stabilizer(y)
                    stab_int = stab_x.intersect(stab_y)
                    
                    idx_x = G.order() // stab_x.order()
                    idx_y = G.order() // stab_y.order()
                    idx_int = G.order() // stab_int.order()
                    
                    conclusion = (idx_int <= idx_x * idx_y)
                    neg_q = not conclusion
                except Exception:
                    neg_q = False
                
                return [h1, h2, neg_q]
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]