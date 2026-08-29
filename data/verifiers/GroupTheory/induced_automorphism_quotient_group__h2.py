import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import itertools

# Top-level setup
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
        G, N, phi = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: phi is an automorphism of G
    try:
        try:
            elements = list(G.generate_dimino())
        except Exception:
            elements = list(G.elements)
            
        if isinstance(phi, dict):
            phi_func = lambda x: phi.get(x, None)
        else:
            phi_func = phi
            
        image = set()
        h2 = True
        for g in elements:
            img = phi_func(g)
            if img not in elements:
                h2 = False
                break
            image.add(img)
            
        if h2:
            if len(image) != len(elements):
                h2 = False
            else:
                for g1 in elements:
                    for g2 in elements:
                        if phi_func(g1 * g2) != phi_func(g1) * phi_func(g2):
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False
        
    # H3: phi(N) = N
    try:
        if not isinstance(N, PermutationGroup):
            h3 = False
        else:
            is_sub = True
            for gen in N.generators:
                if gen not in elements:
                    is_sub = False
                    break
            if not is_sub:
                h3 = False
            else:
                try:
                    n_elements = list(N.generate_dimino())
                except Exception:
                    n_elements = list(N.elements)
                
                image_N = set()
                for n in n_elements:
                    image_N.add(phi_func(n))
                h3 = (image_N == set(n_elements))
    except Exception:
        h3 = False
        
    # neg_Q: G/N is not a quotient group (N is not normal in G)
    try:
        is_norm = True
        try:
            n_elements_set = set(N.generate_dimino())
        except Exception:
            n_elements_set = set(N.elements)
            
        for g in elements:
            g_inv = ~g
            for n in n_elements_set:
                if g * n * g_inv not in n_elements_set:
                    is_norm = False
                    break
            if not is_norm:
                break
        neg_q = not is_norm
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: \\phi is an automorphism of G",
    "H_3: \\phi(N) = N",
    "¬Q: G/N is not a quotient group (N is not normal in G)"
]

N_HYP = 3
NEG_Q_INDEX = 3