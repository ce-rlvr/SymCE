import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
    def get_elements(group):
        if hasattr(group, 'generate') and callable(group.generate):
            return list(group.generate())
        elif hasattr(group, 'elements'):
            return list(group.elements)
        else:
            return list(group)

    def get_map_val(mapping, key):
        if callable(mapping):
            return mapping(key)
        else:
            return mapping[key]

    H1_ok = False
    neg_Q_ok = False
    
    try:
        H = witness['H']
        K = witness['K']
        psi = witness['psi']
        
        H_elements = get_elements(H)
        K_elements = get_elements(K)
        
        H1_ok = True
        for h in H_elements:
            try:
                val = get_map_val(psi, h)
                if val not in K_elements:
                    H1_ok = False
                    break
            except Exception:
                H1_ok = False
                break
                
        if H1_ok:
            for h1 in H_elements:
                for h2 in H_elements:
                    try:
                        val12 = get_map_val(psi, h1 * h2)
                        val1 = get_map_val(psi, h1)
                        val2 = get_map_val(psi, h2)
                        if val12 != val1 * val2:
                            H1_ok = False
                            break
                    except Exception:
                        H1_ok = False
                        break
                if not H1_ok:
                    break
                    
        if H1_ok:
            image = []
            for h in H_elements:
                val = get_map_val(psi, h)
                if val not in image:
                    image.append(val)
            if len(image) != len(K_elements):
                H1_ok = False
    except Exception:
        H1_ok = False

    try:
        G = witness['G']
        H = witness['H']
        K = witness['K']
        phi = witness['phi']
        psi = witness['psi']
        
        G_elements = get_elements(G)
        H_elements = get_elements(H)
        K_elements = get_elements(K)
        
        valid_phi = True
        for g in G_elements:
            try:
                val = get_map_val(phi, g)
                if val not in H_elements:
                    valid_phi = False
                    break
            except Exception:
                valid_phi = False
                break
                
        if not valid_phi:
            neg_Q_ok = False
        else:
            comp = {}
            for g in G_elements:
                comp[g] = get_map_val(psi, get_map_val(phi, g))
                
            is_homo = True
            for g1 in G_elements:
                for g2 in G_elements:
                    if comp[g1 * g2] != comp[g1] * comp[g2]:
                        is_homo = False
                        break
                if not is_homo:
                    break
                    
            image = []
            for val in comp.values():
                if val not in image:
                    image.append(val)
            is_surj = (len(image) == len(K_elements))
            
            conclusion = is_homo and is_surj
            neg_Q_ok = not conclusion
    except Exception:
        neg_Q_ok = False

    return [H1_ok, neg_Q_ok]

CONDITION_LABELS = [
    "H_1: psi: H -> K is a surjective group homomorphism",
    "¬Q: The composition psi o phi: G -> K is not a surjective group homomorphism"
]

N_HYP = 1
NEG_Q_INDEX = 1