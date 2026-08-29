import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import itertools

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 4:
            return [False, False, False]
        N, H, phi, G_mult = witness
    except Exception:
        return [False, False, False]

    # H_1: N and H are groups
    try:
        h1 = hasattr(N, 'elements') and hasattr(H, 'elements') and hasattr(N, 'identity') and hasattr(H, 'identity')
    except Exception:
        h1 = False

    # H_2: phi is a group homomorphism from H to Aut(N)
    try:
        h2 = True
        if h1:
            N_elems = list(N.elements)
            H_elems = list(H.elements)
            for h in H_elems:
                if callable(phi):
                    mapping = phi(h)
                else:
                    if h not in phi:
                        h2 = False; break
                    mapping = phi[h]
                
                mapped_elems = []
                for n in N_elems:
                    if callable(mapping):
                        mapped_n = mapping(n)
                    else:
                        if n not in mapping:
                            h2 = False; break
                        mapped_n = mapping[n]
                    mapped_elems.append(mapped_n)
                if not h2: break
                
                if len(set(mapped_elems)) != len(N_elems):
                    h2 = False; break
                
                for n1 in N_elems:
                    for n2 in N_elems:
                        if callable(mapping):
                            m_n1 = mapping(n1)
                            m_n2 = mapping(n2)
                            m_n1n2 = mapping(n1 * n2)
                        else:
                            m_n1 = mapping[n1]
                            m_n2 = mapping[n2]
                            m_n1n2 = mapping[n1 * n2]
                        if m_n1n2 != m_n1 * m_n2:
                            h2 = False; break
                    if not h2: break
                if not h2: break
                
            if h2:
                for h1_elem in H_elems:
                    for h2_elem in H_elems:
                        h12 = h1_elem * h2_elem
                        if callable(phi):
                            map1 = phi(h1_elem)
                            map2 = phi(h2_elem)
                            map12 = phi(h12)
                        else:
                            map1 = phi[h1_elem]
                            map2 = phi[h2_elem]
                            map12 = phi[h12]
                            
                        for n in N_elems:
                            if callable(map2):
                                m2_n = map2(n)
                            else:
                                m2_n = map2[n]
                                
                            if callable(map1):
                                m1_m2_n = map1(m2_n)
                            else:
                                m1_m2_n = map1[m2_n]
                                
                            if callable(map12):
                                m12_n = map12(n)
                            else:
                                m12_n = map12[n]
                                
                            if m12_n != m1_m2_n:
                                h2 = False; break
                        if not h2: break
                    if not h2: break
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: The conclusion fails
    try:
        neg_q = False
        if h1:
            e_N = N.identity
            e_H = H.identity
            N_elems = list(N.elements)
            H_elems = list(H.elements)
            G_elems = list(itertools.product(N_elems, H_elems))
            
            is_group = True
            for g1 in G_elems:
                for g2 in G_elems:
                    if G_mult(g1, g2) not in G_elems:
                        is_group = False; break
                if not is_group: break
                
            if is_group:
                e_G = (e_N, e_H)
                for g in G_elems:
                    if G_mult(e_G, g) != g or G_mult(g, e_G) != g:
                        is_group = False; break
                        
            if is_group:
                for g in G_elems:
                    has_inv = False
                    for inv in G_elems:
                        if G_mult(g, inv) == e_G and G_mult(inv, g) == e_G:
                            has_inv = True; break
                    if not has_inv:
                        is_group = False; break
                        
            if is_group:
                for g1 in G_elems:
                    for g2 in G_elems:
                        for g3 in G_elems:
                            if G_mult(G_mult(g1, g2), g3) != G_mult(g1, G_mult(g2, g3)):
                                is_group = False; break
                        if not is_group: break
                    if not is_group: break

            if not is_group:
                neg_q = True
            else:
                H_prime = [(e_N, h) for h in H_elems]
                N_prime = [(n, e_H) for n in N_elems]
                
                H_prime_is_subgroup = True
                for h1_elem in H_prime:
                    for h2_elem in H_prime:
                        if G_mult(h1_elem, h2_elem) not in H_prime:
                            H_prime_is_subgroup = False; break
                    if not H_prime_is_subgroup: break
                    
                H_prime_isomorphic = True
                if H_prime_is_subgroup:
                    for h1_elem in H_elems:
                        for h2_elem in H_elems:
                            if G_mult((e_N, h1_elem), (e_N, h2_elem)) != (e_N, h1_elem * h2_elem):
                                H_prime_isomorphic = False; break
                        if not H_prime_isomorphic: break
                else:
                    H_prime_isomorphic = False
                    
                N_prime_is_normal = True
                for n1 in N_prime:
                    for n2 in N_prime:
                        if G_mult(n1, n2) not in N_prime:
                            N_prime_is_normal = False; break
                    if not N_prime_is_normal: break
                    
                if N_prime_is_normal:
                    for g in G_elems:
                        g_inv = None
                        for inv in G_elems:
                            if G_mult(g, inv) == e_G and G_mult(inv, g) == e_G:
                                g_inv = inv; break
                        for n in N_prime:
                            if G_mult(G_mult(g, n), g_inv) not in N_prime:
                                N_prime_is_normal = False; break
                        if not N_prime_is_normal: break
                        
                intersection_trivial = True
                for x in N_prime:
                    if x in H_prime and x != e_G:
                        intersection_trivial = False; break
                        
                product_is_G = True
                NH_product = set()
                for n in N_prime:
                    for h in H_prime:
                        NH_product.add(G_mult(n, h))
                if len(NH_product) != len(G_elems):
                    product_is_G = False
                    
                conclusion = (H_prime_is_subgroup and H_prime_isomorphic and 
                              N_prime_is_normal and intersection_trivial and product_is_G)
                neg_q = not conclusion
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N and H are groups",
    "H_2: phi is a group homomorphism from H to Aut(N)",
    "¬Q: H' is not a subgroup of G isomorphic to H, or G is not the internal semidirect product of N' and H'"
]

N_HYP = 2
NEG_Q_INDEX = 2