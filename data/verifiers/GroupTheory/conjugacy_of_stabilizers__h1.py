import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        G = witness['G']
        X = witness['X']
        action = witness['action']
        x = witness['x']
        y = witness['y']
        g = witness['g']
        
        G_elements = list(G)
        
        def apply_action(h, pt):
            if callable(action):
                return action(h, pt)
            else:
                return action[(h, pt)]
                
        # H1: x and y are elements of X in the same orbit
        # We compute the orbit as the connected component in the action graph
        equiv_class = set([x])
        queue = [x]
        while queue:
            curr = queue.pop(0)
            # Forward reachability
            for h in G_elements:
                try:
                    nxt = apply_action(h, curr)
                    if nxt in X and nxt not in equiv_class:
                        equiv_class.add(nxt)
                        queue.append(nxt)
                except Exception:
                    pass
            # Backward reachability
            for v in X:
                if v not in equiv_class:
                    for h in G_elements:
                        try:
                            if apply_action(h, v) == curr:
                                equiv_class.add(v)
                                queue.append(v)
                                break
                        except Exception:
                            pass
                            
        h1_ok = (x in X) and (y in X) and (y in equiv_class)
        
        # H2: There exists g \in G such that y = g \cdot x
        # The witness provides the specific g to be used in the conclusion
        h2_ok = (g in G_elements) and (apply_action(g, x) == y)
        
        # Conclusion: Stab_G(y) = g Stab_G(x) g^{-1}
        stab_x = set()
        stab_y = set()
        for h in G_elements:
            if apply_action(h, x) == x:
                stab_x.add(h)
            if apply_action(h, y) == y:
                stab_y.add(h)
                
        if 'mul' in witness and 'inv' in witness:
            mul = witness['mul']
            inv = witness['inv']
            g_stab_x_g_inv = {mul(mul(g, h), inv(g)) for h in stab_x}
        else:
            g_stab_x_g_inv = {g * h * (g**-1) for h in stab_x}
            
        neg_q_ok = (stab_y != g_stab_x_g_inv)
        
        return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: x and y are elements of X in the same orbit",
    "H_2: There exists g in G such that y = g * x",
    "¬Q: Stab_G(y) != g Stab_G(x) g^{-1}"
]

N_HYP = 2
NEG_Q_INDEX = 2