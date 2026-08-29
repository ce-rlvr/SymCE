import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, DihedralGroup, AlternatingGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    # H_1: Let P be a Sylow 2-subgroup of S_4
    try:
        if not hasattr(witness, 'generators') or not hasattr(witness, 'order'):
            h1 = False
        else:
            order_val = witness.order() if callable(witness.order) else witness.order
            is_sub = True
            for g in witness.generators:
                if hasattr(g, 'size'):
                    # A permutation in S4 can only move elements 0, 1, 2, 3.
                    if any(g(i) != i for i in range(4, g.size)):
                        is_sub = False
                        break
                else:
                    is_sub = False
                    break
            
            # S4 has order 24, so a Sylow 2-subgroup has order 8
            if is_sub and order_val == 8:
                h1 = True
            else:
                h1 = False
    except Exception:
        h1 = False

    # Q: P is isomorphic to the dihedral group of order 8
    try:
        if not hasattr(witness, 'order'):
            q = False
        else:
            order_val = witness.order() if callable(witness.order) else witness.order
            if order_val != 8:
                q = False
            else:
                is_ab = getattr(witness, 'is_abelian', False)
                if callable(is_ab):
                    is_ab = is_ab()
                
                if is_ab:
                    q = False
                else:
                    if hasattr(witness, 'generate'):
                        elements = list(witness.generate())
                    elif hasattr(witness, 'elements'):
                        elements = list(witness.elements)
                    else:
                        elements = []
                        
                    if not elements:
                        q = False
                    else:
                        # D4 is the unique non-abelian group of order 8 with exactly 5 elements of order 2
                        order_2_count = 0
                        for g in elements:
                            g_order = g.order() if callable(g.order) else g.order
                            if g_order == 2:
                                order_2_count += 1
                        
                        if order_2_count == 5:
                            q = True
                        else:
                            q = False
    except Exception:
        q = False

    neg_q = not q

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P is a Sylow 2-subgroup of S_4",
    "¬Q: P is not isomorphic to the dihedral group of order 8"
]

N_HYP = 1
NEG_Q_INDEX = 1