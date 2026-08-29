import sympy
from sympy import Matrix, eye, zeros
import itertools
import functools
import math

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = list(witness['R'])
            S = list(witness['S'])
            phi = witness['phi']
            s = witness['s']
            add_R = witness.get('add_R', lambda a, b: a + b)
            mul_R = witness.get('mul_R', lambda a, b: a * b)
            add_S = witness.get('add_S', lambda a, b: a + b)
            mul_S = witness.get('mul_S', lambda a, b: a * b)
            zero_R = witness.get('zero_R', None)
            one_R = witness.get('one_R', None)
            zero_S = witness.get('zero_S', None)
            one_S = witness.get('one_S', None)
            eq_R = witness.get('eq_R', lambda a, b: a == b)
            eq_S = witness.get('eq_S', lambda a, b: a == b)
        else:
            R, S, phi, s = witness
            R = list(R)
            S = list(S)
            add_R = lambda a, b: a + b
            mul_R = lambda a, b: a * b
            add_S = lambda a, b: a + b
            mul_S = lambda a, b: a * b
            zero_R = None
            one_R = None
            zero_S = None
            one_S = None
            eq_R = lambda a, b: a == b
            eq_S = lambda a, b: a == b
    except Exception:
        return [False, False, False]

    try:
        if len(R) > 500 or len(S) > 500:
            h1 = False
        else:
            zR = zero_R
            if zR is None:
                for x in R:
                    if all(eq_R(add_R(x, y), y) and eq_R(add_R(y, x), y) for y in R):
                        zR = x
                        break
            oR = one_R
            if oR is None:
                for x in R:
                    if all(eq_R(mul_R(x, y), y) and eq_R(mul_R(y, x), y) for y in R):
                        oR = x
                        break
            zS = zero_S
            if zS is None:
                for x in S:
                    if all(eq_S(add_S(x, y), y) and eq_S(add_S(y, x), y) for y in S):
                        zS = x
                        break
            oS = one_S
            if oS is None:
                for x in S:
                    if all(eq_S(mul_S(x, y), y) and eq_S(mul_S(y, x), y) for y in S):
                        oS = x
                        break

            R_is_ring = (zR is not None) and (oR is not None)
            if R_is_ring:
                for a in R:
                    if not eq_R(add_R(a, zR), a): R_is_ring = False
                    if not eq_R(add_R(zR, a), a): R_is_ring = False
                    if not eq_R(mul_R(a, oR), a): R_is_ring = False
                    if not eq_R(mul_R(oR, a), a): R_is_ring = False
                    has_inv = False
                    for b in R:
                        if eq_R(add_R(a, b), zR) and eq_R(add_R(b, a), zR):
                            has_inv = True
                            break
                    if not has_inv: R_is_ring = False

            S_is_ring = (zS is not None) and (oS is not None)
            if S_is_ring:
                for a in S:
                    if not eq_S(add_S(a, zS), a): S_is_ring = False
                    if not eq_S(add_S(zS, a), a): S_is_ring = False
                    if not eq_S(mul_S(a, oS), a): S_is_ring = False
                    if not eq_S(mul_S(oS, a), a): S_is_ring = False
                    has_inv = False
                    for b in S:
                        if eq_S(add_S(a, b), zS) and eq_S(add_S(b, a), zS):
                            has_inv = True
                            break
                    if not has_inv: S_is_ring = False

            if isinstance(phi, dict):
                phi_func = lambda x: phi[x]
            else:
                phi_func = phi

            phi_is_hom = True
            for a in R:
                for b in R:
                    if not eq_S(phi_func(add_R(a, b)), add_S(phi_func(a), phi_func(b))):
                        phi_is_hom = False
                    if not eq_S(phi_func(mul_R(a, b)), mul_S(phi_func(a), phi_func(b))):
                        phi_is_hom = False
            if not eq_S(phi_func(oR), oS):
                phi_is_hom = False

            h1 = R_is_ring and S_is_ring and phi_is_hom
    except Exception:
        h1 = False

    try:
        h2 = any(eq_S(s, x) for x in S)
    except Exception:
        h2 = False

    try:
        if isinstance(phi, dict):
            phi_func = lambda x: phi[x]
        else:
            phi_func = phi
            
        neg_q = False
        for r in R:
            pr = phi_func(r)
            if not eq_S(mul_S(s, pr), mul_S(pr, s)):
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: phi is a ring homomorphism from R to S",
    "H_2: s is an element of S",
    "¬Q: There does not exist a unique ring homomorphism Phi from the polynomial ring over R to S such that Phi(r) = phi(r) and Phi(x) = s"
]

N_HYP = 2
NEG_Q_INDEX = 2