import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
import itertools
import functools
import math

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

CONDITION_LABELS = [
    "H_1: H is a finite subgroup of G",
    "H_2: x is an element of G",
    "¬Q: The cardinality of the left coset xH is not equal to the cardinality of H"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            if 'G' not in witness or 'H' not in witness or 'x' not in witness:
                return [False, False, False]
            G = witness['G']
            H = witness['H']
            x = witness['x']
            if 'op' in witness:
                op = witness['op']
            elif hasattr(G, 'op'):
                op = G.op
            else:
                op = lambda a, b: a * b
        elif hasattr(witness, 'G') and hasattr(witness, 'H') and hasattr(witness, 'x'):
            G = witness.G
            H = witness.H
            x = witness.x
            if hasattr(witness, 'op'):
                op = witness.op
            elif hasattr(G, 'op'):
                op = G.op
            else:
                op = lambda a, b: a * b
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 4:
                G, H, x, op = witness
            elif len(witness) == 3:
                G, H, x = witness
                if hasattr(G, 'op'):
                    op = G.op
                else:
                    op = lambda a, b: a * b
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        H_list = list(H)
        unique_H = []
        for h in H_list:
            if h not in unique_H:
                unique_H.append(h)
    except Exception:
        return [False, False, False]

    # H_1: H is a finite subgroup of G
    try:
        h1 = True
        if not unique_H:
            h1 = False
        
        if h1:
            for h in unique_H:
                if h not in G:
                    h1 = False
                    break
                    
        if h1:
            for a in unique_H:
                for b in unique_H:
                    if op(a, b) not in unique_H:
                        h1 = False
                        break
                if not h1: break
                
        if h1:
            for a in unique_H:
                for b in unique_H:
                    for c in unique_H:
                        if op(a, op(b, c)) != op(op(a, b), c):
                            h1 = False
                            break
                    if not h1: break
                if not h1: break
                
        if h1:
            identity = None
            for e in unique_H:
                is_id = True
                for h in unique_H:
                    if op(e, h) != h or op(h, e) != h:
                        is_id = False
                        break
                if is_id:
                    identity = e
                    break
            if identity is None:
                h1 = False
                
        if h1:
            for h in unique_H:
                has_inv = False
                for inv in unique_H:
                    if op(h, inv) == identity and op(inv, h) == identity:
                        has_inv = True
                        break
                if not has_inv:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H_2: x is an element of G
    try:
        h2 = x in G
    except Exception:
        h2 = False

    # ¬Q: The cardinality of the left coset xH is not equal to the cardinality of H
    try:
        xH = []
        for h in unique_H:
            xh = op(x, h)
            if xh not in xH:
                xH.append(xh)
        neg_q = len(xH) != len(unique_H)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]