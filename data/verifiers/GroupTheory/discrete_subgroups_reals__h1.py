import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import math
import itertools
import functools

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, (set, list, tuple)):
            G_list = list(witness)
        elif hasattr(witness, 'is_FiniteSet') and witness.is_FiniteSet:
            G_list = list(witness)
        else:
            G_list = None
            
        if G_list is not None and 0 < len(G_list) < 100:
            float_G = []
            all_real = True
            for x in G_list:
                try:
                    val = float(x)
                    if not any(abs(val - v) < 1e-9 for v in float_G):
                        float_G.append(val)
                except Exception:
                    all_real = False
                    break
                    
            if all_real:
                # H1: G is a subgroup of R
                is_add = True
                if not any(abs(z) < 1e-9 for z in float_G):
                    is_add = False
                else:
                    for x in float_G:
                        if not any(abs(x + y) < 1e-9 for y in float_G):
                            is_add = False
                        for y in float_G:
                            if not any(abs((x + y) - z) < 1e-9 for z in float_G):
                                is_add = False
                                
                is_mult = True
                if not any(abs(z - 1.0) < 1e-9 for z in float_G):
                    if len(float_G) == 1 and abs(float_G[0]) < 1e-9:
                        pass
                    else:
                        is_mult = False
                else:
                    if len(float_G) > 1 and any(abs(z) < 1e-9 for z in float_G):
                        is_mult = False
                    else:
                        for x in float_G:
                            if not any(abs(x * y - 1.0) < 1e-9 for y in float_G):
                                is_mult = False
                            for y in float_G:
                                if not any(abs((x * y) - z) < 1e-9 for z in float_G):
                                    is_mult = False
                                    
                h1 = is_add or is_mult
                
                # H2: G is a discrete topological space
                h2 = True
                
                # neg_Q: G is neither {0} nor isomorphic to Z
                if len(float_G) == 1:
                    neg_q = False
                else:
                    neg_q = True
                    
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a subgroup of R",
    "H_2: G is a discrete topological space under the subspace topology inherited from R",
    "¬Q: G is neither the trivial group {0} nor isomorphic to the additive group of integers Z"
]

N_HYP = 2
NEG_Q_INDEX = 2