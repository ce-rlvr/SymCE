import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, H, p = witness
        else:
            G = witness.G
            H = witness.H
            p = witness.p
    except Exception:
        return [False, False, False]
        
    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False
        
    try:
        h2 = False
        if hasattr(witness, 'is_subgroup'):
            val = witness.is_subgroup
            h2 = bool(val() if callable(val) else val)
        elif hasattr(H, 'is_subgroup'):
            val = H.is_subgroup
            if callable(val):
                try:
                    h2 = bool(val(G))
                except Exception:
                    h2 = bool(val())
            else:
                h2 = bool(val)
        elif hasattr(G, 'has_subgroup'):
            val = G.has_subgroup
            h2 = bool(val(H) if callable(val) else val)
        else:
            try:
                h2 = bool(H <= G)
            except Exception:
                pass
    except Exception:
        h2 = False
        
    try:
        contains_sylow = None
        if hasattr(witness, 'contains_sylow'):
            val = witness.contains_sylow
            contains_sylow = bool(val() if callable(val) else val)
        elif hasattr(H, 'contains_sylow'):
            val = H.contains_sylow
            if callable(val):
                try:
                    contains_sylow = bool(val(G, p))
                except Exception:
                    contains_sylow = bool(val())
            else:
                contains_sylow = bool(val)
                
        index = None
        if hasattr(witness, 'index'):
            val = witness.index
            index = val() if callable(val) else val
        elif hasattr(H, 'index'):
            val = H.index
            if callable(val):
                try:
                    index = val(G)
                except Exception:
                    index = val()
            else:
                index = val
        elif hasattr(G, 'index'):
            val = G.index
            if callable(val):
                try:
                    index = val(H)
                except Exception:
                    index = val()
            else:
                index = val
                
        if index is None:
            try:
                oG = G.order() if callable(G.order) else G.order
                oH = H.order() if callable(H.order) else H.order
                if oG != sympy.oo and oH != sympy.oo:
                    index = oG // oH
            except Exception:
                pass

        if contains_sylow is None or index is None:
            neg_q = False
        else:
            if index == sympy.oo or index == float('inf'):
                divisible = False
            else:
                divisible = (int(index) % int(p) == 0)
            
            q = (contains_sylow == (not divisible))
            neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = ["H_1: p is a prime number", "H_2: H is a subgroup of G", "¬Q: The equivalence fails"]

N_HYP = 2
NEG_Q_INDEX = 2