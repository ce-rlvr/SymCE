import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

# Standard algebra objects
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

CONDITION_LABELS = [
    "H_1: N and H are groups and phi: H -> Aut(N) is a homomorphism",
    "H_2: G = N ⋊_phi H is the external semidirect product",
    "H_3: f: N -> K and g: H -> K are group homomorphisms",
    "H_4: f(N) is normalized by g(H) in K",
    "H_5: f(phi_h(n)) = g(h) f(n) g(h)^-1 for all n in N and h in H",
    "¬Q: There does NOT exist a unique group homomorphism Phi: G -> K such that Phi((n, 1_H)) = f(n) and Phi((1_N, h)) = g(h)"
]

N_HYP = 5
NEG_Q_INDEX = 5

def conditions(witness) -> list[bool]:
    # H1: N and H are groups and phi: H -> Aut(N) is a homomorphism
    try:
        h1_ok = True
        for h1 in witness.H:
            for h2 in witness.H:
                for n in witness.N:
                    if witness.phi(witness.mul_H(h1, h2), n) != witness.phi(h1, witness.phi(h2, n)):
                        h1_ok = False
                        break
            for n1 in witness.N:
                for n2 in witness.N:
                    if witness.phi(h1, witness.mul_N(n1, n2)) != witness.mul_N(witness.phi(h1, n1), witness.phi(h1, n2)):
                        h1_ok = False
                        break
            if not h1_ok:
                break
        for n in witness.N:
            if witness.phi(witness.id_H, n) != n:
                h1_ok = False
                break
    except Exception:
        h1_ok = False

    # H2: G = N ⋊_phi H is the external semidirect product
    try:
        h2_ok = True
        for n1 in witness.N:
            for h1 in witness.H:
                for n2 in witness.N:
                    for h2 in witness.H:
                        expected_n = witness.mul_N(n1, witness.phi(h1, n2))
                        expected_h = witness.mul_H(h1, h2)
                        if witness.mul_G((n1, h1), (n2, h2)) != (expected_n, expected_h):
                            h2_ok = False
                            break
                    if not h2_ok: break
                if not h2_ok: break
            if not h2_ok: break
    except Exception:
        h2_ok = False

    # H3: f: N -> K and g: H -> K are group homomorphisms
    try:
        h3_ok = True
        for n1 in witness.N:
            for n2 in witness.N:
                if witness.f(witness.mul_N(n1, n2)) != witness.mul_K(witness.f(n1), witness.f(n2)):
                    h3_ok = False
                    break
            if not h3_ok: break
        for h1 in witness.H:
            for h2 in witness.H:
                if witness.g(witness.mul_H(h1, h2)) != witness.mul_K(witness.g(h1), witness.g(h2)):
                    h3_ok = False
                    break
            if not h3_ok: break
    except Exception:
        h3_ok = False

    # H4: f(N) is normalized by g(H) in K
    try:
        h4_ok = True
        f_N = [witness.f(n) for n in witness.N]
        for h in witness.H:
            gh = witness.g(h)
            gh_inv = witness.inv_K(gh)
            for fn in f_N:
                conj = witness.mul_K(witness.mul_K(gh, fn), gh_inv)
                if conj not in f_N:
                    h4_ok = False
                    break
            if not h4_ok: break
    except Exception:
        h4_ok = False

    # H5: f(phi_h(n)) = g(h) f(n) g(h)^-1 for all n in N and h in H
    try:
        h5_ok = True
        for n in witness.N:
            for h in witness.H:
                lhs = witness.f(witness.phi(h, n))
                gh = witness.g(h)
                gh_inv = witness.inv_K(gh)
                rhs = witness.mul_K(witness.mul_K(gh, witness.f(n)), gh_inv)
                if lhs != rhs:
                    h5_ok = False
                    break
            if not h5_ok: break
    except Exception:
        h5_ok = False

    # ¬Q: There does NOT exist a unique group homomorphism Phi: G -> K such that Phi((n, 1_H)) = f(n) and Phi((1_N, h)) = g(h)
    try:
        q_ok = True
        for n1 in witness.N:
            for h1 in witness.H:
                for n2 in witness.N:
                    for h2 in witness.H:
                        n_prod = witness.mul_N(n1, witness.phi(h1, n2))
                        h_prod = witness.mul_H(h1, h2)
                        
                        phi_left = witness.mul_K(witness.f(n_prod), witness.g(h_prod))
                        
                        phi_1 = witness.mul_K(witness.f(n1), witness.g(h1))
                        phi_2 = witness.mul_K(witness.f(n2), witness.g(h2))
                        phi_right = witness.mul_K(phi_1, phi_2)
                        
                        if phi_left != phi_right:
                            q_ok = False
                            break
                    if not q_ok: break
                if not q_ok: break
            if not q_ok: break
        neg_q = not q_ok
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, h4_ok, h5_ok, neg_q]