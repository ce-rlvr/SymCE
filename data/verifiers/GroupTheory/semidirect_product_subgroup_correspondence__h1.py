import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def get_N(w):
    if isinstance(w, dict): return w['N']
    return w.N

def get_H(w):
    if isinstance(w, dict): return w['H']
    return w.H

def get_G(w):
    if isinstance(w, dict): return w['G']
    return w.G

def get_N_tilde(w):
    if isinstance(w, dict): return w['N_tilde']
    return w.N_tilde

def phi(w, h, n):
    if isinstance(w, dict): return w['phi'](h, n)
    return w.phi(h, n)

def mul_N(w, n1, n2):
    if isinstance(w, dict): return w['mul_N'](n1, n2)
    return w.mul_N(n1, n2)

def mul_H(w, h1, h2):
    if isinstance(w, dict): return w['mul_H'](h1, h2)
    return w.mul_H(h1, h2)

def mul_G(w, g1, g2):
    if isinstance(w, dict): return w['mul_G'](g1, g2)
    return w.mul_G(g1, g2)

def f(w, n, h):
    if isinstance(w, dict):
        if 'f' in w: return w['f'](n, h)
        return (n, h)
    if hasattr(w, 'f'): return w.f(n, h)
    return (n, h)

def get_subgroups(elements, mul_func):
    def generate_subgroup(generators):
        sg = set(generators)
        added = True
        while added:
            added = False
            new_elements = set()
            for a in sg:
                for b in sg:
                    c = mul_func(a, b)
                    if c not in sg and c not in new_elements:
                        new_elements.add(c)
            if new_elements:
                sg.update(new_elements)
                added = True
        return frozenset(sg)

    subgroups = set()
    for x in elements:
        subgroups.add(generate_subgroup([x]))
    
    added = True
    while added:
        added = False
        new_subgroups = set()
        for sg1 in subgroups:
            for sg2 in subgroups:
                if sg1 != sg2:
                    sg_join = generate_subgroup(sg1 | sg2)
                    if sg_join not in subgroups and sg_join not in new_subgroups:
                        new_subgroups.add(sg_join)
        if new_subgroups:
            subgroups.update(new_subgroups)
            added = True
            
    return subgroups

def conditions(witness) -> list[bool]:
    try:
        N = get_N(witness)
        H = get_H(witness)
        G = get_G(witness)
        N_tilde = get_N_tilde(witness)
    except Exception:
        return [False, False, False, False]

    def find_id(elements, mul_func):
        for e in elements:
            if all(mul_func(e, x) == x and mul_func(x, e) == x for x in elements):
                return e
        return None

    try:
        id_N = find_id(N, lambda x, y: mul_N(witness, x, y))
        id_H = find_id(H, lambda x, y: mul_H(witness, x, y))
        id_G = find_id(G, lambda x, y: mul_G(witness, x, y))
    except Exception:
        return [False, False, False, False]

    if id_N is None or id_H is None or id_G is None:
        return [False, False, False, False]

    h1_ok = True
    try:
        for h in H:
            img = set(phi(witness, h, n) for n in N)
            if len(img) != len(N) or not img.issubset(set(N)):
                h1_ok = False
                break
            for n1 in N:
                for n2 in N:
                    if phi(witness, h, mul_N(witness, n1, n2)) != mul_N(witness, phi(witness, h, n1), phi(witness, h, n2)):
                        h1_ok = False
                        break
                if not h1_ok: break
            if not h1_ok: break
        
        if h1_ok:
            for h1 in H:
                for h2 in H:
                    h12 = mul_H(witness, h1, h2)
                    for n in N:
                        if phi(witness, h12, n) != phi(witness, h1, phi(witness, h2, n)):
                            h1_ok = False
                            break
                    if not h1_ok: break
                if not h1_ok: break
    except Exception:
        h1_ok = False

    h2_ok = True
    try:
        img_f = set()
        for n in N:
            for h in H:
                g = f(witness, n, h)
                if g not in G:
                    h2_ok = False
                    break
                img_f.add(g)
            if not h2_ok: break
        if h2_ok and len(img_f) != len(G):
            h2_ok = False
        
        if h2_ok:
            for n1 in N:
                for h1 in H:
                    g1 = f(witness, n1, h1)
                    for n2 in N:
                        for h2 in H:
                            g2 = f(witness, n2, h2)
                            g12 = mul_G(witness, g1, g2)
                            expected_n = mul_N(witness, n1, phi(witness, h1, n2))
                            expected_h = mul_H(witness, h1, h2)
                            expected_g = f(witness, expected_n, expected_h)
                            if g12 != expected_g:
                                h2_ok = False
                                break
                        if not h2_ok: break
                    if not h2_ok: break
                if not h2_ok: break
    except Exception:
        h2_ok = False

    h3_ok = True
    try:
        expected_N_tilde = set(f(witness, n, id_H) for n in N)
        if set(N_tilde) != expected_N_tilde:
            h3_ok = False
    except Exception:
        h3_ok = False

    neg_q = False
    try:
        actual_N_tilde = set(N_tilde)
        subgroups_H = get_subgroups(H, lambda x, y: mul_H(witness, x, y))
        subgroups_G = get_subgroups(G, lambda x, y: mul_G(witness, x, y))
        subgroups_G_containing_N_tilde = [sg for sg in subgroups_G if actual_N_tilde.issubset(sg)]
        
        mapped_subgroups = set()
        is_bijection = True
        for K in subgroups_H:
            M_K = frozenset(f(witness, n, k) for n in N for k in K)
            if M_K not in subgroups_G_containing_N_tilde:
                is_bijection = False
                break
            mapped_subgroups.add(M_K)
        
        if is_bijection and len(mapped_subgroups) != len(subgroups_G_containing_N_tilde):
            is_bijection = False
            
        preserves_inclusions = True
        if is_bijection:
            for K1 in subgroups_H:
                for K2 in subgroups_H:
                    M_K1 = frozenset(f(witness, n, k) for n in N for k in K1)
                    M_K2 = frozenset(f(witness, n, k) for n in N for k in K2)
                    if K1.issubset(K2) != M_K1.issubset(M_K2):
                        preserves_inclusions = False
                        break
                if not preserves_inclusions: break
                
        if not (is_bijection and preserves_inclusions):
            neg_q = True
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, neg_q]

CONDITION_LABELS = [
    "H_1: phi is a group homomorphism from H to Aut(N)",
    "H_2: G is the external semidirect product of N and H",
    "H_3: N_tilde is the base subgroup in G",
    "¬Q: The map K -> N x K is not a lattice isomorphism"
]

N_HYP = 3
NEG_Q_INDEX = 3