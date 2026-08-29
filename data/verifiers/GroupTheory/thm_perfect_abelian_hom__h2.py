import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def get_order(grp):
    try:
        o = grp.order
        return o() if callable(o) else o
    except Exception:
        return len(list(grp.generate()))

def get_identity(grp):
    try:
        i = grp.identity
        return i() if callable(i) else i
    except Exception:
        return Permutation()

def get_generators(grp):
    try:
        gens = grp.generators
        return gens() if callable(gens) else gens
    except Exception:
        return []

def build_homomorphism(G, H, gen_map):
    mapping = {}
    ident_G = get_identity(G)
    ident_H = get_identity(H)
    mapping[ident_G] = ident_H
    
    queue = [ident_G]
    gens = get_generators(G)
    
    while queue:
        curr = queue.pop(0)
        curr_img = mapping[curr]
        
        for g in gens:
            nxt = curr * g
            nxt_img = curr_img * gen_map[g]
            
            if nxt in mapping:
                if mapping[nxt] != nxt_img:
                    return None
            else:
                mapping[nxt] = nxt_img
                queue.append(nxt)
                
    if len(mapping) != get_order(G):
        return None
        
    return mapping

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    G = None
    H = None
    phi_data = None
    phi = None

    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, H, phi_data = witness
        elif type(witness).__name__ == 'GroupHomomorphism':
            G = witness.domain
            H = witness.codomain
            phi_data = {g: witness(g) for g in get_generators(G)}
    except Exception:
        pass

    if G is not None:
        try:
            h1 = (get_order(G.derived_subgroup()) == get_order(G))
        except Exception:
            h1 = False

    if G is not None and H is not None and phi_data is not None:
        try:
            gen_map = None
            gens = get_generators(G)
            if isinstance(phi_data, list):
                if len(phi_data) == len(gens):
                    gen_map = {g: h for g, h in zip(gens, phi_data)}
            elif isinstance(phi_data, dict):
                gen_map = {g: phi_data[g] for g in gens}
            elif callable(phi_data):
                gen_map = {g: phi_data(g) for g in gens}
                
            if gen_map is not None:
                imgs_in_H = True
                for g, h in gen_map.items():
                    in_H = False
                    try:
                        in_H = (h in H)
                    except Exception:
                        try:
                            in_H = H.contains(h)
                        except Exception:
                            in_H = True
                    if not in_H:
                        imgs_in_H = False
                        break
                
                if imgs_in_H:
                    phi = build_homomorphism(G, H, gen_map)
        except Exception:
            phi = None

    if phi is not None:
        h2 = True
        try:
            neg_q = False
            ident_H = get_identity(H)
            for g in get_generators(G):
                if phi[g] != ident_H:
                    neg_q = True
                    break
        except Exception:
            neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a perfect group",
    "H_2: phi is a group homomorphism from G to H",
    "¬Q: phi is not the trivial homomorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2