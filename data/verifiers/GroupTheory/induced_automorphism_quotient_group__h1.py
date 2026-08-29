import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    try:
        G, N, phi = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        G_elements = list(G.generate()) if hasattr(G, "generate") else list(G.elements)
        N_elements = list(N.generate()) if hasattr(N, "generate") else list(N.elements)
    except Exception:
        try:
            G_elements = list(G.elements)
            N_elements = list(N.elements)
        except Exception:
            return [False, False, False, False]

    try:
        if isinstance(phi, dict):
            phi_dict = phi
        else:
            phi_dict = {g: phi(g) for g in G_elements}
    except Exception:
        phi_dict = None

    # H1: N is a normal subgroup of G
    try:
        h1 = True
        for gen in N.generators:
            if gen not in G:
                h1 = False
                break
        if h1:
            for g in G.generators:
                for n in N.generators:
                    if (g * n * (g**-1)) not in N:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H2: \phi is an automorphism of G
    try:
        h2 = True
        if phi_dict is None:
            h2 = False
        elif set(phi_dict.keys()) != set(G_elements):
            h2 = False
        elif set(phi_dict.values()) != set(G_elements):
            h2 = False
        else:
            for g1 in G_elements:
                for g2 in G_elements:
                    if phi_dict[g1 * g2] != phi_dict[g1] * phi_dict[g2]:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # H3: \phi(N) = N
    try:
        if phi_dict is None:
            h3 = False
        else:
            mapped_N = {phi_dict[n] for n in N_elements}
            h3 = (mapped_N == set(N_elements))
    except Exception:
        h3 = False

    # neg_Q: \bar{\phi} is NOT an automorphism of G/N
    try:
        if phi_dict is None:
            neg_q = False
        else:
            is_auto = True
            bar_phi = {}
            cosets = set()
            
            # Check well-definedness and build the map
            for g in G_elements:
                coset = frozenset(g * n for n in N_elements)
                cosets.add(coset)
                mapped_coset = frozenset(phi_dict[g] * n for n in N_elements)
                
                if coset in bar_phi:
                    if bar_phi[coset] != mapped_coset:
                        is_auto = False
                        break
                else:
                    bar_phi[coset] = mapped_coset
                    
            # Check bijectivity
            if is_auto:
                if set(bar_phi.values()) != cosets:
                    is_auto = False
                    
            # Check homomorphism
            if is_auto:
                for x in G_elements:
                    for y in G_elements:
                        coset_x = frozenset(x * n for n in N_elements)
                        coset_y = frozenset(y * n for n in N_elements)
                        coset_xy = frozenset((x * y) * n for n in N_elements)
                        
                        mapped_x = bar_phi[coset_x]
                        mapped_y = bar_phi[coset_y]
                        mapped_xy = bar_phi[coset_xy]
                        
                        rep_x = next(iter(mapped_x))
                        rep_y = next(iter(mapped_y))
                        prod_coset = frozenset((rep_x * rep_y) * n for n in N_elements)
                        
                        if mapped_xy != prod_coset:
                            is_auto = False
                            break
                    if not is_auto:
                        break
                        
            neg_q = not is_auto
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    r"H_1: N is a normal subgroup of G",
    r"H_2: \phi is an automorphism of G",
    r"H_3: \phi(N) = N",
    r"¬Q: The map \bar{\phi} is not an automorphism of G/N"
]

N_HYP = 3
NEG_Q_INDEX = 3