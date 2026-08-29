import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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
    h1_ok = False
    h2_ok = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 9:
            R, R_add, R_mul, R_zero, R_one, M, M_add, M_zero, action = witness
        else:
            def get(name):
                if isinstance(witness, dict):
                    return witness[name]
                return getattr(witness, name)
            R = get('R')
            R_add = get('R_add')
            R_mul = get('R_mul')
            R_zero = get('R_zero')
            R_one = get('R_one')
            M = get('M')
            M_add = get('M_add')
            M_zero = get('M_zero')
            action = get('action')
            
        R = list(R)
        M = list(M)
        if len(R) > 100 or len(M) > 100:
            return [False, False, False]
            
        # H1: M is a finitely generated module over R
        h1_ok = True
        if R_zero not in R or R_one not in R or M_zero not in M:
            h1_ok = False
            
        if h1_ok:
            for a in R:
                if R_add(a, R_zero) != a or R_add(R_zero, a) != a: h1_ok = False
                if R_mul(a, R_one) != a or R_mul(R_one, a) != a: h1_ok = False
                inv_exists = False
                for b in R:
                    if R_add(a, b) == R_zero and R_add(b, a) == R_zero:
                        inv_exists = True
                        break
                if not inv_exists: h1_ok = False
                for b in R:
                    if R_add(a, b) not in R: h1_ok = False
                    if R_mul(a, b) not in R: h1_ok = False
                    if R_add(a, b) != R_add(b, a): h1_ok = False
                    if R_mul(a, b) != R_mul(b, a): h1_ok = False
                    for c in R:
                        if R_add(R_add(a, b), c) != R_add(a, R_add(b, c)): h1_ok = False
                        if R_mul(R_mul(a, b), c) != R_mul(a, R_mul(b, c)): h1_ok = False
                        if R_mul(a, R_add(b, c)) != R_add(R_mul(a, b), R_mul(a, c)): h1_ok = False
                        if not h1_ok: break
                    if not h1_ok: break
                if not h1_ok: break
                
        if h1_ok:
            for m in M:
                if M_add(m, M_zero) != m or M_add(M_zero, m) != m: h1_ok = False
                if action(R_one, m) != m: h1_ok = False
                if action(R_zero, m) != M_zero: h1_ok = False
                inv_exists = False
                for n in M:
                    if M_add(m, n) == M_zero and M_add(n, m) == M_zero:
                        inv_exists = True
                        break
                if not inv_exists: h1_ok = False
                for n in M:
                    if M_add(m, n) not in M: h1_ok = False
                    if M_add(m, n) != M_add(n, m): h1_ok = False
                    for p in M:
                        if M_add(M_add(m, n), p) != M_add(m, M_add(n, p)): h1_ok = False
                        if not h1_ok: break
                    if not h1_ok: break
                if not h1_ok: break
                
        if h1_ok:
            for r in R:
                for m in M:
                    if action(r, m) not in M: h1_ok = False
                    for n in M:
                        if action(r, M_add(m, n)) != M_add(action(r, m), action(r, n)): h1_ok = False
                        if not h1_ok: break
                    if not h1_ok: break
                if not h1_ok: break
                for s in R:
                    for m in M:
                        if action(R_add(r, s), m) != M_add(action(r, m), action(s, m)): h1_ok = False
                        if action(R_mul(r, s), m) != action(r, action(s, m)): h1_ok = False
                        if not h1_ok: break
                    if not h1_ok: break
                if not h1_ok: break
    except Exception:
        h1_ok = False

    try:
        # H2: M is a torsion module
        if h1_ok:
            h2_ok = True
            for m in M:
                is_tor = False
                for r in R:
                    if r != R_zero and action(r, m) == M_zero:
                        is_tor = True
                        break
                if not is_tor:
                    h2_ok = False
                    break
    except Exception:
        h2_ok = False

    try:
        # neg_Q: The annihilator ideal Ann_R(M) is zero
        if h1_ok:
            neg_q = True
            for r in R:
                if r != R_zero:
                    annihilates = True
                    for m in M:
                        if action(r, m) != M_zero:
                            annihilates = False
                            break
                    if annihilates:
                        neg_q = False
                        break
    except Exception:
        neg_q = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: M is a finitely generated module over R",
    "H_2: M is a torsion module",
    "¬Q: The annihilator ideal Ann_R(M) is zero"
]

N_HYP = 2
NEG_Q_INDEX = 2