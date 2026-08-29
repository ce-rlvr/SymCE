import sympy
from sympy.combinatorics import *
from sympy.matrices import *
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

def conditions(witness):
    try:
        R = witness.get('R', [])
        S = witness.get('S', [])
        add_R = witness['add_R']
        mul_R = witness['mul_R']
        add_S = witness['add_S']
        mul_S = witness['mul_S']
        zero_R = witness['zero_R']
        one_R = witness['one_R']
        zero_S = witness['zero_S']
        one_S = witness['one_S']
        phi = witness['phi']
        f = witness['f']
        c = witness['c']
    except Exception:
        return [False] * 5

    def apply_phi(a):
        return phi[a] if isinstance(phi, dict) else phi(a)

    def divides_R(a, b):
        if 'divides_R' in witness: return witness['divides_R'](a, b)
        return any(mul_R(a, q) == b for q in R)

    def divides_S(a, b):
        if 'divides_S' in witness: return witness['divides_S'](a, b)
        return any(mul_S(a, q) == b for q in S)

    def is_gcd_R(d, coeffs):
        if 'is_gcd_R' in witness: return witness['is_gcd_R'](d, coeffs)
        for coef in coeffs:
            if not divides_R(d, coef): return False
        for e in R:
            if all(divides_R(e, coef) for coef in coeffs):
                if not divides_R(e, d): return False
        return True

    def is_gcd_S(d, coeffs):
        if 'is_gcd_S' in witness: return witness['is_gcd_S'](d, coeffs)
        for coef in coeffs:
            if not divides_S(d, coef): return False
        for e in S:
            if all(divides_S(e, coef) for coef in coeffs):
                if not divides_S(e, d): return False
        return True

    def is_unit_S(u):
        if 'is_unit_S' in witness: return witness['is_unit_S'](u)
        return any(mul_S(u, v) == one_S and mul_S(v, u) == one_S for v in S)

    def are_associates_S(a, b):
        if 'are_associates_S' in witness: return witness['are_associates_S'](a, b)
        for u in S:
            if is_unit_S(u):
                if mul_S(u, b) == a or mul_S(b, u) == a:
                    return True
        return False

    try:
        if 'is_isomorphism' in witness:
            h1 = bool(witness['is_isomorphism'])
        else:
            h1 = True
            if len(R) != len(S): h1 = False
            else:
                mapped_R = [apply_phi(a) for a in R]
                for s in S:
                    if s not in mapped_R: h1 = False
                for a in R:
                    for b in R:
                        pa = apply_phi(a)
                        pb = apply_phi(b)
                        if apply_phi(add_R(a, b)) != add_S(pa, pb): h1 = False
                        if apply_phi(mul_R(a, b)) != mul_S(pa, pb): h1 = False
                if apply_phi(one_R) != one_S: h1 = False
                if apply_phi(zero_R) != zero_S: h1 = False
    except Exception:
        h1 = False

    try:
        if 'Phi_f' in witness:
            Phi_f = witness['Phi_f']
            h2 = True
            if len(Phi_f) != len(f): h2 = False
            else:
                for a, b in zip(f, Phi_f):
                    if apply_phi(a) != b: h2 = False
        else:
            Phi_f = [apply_phi(a) for a in f]
            h2 = True
    except Exception:
        h2 = False

    try:
        h3 = any(a != zero_R for a in f)
    except Exception:
        h3 = False

    try:
        h4 = is_gcd_R(c, f)
    except Exception:
        h4 = False

    try:
        if 'content_Phi_f' in witness:
            content_S = witness['content_Phi_f']
            is_content = is_gcd_S(content_S, Phi_f)
            if not is_content:
                neg_q = False
            else:
                neg_q = not are_associates_S(content_S, apply_phi(c))
        else:
            contents_S = [d for d in S if is_gcd_S(d, Phi_f)]
            if not contents_S:
                neg_q = False
            else:
                neg_q = not are_associates_S(contents_S[0], apply_phi(c))
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: phi is a ring isomorphism from R to S",
    "H_2: Phi is the polynomial ring isomorphism induced by phi",
    "H_3: f is a non-zero polynomial over R",
    "H_4: c is the content of f in R",
    "not Q: The content of Phi(f) over S is not associate to phi(c) in S"
]

N_HYP = 4
NEG_Q_INDEX = 4