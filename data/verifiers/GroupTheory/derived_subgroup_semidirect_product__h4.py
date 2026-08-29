import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup, AbelianGroup
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
V4 = AbelianGroup(2, 2)
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
    "H_1: N and H are groups",
    "H_2: phi is a group homomorphism from H to Aut(N)",
    "H_3: G is the external semidirect product of N and H",
    "¬Q: Derived subgroup of G is not equal to the semidirect product"
]

N_HYP = 3
NEG_Q_INDEX = 3

def get_elems(G):
    if hasattr(G, 'generate'):
        elems = list(G.generate())
    elif hasattr(G, 'elements'):
        elems = list(G.elements)
    else:
        elems = list(G)
    
    unique_elems = []
    for e in elems:
        if e not in unique_elems:
            unique_elems.append(e)
    return unique_elems

def is_group(elems):
    if not elems: return False, None
    id_elem = None
    for e in elems:
        is_id = True
        for x in elems:
            if e * x != x or x * e != x:
                is_id = False
                break
        if is_id:
            id_elem = e
            break
    if id_elem is None: return False, None
    
    for a in elems:
        has_inv = False
        for b in elems:
            if a * b == id_elem and b * a == id_elem:
                has_inv = True
                break
        if not has_inv: return False, None
        
        for b in elems:
            if a * b not in elems: return False, None
    return True, id_elem

def conditions(witness):
    try:
        if len(witness) == 3:
            N, H, phi = witness
        elif len(witness) == 4:
            N, H, phi, _ = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
        
    try:
        N_elems = get_elems(N)
        H_elems = get_elems(H)
    except Exception:
        return [False, False, False, False]
        
    # H1: N and H are groups
    try:
        N_is_group, id_N = is_group(N_elems)
        H_is_group, id_H = is_group(H_elems)
        h1_ok = bool(N_is_group and H_is_group)
    except Exception:
        h1_ok = False
        id_N = None
        id_H = None

    # H2: phi is a homomorphism H -> Aut(N)
    try:
        if not h1_ok:
            h2_ok = False
        else:
            h2_ok = True
            for h in H_elems:
                img = []
                for n in N_elems:
                    pn = phi(h, n)
                    if pn not in N_elems:
                        h2_ok = False; break
                    img.append(pn)
                if not h2_ok: break
                
                unique_img = []
                for x in img:
                    if x not in unique_img:
                        unique_img.append(x)
                if len(unique_img) != len(N_elems):
                    h2_ok = False; break
                    
                for n1 in N_elems:
                    for n2 in N_elems:
                        if phi(h, n1 * n2) != phi(h, n1) * phi(h, n2):
                            h2_ok = False; break
                    if not h2_ok: break
                if not h2_ok: break
                
            if h2_ok:
                for h1 in H_elems:
                    for h2 in H_elems:
                        for n in N_elems:
                            if phi(h1 * h2, n) != phi(h1, phi(h2, n)):
                                h2_ok = False; break
                        if not h2_ok: break
                    if not h2_ok: break
            if h2_ok:
                for n in N_elems:
                    if phi(id_H, n) != n:
                        h2_ok = False; break
    except Exception:
        h2_ok = False

    # H3: G is the external semidirect product
    h3_ok = bool(h1_ok and h2_ok)

    # Conclusion: G' == (N'[N,H]) \rtimes H'
    try:
        if not (h1_ok and h2_ok):
            neg_q = False
        else:
            def inv_N(n):
                for x in N_elems:
                    if n * x == id_N and x * n == id_N: return x
                return None
                
            def inv_H(h):
                for x in H_elems:
                    if h * x == id_H and x * h == id_H: return x
                return None
                
            def mul_G(x, y):
                return (x[0] * phi(x[1], y[0]), x[1] * y[1])
                
            def inv_G(x):
                h_inv = inv_H(x[1])
                n_inv = inv_N(x[0])
                return (phi(h_inv, n_inv), h_inv)
                
            G_elems = [(n, h) for n in N_elems for h in H_elems]
            
            G_commutators = []
            for x in G_elems:
                for y in G_elems:
                    x_inv = inv_G(x)
                    y_inv = inv_G(y)
                    comm = mul_G(mul_G(x_inv, y_inv), mul_G(x, y))
                    if comm not in G_commutators:
                        G_commutators.append(comm)
                    
            def get_closure(gens, mul_func, identity):
                closure = [identity]
                active_gens = []
                for g in gens:
                    if g not in closure:
                        active_gens.append(g)
                        queue = list(closure)
                        while queue:
                            curr = queue.pop(0)
                            for ag in active_gens:
                                nxt = mul_func(curr, ag)
                                if nxt not in closure:
                                    closure.append(nxt)
                                    queue.append(nxt)
                return closure
                
            G_prime = get_closure(G_commutators, mul_G, (id_N, id_H))
            
            N_commutators = []
            for n1 in N_elems:
                for n2 in N_elems:
                    n1_inv = inv_N(n1)
                    n2_inv = inv_N(n2)
                    comm = n1_inv * n2_inv * n1 * n2
                    if comm not in N_commutators:
                        N_commutators.append(comm)
                    
            NH_commutators = []
            for n in N_elems:
                for h in H_elems:
                    n_inv = inv_N(n)
                    comm = n_inv * phi(h, n)
                    if comm not in NH_commutators:
                        NH_commutators.append(comm)
                    
            K_gens = []
            for x in N_commutators + NH_commutators:
                if x not in K_gens:
                    K_gens.append(x)
                    
            K = get_closure(K_gens, lambda a, b: a * b, id_N)
            
            H_commutators = []
            for h1 in H_elems:
                for h2 in H_elems:
                    h1_inv = inv_H(h1)
                    h2_inv = inv_H(h2)
                    comm = h1_inv * h2_inv * h1 * h2
                    if comm not in H_commutators:
                        H_commutators.append(comm)
                        
            H_prime = get_closure(H_commutators, lambda a, b: a * b, id_H)
            
            S = []
            for k in K:
                for hp in H_prime:
                    S.append((k, hp))
            
            if len(G_prime) != len(S):
                neg_q = True
            else:
                neg_q = False
                for x in G_prime:
                    if x not in S:
                        neg_q = True
                        break
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, neg_q]