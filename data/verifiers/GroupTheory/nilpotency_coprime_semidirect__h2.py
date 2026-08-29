import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness expressions
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

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False]
        N, H, phi = witness
    except Exception:
        return [False, False, False]
        
    # H_1: N and H are finite groups
    try:
        h1_ok = isinstance(N, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1_ok = False
        
    # H_2: phi: H -> Aut(N) is a group homomorphism
    try:
        if not h1_ok:
            h2_ok = False
        elif not callable(phi):
            h2_ok = False
        else:
            try:
                N_elems = list(N.generate())
            except AttributeError:
                N_elems = list(N.elements)
            try:
                H_elems = list(H.generate())
            except AttributeError:
                H_elems = list(H.elements)
                
            h2_ok = True
            for h in H_elems:
                mapped_N = []
                for n in N_elems:
                    pn = phi(h, n)
                    if pn not in N_elems:
                        h2_ok = False
                        break
                    if pn not in mapped_N:
                        mapped_N.append(pn)
                if not h2_ok: break
                if len(mapped_N) != len(N_elems):
                    h2_ok = False
                    break
                    
                for n1 in N_elems:
                    for n2 in N_elems:
                        if phi(h, n1 * n2) != phi(h, n1) * phi(h, n2):
                            h2_ok = False
                            break
                    if not h2_ok: break
                if not h2_ok: break
                
            if h2_ok:
                for h1 in H_elems:
                    for h2 in H_elems:
                        for n in N_elems:
                            if phi(h1 * h2, n) != phi(h1, phi(h2, n)):
                                h2_ok = False
                                break
                        if not h2_ok: break
                    if not h2_ok: break
    except Exception:
        h2_ok = False
        
    # neg_Q: The conclusion fails at the witness
    try:
        if not (h1_ok and h2_ok):
            neg_q = False
        else:
            try:
                N_elems = list(N.generate())
            except AttributeError:
                N_elems = list(N.elements)
            try:
                H_elems = list(H.generate())
            except AttributeError:
                H_elems = list(H.elements)
                
            def is_nilpotent_group(elements, mult):
                identity = None
                for e in elements:
                    if mult(e, e) == e:
                        identity = e
                        break
                if identity is None:
                    return False
                    
                G_i = list(elements)
                inverses = []
                for x in elements:
                    for y in elements:
                        if mult(x, y) == identity:
                            inverses.append((x, y))
                            break
                            
                def get_inv(x):
                    for a, b in inverses:
                        if a == x:
                            return b
                    return x
                    
                while True:
                    commutators = []
                    for x in G_i:
                        for y in elements:
                            x_inv = get_inv(x)
                            y_inv = get_inv(y)
                            comm = mult(mult(mult(x_inv, y_inv), x), y)
                            if comm not in commutators:
                                commutators.append(comm)
                                
                    subgroup = list(commutators)
                    added = True
                    while added:
                        added = False
                        for a in subgroup:
                            for b in subgroup:
                                c = mult(a, b)
                                if c not in subgroup:
                                    subgroup.append(c)
                                    added = True
                                    
                    next_G_i = subgroup
                    if len(next_G_i) == len(G_i):
                        return len(next_G_i) == 1
                    G_i = next_G_i

            SD_elems = [(n, h) for n in N_elems for h in H_elems]
            def SD_mult(x, y):
                n1, h1 = x
                n2, h2 = y
                return (n1 * phi(h1, n2), h1 * h2)
                
            SD_nilpotent = is_nilpotent_group(SD_elems, SD_mult)
            N_nilpotent = is_nilpotent_group(N_elems, lambda x, y: x * y)
            H_nilpotent = is_nilpotent_group(H_elems, lambda x, y: x * y)
            
            phi_trivial = True
            for h in H_elems:
                for n in N_elems:
                    if phi(h, n) != n:
                        phi_trivial = False
                        break
                if not phi_trivial:
                    break
                    
            rhs = N_nilpotent and H_nilpotent and phi_trivial
            
            # The conclusion is an iff statement. It fails if the two sides have different truth values.
            neg_q = (SD_nilpotent != rhs)
    except Exception:
        neg_q = False
        
    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: N and H are finite groups",
    "H_2: phi is a group homomorphism from H to Aut(N)",
    "¬Q: N ⋊_phi H is nilpotent iff N and H are nilpotent and phi is trivial (fails)"
]

N_HYP = 2
NEG_Q_INDEX = 2