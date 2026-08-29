import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

def get_elements(G):
    if hasattr(G, 'elements'):
        return set(G.elements)
    return set(G.generate())

def is_subgroup(G_elements, N_elements, identity):
    N_set = set(N_elements)
    if identity not in N_set: 
        return False
    for n1 in N_set:
        if ~n1 not in N_set: 
            return False
        for n2 in N_set:
            if n1 * n2 not in N_set: 
                return False
    return True

def is_normal_subgroup(G_elements, N_elements, identity):
    if not is_subgroup(G_elements, N_elements, identity): 
        return False
    N_set = set(N_elements)
    for g in G_elements:
        for n in N_set:
            if g * n * ~g not in N_set: 
                return False
    return True

def is_maximal_normal_subgroup(G, N_elements):
    G_elements = get_elements(G)
    N_set = set(N_elements)
    
    if not N_set.issubset(G_elements): 
        return False
    if N_set == G_elements: 
        return False
    if not is_normal_subgroup(G_elements, N_set, G.identity): 
        return False
    
    # Check maximality: no normal subgroup strictly between N and G
    for g in G_elements - N_set:
        closure = set(N_set)
        closure.add(g)
        closure.add(~g)
        added = True
        while added:
            added = False
            new_elements = set()
            for x in list(closure):
                for y in list(closure):
                    if x * y not in closure:
                        new_elements.add(x * y)
            for x in list(closure):
                for h in G_elements:
                    if h * x * ~h not in closure:
                        new_elements.add(h * x * ~h)
            if new_elements:
                closure.update(new_elements)
                added = True
        
        # If the normal closure of N U {g} is strictly smaller than G, N is not maximal
        if closure < G_elements:
            return False
            
    return True

def conditions(witness):
    try:
        G, H, f_dict, N_obj = witness
        
        G_elements = get_elements(G)
        H_elements = get_elements(H)
        
        if hasattr(N_obj, 'elements') or hasattr(N_obj, 'generate'):
            N_elements = get_elements(N_obj)
        else:
            N_elements = set(N_obj)
            
        if isinstance(f_dict, dict):
            f_map = f_dict
        elif callable(f_dict):
            f_map = {g: f_dict(g) for g in G_elements}
        else:
            f_map = dict(f_dict)
            
        # H1: f is a surjective group homomorphism
        h1_ok = True
        for g1 in G_elements:
            if g1 not in f_map or f_map[g1] not in H_elements:
                h1_ok = False
                break
            for g2 in G_elements:
                if (g1 * g2) not in f_map or f_map[g1 * g2] != f_map[g1] * f_map[g2]:
                    h1_ok = False
                    break
            if not h1_ok: 
                break
                
        if h1_ok:
            image = set(f_map[g] for g in G_elements)
            if image != H_elements:
                h1_ok = False
    except Exception:
        h1_ok = False

    try:
        # H2: N is a maximal normal subgroup of G
        h2_ok = is_maximal_normal_subgroup(G, N_elements)
    except Exception:
        h2_ok = False

    try:
        # H3: ker(f) is a subset of N
        ker_f = {g for g in G_elements if f_map[g] == H.identity}
        h3_ok = ker_f.issubset(set(N_elements))
    except Exception:
        h3_ok = False

    try:
        # ¬Q: f(N) is not a maximal normal subgroup of H
        f_N = set(f_map[n] for n in N_elements)
        is_max_normal = is_maximal_normal_subgroup(H, f_N)
        neg_q_ok = not is_max_normal
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(h3_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: f: G -> H is a surjective group homomorphism",
    "H_2: N is a maximal normal subgroup of G",
    "H_3: ker(f) is a subset of N",
    "¬Q: f(N) is not a maximal normal subgroup of H"
]

N_HYP = 3
NEG_Q_INDEX = 3