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

def conditions(witness):
    try:
        if isinstance(witness, dict):
            N = witness['N']
            H = witness['H']
            phi = witness['phi']
            G_elems = witness.get('G_elems', witness.get('G'))
            G_op = witness.get('G_op', getattr(G_elems, 'op', None))
            n = witness['n']
            h = witness['h']
        else:
            N = witness.N
            H = witness.H
            phi = witness.phi
            G_elems = getattr(witness, 'G_elems', getattr(witness, 'G', None))
            G_op = getattr(witness, 'G_op', getattr(G_elems, 'op', None))
            n = witness.n
            h = witness.h
            
        if G_elems is None or G_op is None:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    def eval_phi(h_val, n_val):
        if callable(phi):
            return phi(h_val, n_val)
        return phi[h_val][n_val]

    # H1: N and H are groups
    try:
        if hasattr(N, 'generate'):
            N_elems = list(N.generate())
        elif hasattr(N, 'elements'):
            N_elems = list(N.elements)
        else:
            N_elems = list(N)
            
        if hasattr(H, 'generate'):
            H_elems = list(H.generate())
        elif hasattr(H, 'elements'):
            H_elems = list(H.elements)
        else:
            H_elems = list(H)
            
        h1 = True
        if not N_elems or not H_elems:
            h1 = False
        else:
            for x in N_elems:
                if x**-1 not in N_elems:
                    h1 = False
                for y in N_elems:
                    if x*y not in N_elems:
                        h1 = False
            for x in H_elems:
                if x**-1 not in H_elems:
                    h1 = False
                for y in H_elems:
                    if x*y not in H_elems:
                        h1 = False
    except Exception:
        h1 = False

    # H2: phi: H -> Aut(N) is a group homomorphism
    try:
        h2 = True
        for h_elem in H_elems:
            mapped_N = []
            for n_elem in N_elems:
                pn = eval_phi(h_elem, n_elem)
                if pn not in N_elems:
                    h2 = False
                    break
                mapped_N.append(pn)
            if not h2: break
            
            if len(set(mapped_N)) != len(N_elems):
                h2 = False
                break
                
            for n1 in N_elems:
                for n2 in N_elems:
                    if eval_phi(h_elem, n1 * n2) != eval_phi(h_elem, n1) * eval_phi(h_elem, n2):
                        h2 = False
                        break
                if not h2: break
            if not h2: break
            
        if h2:
            for h1_elem in H_elems:
                for h2_elem in H_elems:
                    for n_elem in N_elems:
                        if eval_phi(h1_elem * h2_elem, n_elem) != eval_phi(h1_elem, eval_phi(h2_elem, n_elem)):
                            h2 = False
                            break
                    if not h2: break
                if not h2: break
    except Exception:
        h2 = False

    # H3: (n, h) is an element of G
    try:
        G_elems_list = list(G_elems)
        h3 = (n, h) in G_elems_list
    except Exception:
        h3 = False

    # neg_Q: The inverse of (n, h) in G is NOT (phi_{h^{-1}}(n^{-1}), h^{-1})
    try:
        e_G = None
        if G_elems_list:
            x = G_elems_list[0]
            candidates = [e for e in G_elems_list if G_op(e, x) == x]
            for e in candidates:
                is_id = True
                for y in G_elems_list:
                    if G_op(e, y) != y or G_op(y, e) != y:
                        is_id = False
                        break
                if is_id:
                    e_G = e
                    break
                    
        if e_G is None:
            neg_q = True
        else:
            inv_G = None
            for y in G_elems_list:
                if G_op((n, h), y) == e_G and G_op(y, (n, h)) == e_G:
                    inv_G = y
                    break
            
            if inv_G is None:
                neg_q = True
            else:
                h_inv = h**-1
                n_inv = n**-1
                expected_inv = (eval_phi(h_inv, n_inv), h_inv)
                neg_q = (inv_G != expected_inv)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: N and H are groups",
    "H_2: phi: H -> Aut(N) is a group homomorphism",
    "H_3: (n, h) is an element of G",
    "¬Q: The inverse of (n, h) in G is not (phi_{h^{-1}}(n^{-1}), h^{-1})"
]

N_HYP = 3
NEG_Q_INDEX = 3