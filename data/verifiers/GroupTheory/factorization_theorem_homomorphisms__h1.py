import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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

def get_elements(group):
    if hasattr(group, 'elements'):
        return list(group.elements)
    elif hasattr(group, 'generate'):
        return list(group.generate())
    else:
        return list(group)

def get_identity(elements):
    if not elements:
        return None
    for e in elements:
        if hasattr(e, 'is_Identity') and e.is_Identity:
            return e
    for e in elements:
        if all(e * x == x for x in elements):
            return e
    return None

def get_phi_val(phi_list, g):
    for k, v in phi_list:
        if k == g:
            return v
    return None

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            phi = witness.get('phi')
            N = witness.get('N')
        elif isinstance(witness, (list, tuple)) and len(witness) == 4:
            G, H, phi, N = witness
        else:
            return [False, False, False]
            
        if G is None or H is None or phi is None or N is None:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        G_elements = get_elements(G)
        H_elements = get_elements(H)
        
        h1 = True
        if callable(phi):
            phi_list = [(g, phi(g)) for g in G_elements]
        elif isinstance(phi, dict):
            phi_list = list(phi.items())
        elif isinstance(phi, list):
            phi_list = phi
        else:
            h1 = False
            phi_list = []
        
        if h1:
            for g in G_elements:
                val = get_phi_val(phi_list, g)
                if val is None:
                    h1 = False
                    break
                if not any(val == h for h in H_elements):
                    h1 = False
                    break
                    
        if h1:
            for g1 in G_elements:
                for g2 in G_elements:
                    val1 = get_phi_val(phi_list, g1)
                    val2 = get_phi_val(phi_list, g2)
                    val12 = get_phi_val(phi_list, g1 * g2)
                    if val12 != val1 * val2:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    try:
        N_elements = get_elements(N)
        h2 = True
        
        if not N_elements:
            h2 = False
        else:
            id_G = get_identity(G_elements)
            if id_G is None or not any(id_G == n for n in N_elements):
                h2 = False
                
            if h2:
                for n in N_elements:
                    if not any(n == g for g in G_elements):
                        h2 = False
                        break
                        
            if h2:
                for n1 in N_elements:
                    for n2 in N_elements:
                        if not any(n1 * n2 == n for n in N_elements):
                            h2 = False
                            break
                    if not h2:
                        break
                        
            if h2:
                for n in N_elements:
                    inv = None
                    for x in N_elements:
                        if n * x == id_G and x * n == id_G:
                            inv = x
                            break
                    if inv is None:
                        try:
                            if not any(n**-1 == x for x in N_elements):
                                h2 = False
                        except Exception:
                            h2 = False
                    if not h2:
                        break
                        
            if h2:
                for g in G_elements:
                    g_inv = None
                    for x in G_elements:
                        if g * x == id_G and x * g == id_G:
                            g_inv = x
                            break
                    if g_inv is None:
                        try:
                            g_inv = g**-1
                        except Exception:
                            h2 = False
                            break
                    for n in N_elements:
                        if not any(g * n * g_inv == x for x in N_elements):
                            h2 = False
                            break
                    if not h2:
                        break
                        
            if h2:
                id_H = get_identity(H_elements)
                for n in N_elements:
                    val = get_phi_val(phi_list, n)
                    if val != id_H:
                        h2 = False
                        break
    except Exception:
        h2 = False

    try:
        cosets = []
        g_to_coset_idx = []
        for g in G_elements:
            coset_list = []
            for n in N_elements:
                elem = g * n
                if not any(elem == x for x in coset_list):
                    coset_list.append(elem)
            
            found_idx = -1
            for idx, c in enumerate(cosets):
                if len(c) == len(coset_list):
                    if all(any(x == y for y in c) for x in coset_list):
                        found_idx = idx
                        break
            
            if found_idx == -1:
                cosets.append(coset_list)
                found_idx = len(cosets) - 1
                
            g_to_coset_idx.append((g, found_idx))
            
        bar_phi = []
        exists = True
        for g in G_elements:
            c_idx = -1
            for x, idx in g_to_coset_idx:
                if x == g:
                    c_idx = idx
                    break
            
            val = get_phi_val(phi_list, g)
            
            existing_val = None
            for idx, v in bar_phi:
                if idx == c_idx:
                    existing_val = v
                    break
            
            if existing_val is not None:
                if existing_val != val:
                    exists = False
                    break
            else:
                bar_phi.append((c_idx, val))
                
        is_homomorphism = False
        if exists:
            is_homomorphism = True
            for g1 in G_elements:
                for g2 in G_elements:
                    c1_idx = -1
                    c2_idx = -1
                    c12_idx = -1
                    for x, idx in g_to_coset_idx:
                        if x == g1: c1_idx = idx
                        if x == g2: c2_idx = idx
                        if x == g1 * g2: c12_idx = idx
                        
                    val1 = None
                    val2 = None
                    val12 = None
                    for idx, v in bar_phi:
                        if idx == c1_idx: val1 = v
                        if idx == c2_idx: val2 = v
                        if idx == c12_idx: val12 = v
                        
                    if val12 != val1 * val2:
                        is_homomorphism = False
                        break
                if not is_homomorphism:
                    break
                    
        q = exists and is_homomorphism
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: phi: G -> H is a group homomorphism",
    "H_2: N is a normal subgroup of G such that N is a subset of ker(phi)",
    "¬Q: There does not exist a unique group homomorphism bar_phi: G/N -> H such that phi(g) = bar_phi(gN) for all g in G"
]

N_HYP = 2
NEG_Q_INDEX = 2