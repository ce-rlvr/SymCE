import sympy
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.combinatorics.permutations import *
from sympy.matrices import *
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *
import z3
import math
import itertools
import functools

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
    h1, h2, neg_q = False, False, False
    try:
        if callable(witness):
            witness = witness()
            
        if isinstance(witness, dict):
            h1 = bool(witness.get('H1', witness.get('G_is_finite_group_of_automorphisms', False)))
            h2 = bool(witness.get('H2', witness.get('K_is_fixed_field', False)))
            if 'Q' in witness:
                q = bool(witness['Q'])
            else:
                is_galois = witness.get('is_finite_Galois_extension', True)
                degree = witness.get('L_K_degree', 0)
                g_order = witness.get('G_order', 0)
                q = is_galois and (degree == g_order)
            neg_q = not q
            return [h1, h2, neg_q]
            
        if hasattr(witness, 'H1'):
            h1 = bool(witness.H1)
            h2 = bool(witness.H2)
            q = bool(witness.Q)
            neg_q = not q
            return [h1, h2, neg_q]
            
        if hasattr(witness, 'G_is_finite_group_of_automorphisms'):
            h1 = bool(witness.G_is_finite_group_of_automorphisms)
            h2 = bool(witness.K_is_fixed_field)
            if hasattr(witness, 'Q'):
                q = bool(witness.Q)
            else:
                is_galois = bool(getattr(witness, 'is_finite_Galois_extension', True))
                degree = getattr(witness, 'L_K_degree', 0)
                g_order = getattr(witness, 'G_order', 0)
                q = is_galois and (degree == g_order)
            neg_q = not q
            return [h1, h2, neg_q]
            
        if isinstance(witness, tuple) and len(witness) == 3:
            if all(isinstance(x, bool) for x in witness):
                return [witness[0], witness[1], not witness[2]]
                
    except Exception:
        pass
        
    return [False, False, False]

CONDITION_LABELS = [
    "H_1: G is a finite group of automorphisms of L",
    "H_2: K is the fixed field of G in L",
    "¬Q: L/K is not a finite Galois extension with degree equal to the order of G"
]

N_HYP = 2
NEG_Q_INDEX = 2