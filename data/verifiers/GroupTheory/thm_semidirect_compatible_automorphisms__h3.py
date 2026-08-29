import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
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
        N = witness['N']
        H = witness['H']
        phi = witness['phi']
        alpha = witness['alpha']
        beta = witness['beta']
    except Exception:
        return [False, False, False, False, False]

    def get_elements(G):
        if hasattr(G, 'generate'):
            return list(G.generate())
        elif hasattr(G, 'elements'):
            return list(G.elements)
        else:
            return list(G)

    def is_bijection(f, G):
        try:
            elements = get_elements(G)
            images = []
            for g in elements:
                img = f(g)
                if img not in elements:
                    return False
                images.append(img)
            for i in range(len(images)):
                for j in range(i + 1, len(images)):
                    if images[i] == images[j]:
                        return False
            return True
        except Exception:
            return False

    def is_homomorphism(f, G):
        try:
            elements = get_elements(G)
            for g1 in elements:
                for g2 in elements:
                    if f(g1 * g2) != f(g1) * f(g2):
                        return False
            return True
        except Exception:
            return False

    def is_automorphism(f, G):
        return is_bijection(f, G) and is_homomorphism(f, G)

    # H1: N and H are groups
    try:
        N_elems = get_elements(N)
        H_elems = get_elements(H)
        def is_group(elems):
            if not elems: return False
            for a in elems:
                for b in elems:
                    if a * b not in elems:
                        return False
            identities = [e for e in elems if all(e * a == a and a * e == a for a in elems)]
            if not identities:
                return False
            e = identities[0]
            for a in elems:
                if not any(a * b == e and b * a == e for b in elems):
                    return False
            return True
        h1_ok = is_group(N_elems) and is_group(H_elems)
    except Exception:
        h1_ok = False

    # H2: phi is a valid action of H on N (homomorphism H -> Aut(N))
    try:
        h2_ok = True
        for h in H_elems:
            phi_h = phi(h)
            if not is_automorphism(phi_h, N):
                h2_ok = False
                break
        if h2_ok:
            for h1 in H_elems:
                for h2 in H_elems:
                    phi_h1 = phi(h1)
                    phi_h2 = phi(h2)
                    phi_h1_h2 = phi(h1 * h2)
                    for n in N_elems:
                        if phi_h1_h2(n) != phi_h1(phi_h2(n)):
                            h2_ok = False
                            break
                    if not h2_ok: break
                if not h2_ok: break
    except Exception:
        h2_ok = False

    # H3: alpha is an automorphism of N
    try:
        h3_ok = is_automorphism(alpha, N)
    except Exception:
        h3_ok = False

    # H4: beta is an automorphism of H
    try:
        h4_ok = is_automorphism(beta, H)
    except Exception:
        h4_ok = False

    # neg_Q: gamma is not a group automorphism of G
    try:
        neg_q = False
        for h in H_elems:
            for n in N_elems:
                if alpha(phi(h)(n)) != phi(beta(h))(alpha(n)):
                    neg_q = True
                    break
            if neg_q: break
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, h4_ok, neg_q]

CONDITION_LABELS = [
    "H_1: N and H are groups",
    "H_2: phi is a valid action of H on N (homomorphism H -> Aut(N))",
    "H_3: alpha is an automorphism of N",
    "H_4: beta is an automorphism of H",
    "¬Q: gamma is not a group automorphism of G"
]

N_HYP = 4
NEG_Q_INDEX = 4