import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def extract_witness(witness):
    if isinstance(witness, dict):
        return witness['N'], witness['H'], witness['phi']
    elif hasattr(witness, 'N') and hasattr(witness, 'H') and hasattr(witness, 'phi'):
        return witness.N, witness.H, witness.phi
    elif isinstance(witness, (tuple, list)) and len(witness) == 3:
        return witness[0], witness[1], witness[2]
    else:
        raise ValueError("Witness must provide N, H, and phi")

def get_elements(G):
    if hasattr(G, 'elements'):
        elems = G.elements
        if callable(elems):
            elems = elems()
        return list(elems)
    return list(G)

def apply_phi(h, n, phi, elements_H, elements_N):
    if callable(phi):
        try:
            f = phi(h)
        except TypeError:
            return phi(h, n)
    elif isinstance(phi, list):
        try:
            f = phi[h]
        except TypeError:
            idx = elements_H.index(h)
            f = phi[idx]
    else:
        try:
            f = phi[h]
        except KeyError:
            idx = elements_H.index(h)
            f = phi[idx]
            
    if isinstance(f, dict):
        try:
            return f[n]
        except KeyError:
            idx = elements_N.index(n)
            return f[idx]
    elif isinstance(f, list):
        try:
            return f[n]
        except TypeError:
            idx = elements_N.index(n)
            return f[idx]
    else:
        return f(n)

def check_H1(N):
    if hasattr(N, 'is_abelian'):
        return bool(N.is_abelian)
    elements = get_elements(N)
    for a in elements:
        for b in elements:
            if a * b != b * a:
                return False
    return True

def check_H2(N, H, phi):
    elements_N = get_elements(N)
    elements_H = get_elements(H)
    
    # Check if phi[h] is an automorphism
    for h in elements_H:
        mapped_N = []
        for n in elements_N:
            mapped_n = apply_phi(h, n, phi, elements_H, elements_N)
            if mapped_n not in elements_N:
                return False
            mapped_N.append(mapped_n)
        for n in elements_N:
            if n not in mapped_N:
                return False
            
        for a in elements_N:
            for b in elements_N:
                if apply_phi(h, a * b, phi, elements_H, elements_N) != apply_phi(h, a, phi, elements_H, elements_N) * apply_phi(h, b, phi, elements_H, elements_N):
                    return False
                    
    # Check homomorphism
    for h1 in elements_H:
        for h2 in elements_H:
            h12 = h1 * h2
            for n in elements_N:
                if apply_phi(h12, n, phi, elements_H, elements_N) != apply_phi(h1, apply_phi(h2, n, phi, elements_H, elements_N), phi, elements_H, elements_N):
                    return False
                    
    # Check injectivity
    for h1 in elements_H:
        for h2 in elements_H:
            if h1 == h2:
                continue
            same = True
            for n in elements_N:
                if apply_phi(h1, n, phi, elements_H, elements_N) != apply_phi(h2, n, phi, elements_H, elements_N):
                    same = False
                    break
            if same:
                return False
                
    return True

def check_neg_Q(N, H, phi):
    elements_N = get_elements(N)
    elements_H = get_elements(H)
    
    SDP = [(n, h) for n in elements_N for h in elements_H]
    
    def mul(x, y):
        n1, h1 = x
        n2, h2 = y
        return (n1 * apply_phi(h1, n2, phi, elements_H, elements_N), h1 * h2)
        
    center = []
    for x in SDP:
        is_center = True
        for y in SDP:
            if mul(x, y) != mul(y, x):
                is_center = False
                break
        if is_center:
            center.append(x)
            
    id_H = None
    for e in elements_H:
        if all(e * h == h for h in elements_H):
            id_H = e
            break
            
    specified_subgroup = []
    for n in elements_N:
        fixed = True
        for h in elements_H:
            if apply_phi(h, n, phi, elements_H, elements_N) != n:
                fixed = False
                break
        if fixed:
            specified_subgroup.append((n, id_H))
            
    for c in center:
        if c not in specified_subgroup:
            return True
    for s in specified_subgroup:
        if s not in center:
            return True
            
    return False

def conditions(witness) -> list[bool]:
    try:
        N, H, phi = extract_witness(witness)
    except Exception:
        return [False, False, False]
        
    try:
        h1 = check_H1(N)
    except Exception:
        h1 = False
        
    try:
        h2 = check_H2(N, H, phi)
    except Exception:
        h2 = False
        
    try:
        neg_q = check_neg_Q(N, H, phi)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N is an abelian group",
    "H_2: phi is an injective group homomorphism from H to Aut(N)",
    "¬Q: The center of N rtimes H is not equal to the subgroup of elements (n, 1_H) such that n is fixed by phi_h for all h in H"
]

N_HYP = 2
NEG_Q_INDEX = 2