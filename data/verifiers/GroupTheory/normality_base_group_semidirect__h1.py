import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    # H1: phi: H -> Aut(N) is a group homomorphism
    try:
        H = witness.H
        H_op = witness.H_op
        e_H = witness.e_H
        N = witness.N
        N_op = witness.N_op
        phi = witness.phi
        
        h1_ok = True
        
        # Check H is a group
        for h in H:
            if H_op(e_H, h) != h or H_op(h, e_H) != h: 
                h1_ok = False
        for h in H:
            has_inv = False
            for inv in H:
                if H_op(h, inv) == e_H and H_op(inv, h) == e_H:
                    has_inv = True
                    break
            if not has_inv: 
                h1_ok = False
        for h1 in H:
            for h2 in H:
                for h3 in H:
                    if H_op(H_op(h1, h2), h3) != H_op(h1, H_op(h2, h3)): 
                        h1_ok = False
                        
        # Check phi maps H to Aut(N)
        for h in H:
            f = phi(h)
            img = [f(n) for n in N]
            if len(img) != len(N):
                h1_ok = False
            for n in N:
                if n not in img:
                    h1_ok = False
            for n1 in N:
                for n2 in N:
                    if f(N_op(n1, n2)) != N_op(f(n1), f(n2)): 
                        h1_ok = False
                        
        # Check phi is a homomorphism
        for h1 in H:
            for h2 in H:
                f12 = phi(H_op(h1, h2))
                f1 = phi(h1)
                f2 = phi(h2)
                for n in N:
                    if f12(n) != f1(f2(n)): 
                        h1_ok = False
    except Exception:
        h1_ok = False

    # H2: G = N \rtimes_\phi H is the external semidirect product
    try:
        N = witness.N
        H = witness.H
        G = witness.G
        G_op = witness.G_op
        N_op = witness.N_op
        H_op = witness.H_op
        phi = witness.phi
        
        h2_ok = True
        expected_G = [(n, h) for n in N for h in H]
        if len(G) != len(expected_G): 
            h2_ok = False
        else:
            for g in G:
                if g not in expected_G: 
                    h2_ok = False
                    break
        
        if h2_ok:
            for g1 in G:
                for g2 in G:
                    n1, h1 = g1
                    n2, h2 = g2
                    expected_res = (N_op(n1, phi(h1)(n2)), H_op(h1, h2))
                    if G_op(g1, g2) != expected_res: 
                        h2_ok = False
    except Exception:
        h2_ok = False

    # Negated Conclusion: N' is NOT a normal subgroup of G that is isomorphic to N
    try:
        N = witness.N
        H = witness.H
        G = witness.G
        G_op = witness.G_op
        e_H = witness.e_H
        
        neg_q_ok = False
        N_prime = [(n, e_H) for n in N]
        
        # Check if G is a group
        e_G = None
        for g in G:
            is_id = True
            for x in G:
                if G_op(g, x) != x or G_op(x, g) != x:
                    is_id = False
                    break
            if is_id:
                e_G = g
                break
                
        if e_G is None:
            neg_q_ok = True
        else:
            is_group = True
            for g in G:
                has_inv = False
                for inv in G:
                    if G_op(g, inv) == e_G and G_op(inv, g) == e_G:
                        has_inv = True
                        break
                if not has_inv:
                    is_group = False
                    break
            if is_group:
                for g1 in G:
                    for g2 in G:
                        for g3 in G:
                            if G_op(G_op(g1, g2), g3) != G_op(g1, G_op(g2, g3)):
                                is_group = False
                                break
                        if not is_group: break
                    if not is_group: break
            
            if not is_group:
                neg_q_ok = True
            else:
                # G is a group. Check if N' is a subgroup
                if e_G not in N_prime:
                    neg_q_ok = True
                else:
                    is_subgroup = True
                    for x in N_prime:
                        for y in N_prime:
                            if G_op(x, y) not in N_prime:
                                is_subgroup = False
                                break
                        if not is_subgroup: break
                    if is_subgroup:
                        for x in N_prime:
                            has_inv = False
                            for inv in N_prime:
                                if G_op(x, inv) == e_G and G_op(inv, x) == e_G:
                                    has_inv = True
                                    break
                            if not has_inv:
                                is_subgroup = False
                                break
                    
                    if not is_subgroup:
                        neg_q_ok = True
                    else:
                        # N' is a subgroup. Check if it is normal
                        is_normal = True
                        for g in G:
                            g_inv = None
                            for inv in G:
                                if G_op(g, inv) == e_G and G_op(inv, g) == e_G:
                                    g_inv = inv
                                    break
                            for n_p in N_prime:
                                conj = G_op(G_op(g, n_p), g_inv)
                                if conj not in N_prime:
                                    is_normal = False
                                    break
                            if not is_normal: break
                        
                        if not is_normal:
                            neg_q_ok = True
                        else:
                            # N' is a normal subgroup. Check if N is a group
                            N_op = witness.N_op
                            e_N = None
                            for n in N:
                                is_id = True
                                for x in N:
                                    if N_op(n, x) != x or N_op(x, n) != x:
                                        is_id = False
                                        break
                                if is_id:
                                    e_N = n
                                    break
                            if e_N is None:
                                neg_q_ok = True
                            else:
                                n_is_group = True
                                for n in N:
                                    has_inv = False
                                    for inv in N:
                                        if N_op(n, inv) == e_N and N_op(inv, n) == e_N:
                                            has_inv = True
                                            break
                                    if not has_inv:
                                        n_is_group = False
                                        break
                                if n_is_group:
                                    for n1 in N:
                                        for n2 in N:
                                            for n3 in N:
                                                if N_op(N_op(n1, n2), n3) != N_op(n1, N_op(n2, n3)):
                                                    n_is_group = False
                                                    break
                                            if not n_is_group: break
                                        if not n_is_group: break
                                if not n_is_group:
                                    neg_q_ok = True
                                else:
                                    # N is a group, N' is a normal subgroup.
                                    # They are isomorphic.
                                    neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: phi: H -> Aut(N) is a group homomorphism",
    "H_2: G = N \\rtimes_\\phi H is the external semidirect product of N and H",
    "¬Q: N' is not a normal subgroup of G that is isomorphic to N"
]

N_HYP = 2
NEG_Q_INDEX = 2