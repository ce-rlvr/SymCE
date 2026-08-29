import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import itertools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: alpha is a surjective group homomorphism from G to H",
    "H_3: beta is a group homomorphism from F to H",
    "¬Q: There does not exist a group homomorphism gamma: F -> G such that alpha(gamma(x)) = beta(x)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def get_identity(group):
    if hasattr(group, 'identity'):
        return group.identity
    for e in group.elements:
        if e.order() == 1:
            return e
    return None

def get_full_map(domain, codomain, mapping):
    if callable(mapping):
        try:
            return {g: mapping(g) for g in domain.elements}
        except Exception:
            pass
    if hasattr(mapping, 'image'):
        try:
            return {g: mapping.image(g) for g in domain.elements}
        except Exception:
            pass
    if isinstance(mapping, dict):
        try:
            if all(g in mapping for g in domain.elements):
                return mapping
        except Exception:
            pass
        try:
            id_dom = get_identity(domain)
            id_cod = get_identity(codomain)
            if id_dom is None or id_cod is None:
                return None
                
            full_map = {id_dom: id_cod}
            queue = [id_dom]
            gens = list(mapping.keys())
            for g in gens:
                if g not in domain:
                    return None
            while queue:
                curr = queue.pop(0)
                for g in gens:
                    nxt = curr * g
                    if nxt not in full_map:
                        full_map[nxt] = full_map[curr] * mapping[g]
                        queue.append(nxt)
            if len(full_map) != domain.order():
                return None
            for g in gens:
                if full_map[g] != mapping[g]:
                    return None
            return full_map
        except Exception:
            return None
    return None

def is_valid_homomorphism(domain, codomain, mapping):
    try:
        if domain.order() > 1024:
            return False
        full_map = get_full_map(domain, codomain, mapping)
        if full_map is None:
            return False
        for v in full_map.values():
            if v not in codomain:
                return False
        for g in domain.elements:
            for h in domain.elements:
                if full_map[g * h] != full_map[g] * full_map[h]:
                    return False
        return True
    except Exception:
        return False

def is_surjective(domain, codomain, mapping):
    try:
        full_map = get_full_map(domain, codomain, mapping)
        if full_map is None:
            return False
        image_elements = set(full_map.values())
        codomain_elements = set(codomain.elements)
        return image_elements == codomain_elements
    except Exception:
        return False

def neg_q_check(G, H, F, alpha, beta):
    try:
        full_alpha = get_full_map(G, H, alpha)
        full_beta = get_full_map(F, H, beta)
        if full_alpha is None or full_beta is None:
            return False
        
        F_gens = F.generators
        if G.order() ** len(F_gens) > 100000:
            return False
            
        for images in itertools.product(G.elements, repeat=len(F_gens)):
            gamma_mapping = dict(zip(F_gens, images))
            full_gamma = get_full_map(F, G, gamma_mapping)
            if full_gamma is None:
                continue
            
            is_hom = True
            for g in F.elements:
                for h in F.elements:
                    if full_gamma[g * h] != full_gamma[g] * full_gamma[h]:
                        is_hom = False
                        break
                if not is_hom:
                    break
            if not is_hom:
                continue
            
            commutes = True
            for x in F.elements:
                if full_alpha[full_gamma[x]] != full_beta[x]:
                    commutes = False
                    break
            if commutes:
                return False 
                
        return True 
    except Exception:
        return False

def conditions(witness):
    try:
        G = witness['G']
        H = witness['H']
        F = witness['F']
        alpha = witness['alpha']
        beta = witness['beta']
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = False
        if h1:
            if is_valid_homomorphism(G, H, alpha) and is_surjective(G, H, alpha):
                h2 = True
    except Exception:
        h2 = False

    try:
        h3 = False
        if isinstance(F, PermutationGroup) and isinstance(H, PermutationGroup):
            if is_valid_homomorphism(F, H, beta):
                h3 = True
    except Exception:
        h3 = False

    try:
        neg_q = False
        if h1 and h2 and h3:
            neg_q = neg_q_check(G, H, F, alpha, beta)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]