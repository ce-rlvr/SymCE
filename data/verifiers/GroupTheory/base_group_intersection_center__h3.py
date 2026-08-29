import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import itertools
import functools
import math

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

def get_elements(G):
    if hasattr(G, 'elements'):
        return list(G.elements)
    elif hasattr(G, 'generate'):
        return list(G.generate())
    if isinstance(G, (list, tuple, set)):
        return list(G)
    return list(G)

def get_identity(G):
    if hasattr(G, 'identity'):
        return G.identity
    els = get_elements(G)
    for e in els:
        if all(e * x == x and x * e == x for x in els):
            return e
    return None

def is_group(G):
    try:
        els = get_elements(G)
        if not els: return False
        # check closure
        for a in els:
            for b in els:
                if a * b not in els:
                    return False
        # check identity
        id_e = get_identity(G)
        if id_e is None: return False
        # check inverses
        for a in els:
            has_inv = False
            for b in els:
                if a * b == id_e and b * a == id_e:
                    has_inv = True
                    break
            if not has_inv: return False
        # check associativity
        for a in els:
            for b in els:
                ab = a * b
                for c in els:
                    if ab * c != a * (b * c):
                        return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        if len(witness) == 4:
            N, H, phi, G_op = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: N and H are groups
    try:
        h1_ok = is_group(N) and is_group(H)
    except Exception:
        h1_ok = False

    # H2: phi is a homomorphism H -> Aut(N)
    try:
        N_els = get_elements(N)
        H_els = get_elements(H)
        
        h2_ok = True
        for h in H_els:
            phi_h = phi(h) if callable(phi) else phi[h]
            mapped = []
            for n in N_els:
                pn = phi_h(n) if callable(phi_h) else phi_h[n]
                if pn not in mapped:
                    mapped.append(pn)
            if len(mapped) != len(N_els):
                h2_ok = False
                break
            # check homomorphism
            for n1 in N_els:
                pn1 = phi_h(n1) if callable(phi_h) else phi_h[n1]
                for n2 in N_els:
                    pn2 = phi_h(n2) if callable(phi_h) else phi_h[n2]
                    pn12 = phi_h(n1 * n2) if callable(phi_h) else phi_h[n1 * n2]
                    if pn12 != pn1 * pn2:
                        h2_ok = False
                        break
                if not h2_ok: break
            if not h2_ok: break
            
        if h2_ok:
            for h1 in H_els:
                for h2 in H_els:
                    phi_h1 = phi(h1) if callable(phi) else phi[h1]
                    phi_h2 = phi(h2) if callable(phi) else phi[h2]
                    phi_h12 = phi(h1 * h2) if callable(phi) else phi[h1 * h2]
                    for n in N_els:
                        pn = phi_h2(n) if callable(phi_h2) else phi_h2[n]
                        p12n = phi_h1(pn) if callable(phi_h1) else phi_h1[pn]
                        ph12n = phi_h12(n) if callable(phi_h12) else phi_h12[n]
                        if p12n != ph12n:
                            h2_ok = False
                            break
                    if not h2_ok: break
                if not h2_ok: break
    except Exception:
        h2_ok = False

    # Conclusion: LHS == RHS
    try:
        id_H = get_identity(H)
        LHS = []
        for n in N_els:
            is_in_ZG = True
            x = (n, id_H)
            for m in N_els:
                for k in H_els:
                    y = (m, k)
                    xy = G_op(x, y) if callable(G_op) else G_op[(x, y)]
                    yx = G_op(y, x) if callable(G_op) else G_op[(y, x)]
                    if xy != yx:
                        is_in_ZG = False
                        break
                if not is_in_ZG:
                    break
            if is_in_ZG:
                if n not in LHS:
                    LHS.append(n)
                
        RHS = []
        for n in N_els:
            in_ZN = True
            for m in N_els:
                if n * m != m * n:
                    in_ZN = False
                    break
            if not in_ZN:
                continue
            fixed = True
            for h in H_els:
                phi_h = phi(h) if callable(phi) else phi[h]
                pn = phi_h(n) if callable(phi_h) else phi_h[n]
                if pn != n:
                    fixed = False
                    break
            if fixed:
                if n not in RHS:
                    RHS.append(n)
                
        neg_q = False
        if len(LHS) != len(RHS):
            neg_q = True
        else:
            for n in LHS:
                if n not in RHS:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: N and H are groups",
    "H_2: phi: H -> Aut(N) is a group homomorphism",
    "¬Q: Z(G) intersection (N x {1_H}) is not equal to {(n, 1_H) | n in Z(N) and phi_h(n)=n for all h}"
]
N_HYP = 2
NEG_Q_INDEX = 2