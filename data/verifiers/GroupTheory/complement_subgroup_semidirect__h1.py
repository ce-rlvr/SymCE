import sympy
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
    def get_attr(obj, attr):
        if isinstance(obj, dict):
            return obj[attr]
        return getattr(obj, attr)

    try:
        N = get_attr(witness, 'N')
        op_N = get_attr(witness, 'op_N')
        e_N = get_attr(witness, 'e_N')
        H = get_attr(witness, 'H')
        op_H = get_attr(witness, 'op_H')
        e_H = get_attr(witness, 'e_H')
        phi = get_attr(witness, 'phi')
    except Exception:
        return [False, False, False]

    def check_h1():
        if e_H not in H: return False
        if e_N not in N: return False
        
        # Check H is a group
        for h1 in H:
            for h2 in H:
                if op_H(h1, h2) not in H: return False
        for h1 in H:
            for h2 in H:
                for h3 in H:
                    if op_H(op_H(h1, h2), h3) != op_H(h1, op_H(h2, h3)): return False
        for h in H:
            if op_H(e_H, h) != h or op_H(h, e_H) != h: return False
        for h in H:
            has_inv = False
            for h_inv in H:
                if op_H(h, h_inv) == e_H and op_H(h_inv, h) == e_H:
                    has_inv = True
                    break
            if not has_inv: return False

        # Check phi maps H to Aut(N)
        for h in H:
            mapped = []
            for n in N:
                res = phi(h, n)
                mapped.append(res)
                if res not in N: return False
            
            unique_mapped = []
            for m in mapped:
                if m not in unique_mapped:
                    unique_mapped.append(m)
            if len(unique_mapped) != len(N): return False
            
            for n1 in N:
                for n2 in N:
                    if phi(h, op_N(n1, n2)) != op_N(phi(h, n1), phi(h, n2)): return False
            if phi(h, e_N) != e_N: return False

        # Check phi is a homomorphism
        for h1 in H:
            for h2 in H:
                for n in N:
                    if phi(op_H(h1, h2), n) != phi(h1, phi(h2, n)): return False
        return True

    try:
        h1_ok = check_h1()
    except Exception:
        h1_ok = False

    h2_ok = True
    try:
        G = [(n, h) for n in N for h in H]
        def op_G(g1, g2):
            n1, h1 = g1
            n2, h2 = g2
            return (op_N(n1, phi(h1, n2)), op_H(h1, h2))
        e_G = (e_N, e_H)
    except Exception:
        h2_ok = False

    def check_q():
        if not h2_ok: return False
        
        # Check if G is a group
        for g1 in G:
            for g2 in G:
                if op_G(g1, g2) not in G: return False
        for g1 in G:
            for g2 in G:
                for g3 in G:
                    if op_G(op_G(g1, g2), g3) != op_G(g1, op_G(g2, g3)): return False
        for g in G:
            if op_G(e_G, g) != g or op_G(g, e_G) != g: return False
        for g in G:
            has_inv = False
            for g_inv in G:
                if op_G(g, g_inv) == e_G and op_G(g_inv, g) == e_G:
                    has_inv = True
                    break
            if not has_inv: return False

        H_prime = [(e_N, h) for h in H]
        N_prime = [(n, e_H) for n in N]
        
        # H' is a subgroup
        for x in H_prime:
            for y in H_prime:
                if op_G(x, y) not in H_prime: return False
        for x in H_prime:
            has_inv = False
            for y in H_prime:
                if op_G(x, y) == e_G and op_G(y, x) == e_G:
                    has_inv = True
                    break
            if not has_inv: return False
            
        # H' isomorphic to H via h -> (e_N, h)
        for h1 in H:
            for h2 in H:
                if op_G((e_N, h1), (e_N, h2)) != (e_N, op_H(h1, h2)): return False
                
        # N' is a normal subgroup
        for x in N_prime:
            for y in N_prime:
                if op_G(x, y) not in N_prime: return False
        for x in N_prime:
            has_inv = False
            for y in N_prime:
                if op_G(x, y) == e_G and op_G(y, x) == e_G:
                    has_inv = True
                    break
            if not has_inv: return False
        for g in G:
            g_inv = None
            for x in G:
                if op_G(g, x) == e_G and op_G(x, g) == e_G:
                    g_inv = x
                    break
            if g_inv is None: return False
            for n_p in N_prime:
                if op_G(g, op_G(n_p, g_inv)) not in N_prime: return False
                    
        # N' \cap H' = {e_G}
        intersection = [x for x in N_prime if x in H_prime]
        if len(intersection) != 1 or intersection[0] != e_G: return False
        
        # N' H' = G
        N_prime_H_prime = []
        for n_p in N_prime:
            for h_p in H_prime:
                prod = op_G(n_p, h_p)
                if prod not in N_prime_H_prime:
                    N_prime_H_prime.append(prod)
        if len(N_prime_H_prime) != len(G): return False
        for g in G:
            if g not in N_prime_H_prime: return False
            
        return True

    try:
        q_ok = check_q()
    except Exception:
        q_ok = False

    neg_q = not q_ok

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: phi is a group homomorphism from H to Aut(N)",
    "H_2: G is the external semidirect product of N and H",
    "¬Q: H' is not a subgroup isomorphic to H, or G is not the internal semidirect product of N' and H'"
]

N_HYP = 2
NEG_Q_INDEX = 2