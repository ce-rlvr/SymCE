import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
import itertools

# Top-level setup
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

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            X = witness.get('X')
            Y = witness.get('Y')
            action_X = witness.get('action_X')
        else:
            G, X, Y, action_X = witness
            
        h1 = isinstance(Y, (set, list, tuple))
        h2 = isinstance(X, (set, list, tuple))
        
        if not (h1 and h2):
            return [h1, h2, False]
            
        X_list = list(X)
        Y_list = list(Y)
        
        if hasattr(G, 'elements'):
            elements = list(G.elements)
        elif hasattr(G, 'generate'):
            elements = list(G.generate())
        else:
            elements = list(G)
            
        def inv(g):
            return ~g if hasattr(g, '__invert__') else g**-1
            
        def mul(g, h):
            return g * h
            
        e = None
        if hasattr(G, 'identity'):
            e = G.identity
        else:
            for cand in elements:
                try:
                    if all(mul(cand, g) == g and mul(g, cand) == g for g in elements):
                        e = cand
                        break
                except Exception:
                    pass
                    
        is_valid_action = True
        
        if e is None:
            is_valid_action = False
            
        all_f = list(itertools.product(Y_list, repeat=len(X_list)))
        
        def apply_f(f, x):
            if x not in X_list:
                raise ValueError("x not in X")
            idx = X_list.index(x)
            return f[idx]
            
        if is_valid_action:
            try:
                e_inv = inv(e)
            except Exception:
                is_valid_action = False
                
            if is_valid_action:
                for f in all_f:
                    for x in X_list:
                        try:
                            act_val = action_X(e_inv, x)
                            if apply_f(f, act_val) != apply_f(f, x):
                                is_valid_action = False
                                break
                        except Exception:
                            is_valid_action = False
                            break
                    if not is_valid_action:
                        break
                        
        if is_valid_action:
            for g in elements:
                try:
                    g_inv = inv(g)
                except Exception:
                    is_valid_action = False
                    break
                for h in elements:
                    try:
                        h_inv = inv(h)
                        gh = mul(g, h)
                        gh_inv = inv(gh)
                    except Exception:
                        is_valid_action = False
                        break
                        
                    for f in all_f:
                        for x in X_list:
                            try:
                                lhs_x = action_X(h_inv, action_X(g_inv, x))
                                rhs_x = action_X(gh_inv, x)
                                lhs_val = apply_f(f, lhs_x)
                                rhs_val = apply_f(f, rhs_x)
                                if lhs_val != rhs_val:
                                    is_valid_action = False
                                    break
                            except Exception:
                                is_valid_action = False
                                break
                        if not is_valid_action:
                            break
                    if not is_valid_action:
                        break
                if not is_valid_action:
                    break
                    
        neg_q = not is_valid_action
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: Y is a set",
    "H_2: Y^X is the set of all functions from X to Y",
    "¬Q: The induced operation is not a valid group action of G on Y^X"
]

N_HYP = 2
NEG_Q_INDEX = 2