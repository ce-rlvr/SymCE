import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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
    def get(attr):
        if isinstance(witness, dict):
            return witness[attr]
        return getattr(witness, attr)

    try:
        N = list(get('N'))
        H = list(get('H'))
        K = list(get('K'))
        mul_N = get('mul_N')
        mul_H = get('mul_H')
        mul_K = get('mul_K')
        id_N = get('id_N')
        id_H = get('id_H')
        id_K = get('id_K')
        f = get('f')
        g = get('g')
        phi_raw = get('phi')
    except Exception:
        return [False, False, False]

    try:
        try:
            _ = phi_raw(id_H, id_N)
            phi = phi_raw
        except Exception:
            _ = phi_raw(id_H)(id_N)
            phi = lambda h, n: phi_raw(h)(n)
    except Exception:
        return [False, False, False]

    try:
        inv_K = get('inv_K')
        _ = inv_K(id_K)
    except Exception:
        def inv_K(k):
            for x in K:
                if mul_K(k, x) == id_K and mul_K(x, k) == id_K:
                    return x
            raise ValueError("No inverse")

    h1_ok = True
    try:
        # Check N is a group
        for n in N:
            if mul_N(n, id_N) != n or mul_N(id_N, n) != n:
                h1_ok = False
        for n1 in N:
            for n2 in N:
                for n3 in N:
                    if mul_N(mul_N(n1, n2), n3) != mul_N(n1, mul_N(n2, n3)):
                        h1_ok = False
        for n in N:
            has_inv = False
            for n_inv in N:
                if mul_N(n, n_inv) == id_N and mul_N(n_inv, n) == id_N:
                    has_inv = True
                    break
            if not has_inv:
                h1_ok = False

        # Check H is a group
        for h in H:
            if mul_H(h, id_H) != h or mul_H(id_H, h) != h:
                h1_ok = False
        for h1 in H:
            for h2 in H:
                for h3 in H:
                    if mul_H(mul_H(h1, h2), h3) != mul_H(h1, mul_H(h2, h3)):
                        h1_ok = False
        for h in H:
            has_inv = False
            for h_inv in H:
                if mul_H(h, h_inv) == id_H and mul_H(h_inv, h) == id_H:
                    has_inv = True
                    break
            if not has_inv:
                h1_ok = False

        # Check phi is an action
        for n in N:
            if phi(id_H, n) != n:
                h1_ok = False
        for h1 in H:
            for h2 in H:
                for n in N:
                    if phi(mul_H(h1, h2), n) != phi(h1, phi(h2, n)):
                        h1_ok = False
        for h in H:
            for n1 in N:
                for n2 in N:
                    if phi(h, mul_N(n1, n2)) != mul_N(phi(h, n1), phi(h, n2)):
                        h1_ok = False
            if phi(h, id_N) != id_N:
                h1_ok = False
    except Exception:
        h1_ok = False

    h2_ok = True
    try:
        # Check K is a group
        for k in K:
            if mul_K(k, id_K) != k or mul_K(id_K, k) != k:
                h2_ok = False
            if mul_K(k, inv_K(k)) != id_K or mul_K(inv_K(k), k) != id_K:
                h2_ok = False
        for k1 in K:
            for k2 in K:
                for k3 in K:
                    if mul_K(mul_K(k1, k2), k3) != mul_K(k1, mul_K(k2, k3)):
                        h2_ok = False
        
        # Check f is hom
        for n1 in N:
            for n2 in N:
                if f(mul_N(n1, n2)) != mul_K(f(n1), f(n2)):
                    h2_ok = False
        
        # Check g is hom
        for h1 in H:
            for h2 in H:
                if g(mul_H(h1, h2)) != mul_K(g(h1), g(h2)):
                    h2_ok = False
    except Exception:
        h2_ok = False

    neg_q = False
    try:
        # RHS: f(phi_h(n)) == g(h) f(n) g(h)^-1
        rhs = True
        for n in N:
            for h in H:
                left = f(phi(h, n))
                right = mul_K(g(h), mul_K(f(n), inv_K(g(h))))
                if left != right:
                    rhs = False
                    break
            if not rhs:
                break
        
        # LHS: exists unique Phi
        lhs = True
        for n1 in N:
            for h1 in H:
                for n2 in N:
                    for h2 in H:
                        n_res = mul_N(n1, phi(h1, n2))
                        h_res = mul_H(h1, h2)
                        phi_res = mul_K(f(n_res), g(h_res))
                        
                        phi_1 = mul_K(f(n1), g(h1))
                        phi_2 = mul_K(f(n2), g(h2))
                        if phi_res != mul_K(phi_1, phi_2):
                            lhs = False
                            break
                    if not lhs: break
                if not lhs: break
            if not lhs: break
        
        neg_q = (lhs != rhs)
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G is an external semidirect product of N and H with respect to phi",
    "H_2: f: N -> K and g: H -> K are group homomorphisms",
    "¬Q: The conclusion fails (LHS iff RHS is false)"
]

N_HYP = 2
NEG_Q_INDEX = 2