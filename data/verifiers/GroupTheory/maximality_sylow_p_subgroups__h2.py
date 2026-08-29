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

def neg_Q_check(G, P, p):
    try:
        if not sympy.isprime(p):
            return True
        
        is_sub = True
        try:
            for g in P.generators:
                if hasattr(g, 'array_form') and hasattr(G, 'degree'):
                    arr = list(g.array_form)
                    if len(arr) < G.degree:
                        arr.extend(range(len(arr), G.degree))
                        g_pad = Permutation(arr)
                    elif len(arr) > G.degree:
                        if all(arr[i] == i for i in range(G.degree, len(arr))):
                            g_pad = Permutation(arr[:G.degree])
                        else:
                            is_sub = False
                            break
                    else:
                        g_pad = g
                    if g_pad not in G:
                        is_sub = False
                        break
                else:
                    if g not in G:
                        is_sub = False
                        break
        except Exception:
            is_sub = False
            
        if not is_sub:
            return True
            
        p_order = P.order()
        if p_order == 1:
            is_p_group = True
        else:
            factors = sympy.factorint(p_order)
            is_p_group = (list(factors.keys()) == [p])
            
        if not is_p_group:
            return True
            
        g_order = G.order()
        m = 0
        temp = g_order
        while temp % p == 0:
            m += 1
            temp //= p
            
        # P is a maximal p-subgroup iff its order is exactly the highest power of p dividing |G|
        if p_order == p**m:
            return False
        else:
            return True
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness['G']
            P = witness['P']
            p = witness.get('p')
            if p is None:
                try:
                    p_order = P.order()
                    factors = sympy.factorint(p_order)
                    if len(factors) == 1:
                        p = list(factors.keys())[0]
                    else:
                        p = 2
                except Exception:
                    p = 2
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                G, P, p = witness
            elif len(witness) == 2:
                G, P = witness
                try:
                    p_order = P.order()
                    factors = sympy.factorint(p_order)
                    if len(factors) == 1:
                        p = list(factors.keys())[0]
                    else:
                        p = 2
                except Exception:
                    p = 2
            else:
                return [False, False]
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    # H_1: G is a finite group
    try:
        h1 = hasattr(G, 'order') and G.order() > 0 and G.order() != sympy.oo
    except Exception:
        h1 = False
        
    # neg_Q: P is not a maximal p-subgroup of G
    neg_q = neg_Q_check(G, P, p)
    
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: P is not a maximal p-subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1