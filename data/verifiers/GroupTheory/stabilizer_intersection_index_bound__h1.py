import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_idx(G, H):
    if hasattr(G, 'order') and hasattr(H, 'order'):
        h_order = H.order()
        if h_order == 0:
            return float('inf')
        return G.order() / h_order
    if hasattr(G, 'index') and callable(G.index):
        try:
            return G.index(H)
        except Exception:
            pass
    if hasattr(G, '__len__') and hasattr(H, '__len__'):
        h_len = len(H)
        if h_len == 0:
            return float('inf')
        return len(G) / h_len
    raise ValueError("Cannot compute index")

def conditions(witness):
    try:
        if isinstance(witness, dict):
            x = witness.get('x')
            y = witness.get('y')
            X = witness.get('X')
            G = witness.get('G')
            
            if X is None:
                if hasattr(G, 'degree'):
                    X = list(range(G.degree))
                elif hasattr(G, '__len__'):
                    X = G
                    
            h1 = False
            if X is not None:
                h1 = (x in X) and (y in X)
                
            if 'idx_x' in witness and 'idx_y' in witness and 'idx_xy' in witness:
                idx_x = witness['idx_x']
                idx_y = witness['idx_y']
                idx_xy = witness['idx_xy']
            else:
                G_x = witness.get('G_x')
                G_y = witness.get('G_y')
                
                if G_x is None and hasattr(G, 'stabilizer'):
                    G_x = G.stabilizer(x)
                    G_y = G.stabilizer(y)
                    
                idx_x = get_idx(G, G_x)
                idx_y = get_idx(G, G_y)
                
                G_xy = witness.get('G_xy')
                if G_xy is None:
                    if hasattr(G_x, 'intersect'):
                        G_xy = G_x.intersect(G_y)
                    elif hasattr(G_x, 'intersection'):
                        G_xy = G_x.intersection(G_y)
                    elif isinstance(G_x, list):
                        G_xy = [g for g in G_x if g in G_y]
                    else:
                        G_xy = set(G_x).intersection(set(G_y))
                        
                idx_xy = get_idx(G, G_xy)
                
            h2 = (idx_x < float('inf')) and (idx_y < float('inf'))
            
            q = (idx_xy < float('inf')) and (idx_xy <= idx_x * idx_y)
            neg_q = not q
            
            return [bool(h1), bool(h2), bool(neg_q)]
            
        elif isinstance(witness, tuple):
            if len(witness) == 4:
                G, X, x, y = witness
            elif len(witness) == 3:
                G, x, y = witness
                if hasattr(G, 'degree'):
                    X = list(range(G.degree))
                else:
                    X = G
            else:
                return [False, False, False]
                
            h1 = False
            if X is not None:
                h1 = (x in X) and (y in X)
            
            if hasattr(G, 'stabilizer'):
                G_x = G.stabilizer(x)
                G_y = G.stabilizer(y)
            else:
                G_x = [g for g in G if g(x) == x]
                G_y = [g for g in G if g(y) == y]
                
            idx_x = get_idx(G, G_x)
            idx_y = get_idx(G, G_y)
            
            h2 = (idx_x < float('inf')) and (idx_y < float('inf'))
            
            if hasattr(G_x, 'intersect'):
                G_xy = G_x.intersect(G_y)
            elif hasattr(G_x, 'intersection'):
                G_xy = G_x.intersection(G_y)
            elif isinstance(G_x, list):
                G_xy = [g for g in G_x if g in G_y]
            else:
                G_xy = set(G_x).intersection(set(G_y))
                
            idx_xy = get_idx(G, G_xy)
            
            q = (idx_xy < float('inf')) and (idx_xy <= idx_x * idx_y)
            neg_q = not q
            
            return [bool(h1), bool(h2), bool(neg_q)]
            
        else:
            return [False, False, False]
            
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: x and y are elements of X",
    "H_2: The point stabilizers G_x and G_y have finite index in G",
    "¬Q: The index of G_x cap G_y in G is infinite or strictly greater than the product of indices"
]

N_HYP = 2
NEG_Q_INDEX = 2