import sympy
from sympy.combinatorics import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup
)
try:
    from sympy.combinatorics import FpGroup
except ImportError:
    FpGroup = type("FpGroup", (), {})  # Fallback if not available in the specific sympy version

from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
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
        h1 = False
        h2 = False
        h3 = False
        neg_q = False
        
        # We support two formats for the witness:
        # Format 1: (X, R, H, f) where X is a list of strings, R is a list of relations, H is a group, f is a dict
        # Format 2: (G, H, f) where G is an FpGroup, H is a group, f is a dict or list of images
        
        if isinstance(witness, tuple) and len(witness) == 4:
            X, R, H, f = witness
            
            # H1: G is a group defined by the presentation <X | R>
            try:
                h1 = isinstance(X, (list, tuple)) and all(isinstance(x, str) for x in X)
                h1 = h1 and isinstance(R, (list, tuple))
                if h1:
                    for r in R:
                        h1 = h1 and isinstance(r, (list, tuple))
                        if not h1: break
                        for term in r:
                            h1 = h1 and isinstance(term, (list, tuple)) and len(term) == 2
                            if not h1: break
                            h1 = h1 and term[0] in X and isinstance(term[1], int)
            except Exception:
                h1 = False
                
            # H2: H is a group
            try:
                h2 = isinstance(H, PermutationGroup) or hasattr(H, 'is_group') or hasattr(H, 'elements')
            except Exception:
                h2 = False
                
            # H3: f: X -> H is a mapping
            try:
                h3 = isinstance(f, dict) and set(f.keys()) == set(X)
                if h3 and hasattr(H, '__contains__'):
                    h3 = all(v in H for v in f.values())
            except Exception:
                h3 = False
                
            # neg_Q: The conclusion FAILS (f does not extend to a unique group homomorphism)
            try:
                if h1 and h2 and h3:
                    extends = True
                    if f:
                        id_H = list(f.values())[0] ** 0
                    else:
                        id_H = None
                        
                    for r in R:
                        val = id_H
                        for gen, power in r:
                            val = val * (f[gen] ** power)
                        if val != id_H:
                            extends = False
                            break
                    neg_q = not extends
            except Exception:
                neg_q = False
                
        elif isinstance(witness, tuple) and len(witness) == 3:
            G, H, f = witness
            
            # H1: G is a group defined by the presentation <X | R>
            try:
                h1 = isinstance(G, FpGroup)
            except Exception:
                h1 = False
                
            # H2: H is a group
            try:
                h2 = isinstance(H, PermutationGroup) or hasattr(H, 'is_group') or hasattr(H, 'elements')
            except Exception:
                h2 = False
                
            # H3: f: X -> H is a mapping
            try:
                if isinstance(f, dict):
                    if set(f.keys()) == set(G.generators):
                        f_dict = f
                        h3 = True
                    elif set(f.keys()) == set(G.free_group.generators):
                        f_dict = {G.generators[i]: f[G.free_group.generators[i]] for i in range(len(G.generators))}
                        h3 = True
                    else:
                        h3 = False
                        f_dict = {}
                elif isinstance(f, (list, tuple)):
                    if len(f) == len(G.generators):
                        f_dict = dict(zip(G.generators, f))
                        h3 = True
                    else:
                        h3 = False
                        f_dict = {}
                else:
                    h3 = False
                    f_dict = {}
                    
                if h3 and hasattr(H, '__contains__'):
                    h3 = all(v in H for v in f_dict.values())
            except Exception:
                h3 = False
                f_dict = {}
                
            # neg_Q: The conclusion FAILS (f does not extend to a unique group homomorphism)
            try:
                if h1 and h2 and h3:
                    extends = True
                    if f_dict:
                        id_H = list(f_dict.values())[0] ** 0
                    else:
                        id_H = None
                        
                    F_gens = G.free_group.generators
                    for r in G.relators:
                        val = id_H
                        for gen, power in r.array_form:
                            idx = F_gens.index(gen)
                            g_gen = G.generators[idx]
                            val = val * (f_dict[g_gen] ** power)
                        if val != id_H:
                            extends = False
                            break
                    neg_q = not extends
            except Exception:
                neg_q = False

        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: G is a group defined by the presentation <X | R>",
    "H_2: H is a group",
    "H_3: f: X -> H is a mapping",
    "¬Q: f does not extend to a unique group homomorphism from G to H"
]

N_HYP = 3
NEG_Q_INDEX = 3