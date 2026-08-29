import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def check_group(G):
    try:
        if hasattr(G, 'elements'):
            elems = list(G.elements)
        elif isinstance(G, (list, tuple, set)):
            elems = list(G)
        else:
            return False, [], None
            
        if not elems: return False, [], None
        
        identity = None
        for e in elems:
            is_id = True
            for a in elems:
                if e * a != a or a * e != a:
                    is_id = False
                    break
            if is_id:
                identity = e
                break
        if identity is None: return False, [], None
        
        for a in elems:
            has_inv = False
            for b in elems:
                prod = a * b
                if prod not in elems: return False, [], None
                if prod == identity and b * a == identity:
                    has_inv = True
            if not has_inv: return False, [], None
            
        return True, elems, identity
    except Exception:
        return False, [], None

def get_val(d, key):
    if isinstance(d, dict):
        try:
            if key in d:
                return d[key]
        except TypeError:
            pass
        for k, v in d.items():
            if k == key: return v
        raise KeyError
    elif callable(d):
        return d(key)
    else:
        for k, v in d:
            if k == key: return v
        raise KeyError

def conditions(witness):
    try:
        N, H, phi, K, f, g = witness
    except Exception:
        return [False]*5 + [False]

    # H1: N and H are groups, phi is hom to Aut(N)
    h1 = False
    try:
        is_N_group, N_elems, N_id = check_group(N)
        is_H_group, H_elems, H_id = check_group(H)
        if is_N_group and is_H_group:
            h1 = True
            for h in H_elems:
                try:
                    mapping = get_val(phi, h)
                except KeyError:
                    h1 = False; break
                
                mapped_values = []
                for n in N_elems:
                    try:
                        val = get_val(mapping, n)
                        if val not in mapped_values:
                            mapped_values.append(val)
                    except KeyError:
                        h1 = False; break
                if not h1: break
                
                if len(mapped_values) != len(N_elems):
                    h1 = False; break
                for n in N_elems:
                    if n not in mapped_values:
                        h1 = False; break
                if not h1: break
                
                # check automorphism
                for n1 in N_elems:
                    for n2 in N_elems:
                        if get_val(mapping, n1 * n2) != get_val(mapping, n1) * get_val(mapping, n2):
                            h1 = False; break
                    if not h1: break
                if not h1: break
            
            # check homomorphism
            if h1:
                for h1_el in H_elems:
                    for h2_el in H_elems:
                        for n in N_elems:
                            map12 = get_val(phi, h1_el * h2_el)
                            map1 = get_val(phi, h1_el)
                            map2 = get_val(phi, h2_el)
                            if get_val(map12, n) != get_val(map1, get_val(map2, n)):
                                h1 = False; break
                        if not h1: break
                    if not h1: break
    except Exception:
        h1 = False

    # H2: G is semidirect product
    h2 = h1

    # H3: K is a group
    h3 = False
    try:
        is_K_group, K_elems, K_id = check_group(K)
        if is_K_group:
            h3 = True
            K_inv_list = []
            for a in K_elems:
                for b in K_elems:
                    if a * b == K_id and b * a == K_id:
                        K_inv_list.append((a, b))
                        break
            def get_inv(x):
                for a, b in K_inv_list:
                    if a == x: return b
                return None
    except Exception:
        h3 = False

    # H4: f(N) normalized by g(H)
    h4 = False
    try:
        if h1 and h3:
            h4 = True
            for n in N_elems:
                try:
                    fn = get_val(f, n)
                    if fn not in K_elems:
                        h4 = False; break
                except Exception:
                    h4 = False; break
            if h4:
                for h in H_elems:
                    try:
                        gh = get_val(g, h)
                        if gh not in K_elems:
                            h4 = False; break
                    except Exception:
                        h4 = False; break
            
            if h4:
                f_N = []
                for n in N_elems:
                    fn = get_val(f, n)
                    if fn not in f_N:
                        f_N.append(fn)
                g_H = []
                for h in H_elems:
                    gh = get_val(g, h)
                    if gh not in g_H:
                        g_H.append(gh)
                
                for x in f_N:
                    for y in g_H:
                        conj = y * x * get_inv(y)
                        if conj not in f_N:
                            h4 = False; break
                    if not h4: break
    except Exception:
        h4 = False

    # H5: f(phi_h(n)) = g(h) f(n) g(h)^-1
    h5 = False
    try:
        if h1 and h3 and h4:
            h5 = True
            for n in N_elems:
                for h in H_elems:
                    map_h = get_val(phi, h)
                    phi_h_n = get_val(map_h, n)
                    f_phi = get_val(f, phi_h_n)
                    gh = get_val(g, h)
                    fn = get_val(f, n)
                    if f_phi != gh * fn * get_inv(gh):
                        h5 = False; break
                if not h5: break
    except Exception:
        h5 = False

    # neg_Q: candidate is NOT a homomorphism
    neg_q = False
    try:
        if h1 and h3 and h4:
            is_hom = True
            for n1 in N_elems:
                for h1_el in H_elems:
                    for n2 in N_elems:
                        for h2_el in H_elems:
                            map_h1 = get_val(phi, h1_el)
                            phi_h1_n2 = get_val(map_h1, n2)
                            n_prod = n1 * phi_h1_n2
                            h_prod = h1_el * h2_el
                            
                            lhs = get_val(f, n_prod) * get_val(g, h_prod)
                            rhs = get_val(f, n1) * get_val(g, h1_el) * get_val(f, n2) * get_val(g, h2_el)
                            if lhs != rhs:
                                is_hom = False
                                break
                        if not is_hom: break
                    if not is_hom: break
                if not is_hom: break
            neg_q = not is_hom
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: N and H are groups and phi: H -> Aut(N) is a homomorphism",
    "H_2: G = N \\rtimes_\\phi H is the external semidirect product",
    "H_3: K is a group",
    "H_4: f(N) is normalized by g(H) in K",
    "H_5: f(phi_h(n)) = g(h) f(n) g(h)^{-1} for all n in N and h in H",
    "¬Q: There does not exist a unique group homomorphism Phi: G -> K satisfying the conditions"
]

N_HYP = 5
NEG_Q_INDEX = 5