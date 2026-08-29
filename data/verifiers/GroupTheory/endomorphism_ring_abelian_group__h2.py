import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def check_neg_Q(G):
    if not hasattr(G, 'generators'):
        return False
        
    elements = []
    if hasattr(G, 'generate'):
        for el in G.generate():
            elements.append(el)
            if len(elements) > 200:
                return False
    elif hasattr(G, 'elements'):
        elements = list(G.elements)
        if len(elements) > 200:
            return False
    else:
        return False
        
    if not elements:
        return False
        
    if hasattr(G, 'identity'):
        identity = G.identity
    else:
        identity = None
        for e in elements:
            if e * e == e:
                identity = e
                break
        if identity is None:
            return False
            
    inverses = {}
    for e in elements:
        for inv_e in elements:
            if e * inv_e == identity and inv_e * e == identity:
                inverses[e] = inv_e
                break
        if e not in inverses:
            return False
            
    gens = list(G.generators)
    elem_to_idx = {e: i for i, e in enumerate(elements)}
    
    endos = []
    for images in itertools.product(elements, repeat=len(gens)):
        mapping = {identity: identity}
        for g, img in zip(gens, images):
            mapping[g] = img
        
        queue = list(gens)
        valid = True
        while queue:
            curr = queue.pop(0)
            for g in gens:
                nxt = curr * g
                nxt_img = mapping[curr] * mapping[g]
                if nxt in mapping:
                    if mapping[nxt] != nxt_img:
                        valid = False
                        break
                else:
                    mapping[nxt] = nxt_img
                    queue.append(nxt)
            if not valid:
                break
        
        if valid and len(mapping) == len(elements):
            for x in elements:
                for y in elements:
                    if mapping[x*y] != mapping[x] * mapping[y]:
                        valid = False
                        break
                if not valid:
                    break
            if valid:
                endo_tuple = tuple(mapping[x] for x in elements)
                endos.append(endo_tuple)
                
    endos = set(endos)
    
    # Check closure under pointwise addition
    for f in endos:
        for g in endos:
            h = tuple(f[i] * g[i] for i in range(len(elements)))
            if h not in endos:
                return True
                
    # Check commutativity of addition
    for f in endos:
        for g in endos:
            for i in range(len(elements)):
                if f[i] * g[i] != g[i] * f[i]:
                    return True
                    
    # Check identity of addition
    zero_endo = tuple(identity for _ in elements)
    if zero_endo not in endos:
        return True
        
    # Check inverses of addition
    for f in endos:
        inv_f = tuple(inverses[f[i]] for i in range(len(elements)))
        if inv_f not in endos:
            return True
            
    def compose(f, g):
        return tuple(f[elem_to_idx[g[i]]] for i in range(len(elements)))
        
    # Check distributivity
    for f in endos:
        for g in endos:
            for h in endos:
                f_plus_g = tuple(f[i] * g[i] for i in range(len(elements)))
                left1 = compose(f_plus_g, h)
                right1 = tuple(compose(f, h)[i] * compose(g, h)[i] for i in range(len(elements)))
                if left1 != right1:
                    return True
                    
                g_plus_h = tuple(g[i] * h[i] for i in range(len(elements)))
                left2 = compose(f, g_plus_h)
                right2 = tuple(compose(f, g)[i] * compose(f, h)[i] for i in range(len(elements)))
                if left2 != right2:
                    return True

    # Check units == Aut(G)
    aut_G = set()
    for f in endos:
        if len(set(f)) == len(elements):
            aut_G.add(f)
            
    id_map = tuple(elements)
    if id_map not in endos:
        return True
        
    units = set()
    for f in endos:
        is_unit = False
        for g in endos:
            if compose(f, g) == id_map and compose(g, f) == id_map:
                is_unit = True
                break
        if is_unit:
            units.add(f)
            
    if units != aut_G:
        return True
        
    return False

def conditions(witness) -> list[bool]:
    try:
        h1 = bool(witness.is_abelian)
    except Exception:
        h1 = False

    try:
        neg_q = check_neg_Q(witness)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "¬Q: End(G) does not form a ring under pointwise addition and function composition, or the group of units is not Aut(G)"
]

N_HYP = 1
NEG_Q_INDEX = 1