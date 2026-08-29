import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
        if isinstance(witness, tuple) and len(witness) == 2:
            G, H = witness
        else:
            G = witness.G
            H = witness.H
    except Exception:
        return [False, False, False]

    # H_1: H is a subgroup of G
    try:
        if hasattr(H, 'is_subgroup'):
            if callable(H.is_subgroup):
                h1 = bool(H.is_subgroup(G))
            else:
                h1 = bool(H.is_subgroup)
        else:
            h_elems = set(H.elements)
            g_elems = set(G.elements)
            if not h_elems or not h_elems.issubset(g_elems):
                h1 = False
            elif hasattr(G, 'identity') and G.identity not in h_elems:
                h1 = False
            else:
                h1 = True
                for x in h_elems:
                    for y in h_elems:
                        if (x * y) not in h_elems:
                            h1 = False
                            break
                    if not h1:
                        break
    except Exception:
        h1 = False

    # H_2: For every endomorphism \phi of G, \phi(H) \subseteq H
    try:
        if hasattr(G, 'endomorphisms'):
            if callable(G.endomorphisms):
                endos = G.endomorphisms()
            else:
                endos = G.endomorphisms
            
            h_elements = list(H.elements)
            h2 = True
            for phi in endos:
                for h_elem in h_elements:
                    mapped = phi(h_elem) if callable(phi) else phi[h_elem]
                    if mapped not in h_elements:
                        h2 = False
                        break
                if not h2:
                    break
        else:
            elements = list(G.elements)
            gens = list(G.generators)
            
            endos = []
            for images in itertools.product(elements, repeat=len(gens)):
                mapping = {}
                valid = True
                for g, img in zip(gens, images):
                    if g in mapping and mapping[g] != img:
                        valid = False
                    mapping[g] = img
                if not valid: continue
                
                if G.identity in mapping:
                    if mapping[G.identity] != G.identity:
                        continue
                else:
                    mapping[G.identity] = G.identity
                    
                queue = [G.identity] + gens
                
                while queue and valid:
                    curr = queue.pop(0)
                    for g in gens:
                        nxt = curr * g
                        expected_img = mapping[curr] * mapping[g]
                        if nxt in mapping:
                            if mapping[nxt] != expected_img:
                                valid = False
                                break
                        else:
                            mapping[nxt] = expected_img
                            queue.append(nxt)
                            
                if valid and len(mapping) == len(elements):
                    endos.append(mapping)
                        
            h_elements = list(H.elements)
            h2 = True
            for phi in endos:
                for h_elem in h_elements:
                    if phi[h_elem] not in h_elements:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # neg_Q: H is NOT a normal subgroup of G
    try:
        if hasattr(H, 'is_normal'):
            if callable(H.is_normal):
                is_norm = bool(H.is_normal(G))
            else:
                is_norm = bool(H.is_normal)
        else:
            h_elems = set(H.elements)
            g_elems = set(G.elements)
            is_norm = True
            for g in g_elems:
                try:
                    g_inv = g**-1
                except Exception:
                    g_inv = None
                    for x in g_elems:
                        if x * g == G.identity and g * x == G.identity:
                            g_inv = x
                            break
                    if g_inv is None:
                        raise ValueError("No inverse found")
                
                for h in h_elems:
                    if (g * h * g_inv) not in h_elems:
                        is_norm = False
                        break
                if not is_norm:
                    break
        neg_q = not is_norm
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: For every endomorphism \\phi of G, \\phi(H) \\subseteq H",
    "¬Q: H is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2