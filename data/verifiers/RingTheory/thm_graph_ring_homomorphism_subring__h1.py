import sympy
from sympy import *
import math
import itertools
import functools

# Top-level setup
# The witness is expected to be a tuple (n, m, f_map) representing a map f: Z/nZ -> Z/mZ.
# n and m are integers >= 2 (moduli of the rings R and S).
# f_map can be a list, dict, callable, or list of pairs defining the mapping.

def conditions(witness):
    try:
        if len(witness) == 3:
            n, m, f_map = witness
        elif len(witness) == 2:
            n, f_map = witness
            m = n
        else:
            return [False, False, False]
            
        n = int(n)
        m = int(m)
        if n < 2 or m < 2:
            return [False, False, False]
            
        if callable(f_map):
            f = {x: int(f_map(x)) % m for x in range(n)}
        elif isinstance(f_map, dict):
            f = {x: int(f_map[x]) % m for x in range(n)}
        elif isinstance(f_map, (list, tuple)) and len(f_map) > 0 and isinstance(f_map[0], (list, tuple)):
            f_dict = dict(f_map)
            f = {x: int(f_dict[x]) % m for x in range(n)}
        else:
            f = {x: int(f_map[x]) % m for x in range(n)}
            
        # H1: f is a ring homomorphism (preserves addition and multiplication)
        # Note: We do not enforce f(1) == 1 here, as non-unital homomorphisms 
        # are the key to the counterexample.
        h1 = True
        for x in range(n):
            for y in range(n):
                if f[(x + y) % n] != (f[x] + f[y]) % m:
                    h1 = False
                    break
                if f[(x * y) % n] != (f[x] * f[y]) % m:
                    h1 = False
                    break
            if not h1:
                break
                
        # H2: G is the graph of f
        # By definition of the witness format, G is constructed as the graph of f.
        h2 = True
        
        # neg_Q: G is not a subring of R x S
        # A subring must contain the multiplicative identity of the parent ring.
        # The identity of Z/nZ x Z/mZ is (1, 1).
        # G = {(x, f(x)) | x in Z/nZ} contains (1, 1) iff f(1) == 1.
        # Thus, G is not a subring iff f(1) != 1.
        neg_q = (f[1] != 1)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: f: R -> S is a ring homomorphism",
    "H_2: G is the graph of f",
    "¬Q: G is not a subring of R x S"
]

N_HYP = 2
NEG_Q_INDEX = 2