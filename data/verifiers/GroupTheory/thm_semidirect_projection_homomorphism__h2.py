import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    def find_id(els):
        for e in els:
            if all(e * x == x and x * e == x for x in els):
                return e
        return None

    def is_group(els):
        if not els: return False
        for a in els:
            for b in els:
                if a * b not in els: return False
        id_e = find_id(els)
        if id_e is None: return False
        for a in els:
            if not any(a * b == id_e and b * a == id_e for b in els):
                return False
        return True

    try:
        N = witness['N']
        H = witness['H']
        N_els = list(N.generate()) if hasattr(N, 'generate') else list(N)
        H_els = list(H.generate()) if hasattr(H, 'generate') else list(H)
    except Exception:
        return [False, False]

    try:
        phi = witness['phi']
        
        if not is_group(N_els) or not is_group(H_els):
            h1_ok = False
        else:
            id_N = find_id(N_els)
            id_H = find_id(H_els)
            
            h1_ok = True
            for h in H_els:
                phi_h = phi(h) if callable(phi) else phi[h]
                for n1 in N_els:
                    pn1 = phi_h(n1) if callable(phi_h) else phi_h.get(n1)
                    if pn1 not in N_els:
                        h1_ok = False; break
                    for n2 in N_els:
                        pn2 = phi_h(n2) if callable(phi_h) else phi_h.get(n2)
                        pn12 = phi_h(n1 * n2) if callable(phi_h) else phi_h.get(n1 * n2)
                        if pn12 != pn1 * pn2:
                            h1_ok = False; break
                    if not h1_ok: break
                if not h1_ok: break
                
            if h1_ok:
                for h1 in H_els:
                    phi_h1 = phi(h1) if callable(phi) else phi[h1]
                    for h2 in H_els:
                        phi_h2 = phi(h2) if callable(phi) else phi[h2]
                        phi_h12 = phi(h1 * h2) if callable(phi) else phi[h1 * h2]
                        for n in N_els:
                            pn = phi_h2(n) if callable(phi_h2) else phi_h2.get(n)
                            p12n = phi_h12(n) if callable(phi_h12) else phi_h12.get(n)
                            p1_p2n = phi_h1(pn) if callable(phi_h1) else phi_h1.get(pn)
                            if p12n != p1_p2n:
                                h1_ok = False; break
                        if not h1_ok: break
                    if not h1_ok: break
            
            if h1_ok:
                phi_idH = phi(id_H) if callable(phi) else phi[id_H]
                for n in N_els:
                    pn = phi_idH(n) if callable(phi_idH) else phi_idH.get(n)
                    if pn != n:
                        h1_ok = False; break
    except Exception:
        h1_ok = False

    try:
        id_N = find_id(N_els)
        id_H = find_id(H_els)
        if id_N is None or id_H is None:
            neg_q_ok = False
        else:
            phi = witness['phi']
            pi = witness['pi']
            pi_func = pi if callable(pi) else (lambda g: pi[g])
            
            codomain = witness.get('codomain', None)
            if codomain is not None:
                codomain_els = list(codomain.generate()) if hasattr(codomain, 'generate') else list(codomain)
            
            is_hom = True
            try:
                for n1 in N_els:
                    for h1 in H_els:
                        for n2 in N_els:
                            for h2 in H_els:
                                g1 = (n1, h1)
                                g2 = (n2, h2)
                                
                                phi_h1 = phi(h1) if callable(phi) else phi[h1]
                                pn2 = phi_h1(n2) if callable(phi_h1) else phi_h1.get(n2)
                                
                                g12 = (n1 * pn2, h1 * h2)
                                
                                if pi_func(g1) * pi_func(g2) != pi_func(g12):
                                    is_hom = False
                                    break
                            if not is_hom: break
                        if not is_hom: break
                    if not is_hom: break
            except Exception:
                is_hom = False
                
            if codomain is not None:
                try:
                    image = []
                    for n in N_els:
                        for h in H_els:
                            val = pi_func((n, h))
                            if val not in image:
                                image.append(val)
                    
                    is_surj = True
                    if len(image) != len(codomain_els):
                        is_surj = False
                    else:
                        for val in image:
                            if val not in codomain_els:
                                is_surj = False
                                break
                except Exception:
                    is_surj = False
            else:
                is_surj = True
                
            try:
                id_K = pi_func((id_N, id_H))
                kernel = []
                for n in N_els:
                    for h in H_els:
                        if pi_func((n, h)) == id_K:
                            kernel.append((n, h))
                            
                expected_kernel = [(n, id_H) for n in N_els]
                
                is_kernel_correct = True
                if len(kernel) != len(expected_kernel):
                    is_kernel_correct = False
                else:
                    for k in kernel:
                        if k not in expected_kernel:
                            is_kernel_correct = False
                            break
            except Exception:
                is_kernel_correct = False
                
            conclusion = is_hom and is_surj and is_kernel_correct
            neg_q_ok = not conclusion
            
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is the external semidirect product of N by H with respect to an action φ",
    "¬Q: π is not a surjective group homomorphism, or its kernel is not N × {1_H}"
]

N_HYP = 1
NEG_Q_INDEX = 1