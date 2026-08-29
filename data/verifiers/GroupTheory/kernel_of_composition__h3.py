import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

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
        G, H, K, f, g = witness
    except Exception:
        return [False, False, False]
    
    def eval_f(x):
        return f[x] if isinstance(f, dict) else f(x)
        
    def eval_g(x):
        return g[x] if isinstance(g, dict) else g(x)

    # H1: G, H, and K are groups
    try:
        h1 = (hasattr(G, 'elements') and hasattr(G, 'identity') and
              hasattr(H, 'elements') and hasattr(H, 'identity') and
              hasattr(K, 'elements') and hasattr(K, 'identity'))
    except Exception:
        h1 = False

    # H2: f is a group homomorphism from G to H
    try:
        if h1:
            G_elems = set(G.elements)
            H_elems = set(H.elements)
            
            valid_f = True
            for x in G_elems:
                if eval_f(x) not in H_elems:
                    valid_f = False
                    break
            
            if valid_f:
                h2 = all(eval_f(x * y) == eval_f(x) * eval_f(y) for x in G_elems for y in G_elems)
            else:
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The kernel of f is not a subgroup of the kernel of g \circ f
    try:
        if h1:
            K_elems = set(K.elements)
            
            valid_g = True
            for x in G.elements:
                try:
                    if eval_g(eval_f(x)) not in K_elems:
                        valid_g = False
                        break
                except Exception:
                    valid_g = False
                    break
            
            if valid_g:
                ker_f = {x for x in G.elements if eval_f(x) == H.identity}
                ker_gf = {x for x in G.elements if eval_g(eval_f(x)) == K.identity}
                
                is_subset = ker_f.issubset(ker_gf)
                
                is_ker_gf_subgroup = (
                    G.identity in ker_gf and
                    all(x * y in ker_gf for x in ker_gf for y in ker_gf) and
                    all(x**-1 in ker_gf for x in ker_gf)
                )
                
                neg_q = not (is_subset and is_ker_gf_subgroup)
            else:
                neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G, H, and K are groups",
    "H_2: f is a group homomorphism from G to H",
    "¬Q: The kernel of f is not a subgroup of the kernel of g \circ f"
]

N_HYP = 2
NEG_Q_INDEX = 2