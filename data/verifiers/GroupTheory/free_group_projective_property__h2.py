import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math
import z3

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

CONDITION_LABELS = [
    "H_1: F is a free group",
    "H_2: alpha is a surjective group homomorphism from G to H",
    "H_3: beta is a group homomorphism from F to H",
    "¬Q: There is no group homomorphism gamma: F -> G such that alpha o gamma = beta"
]

N_HYP = 3
NEG_Q_INDEX = 3

def get_elements(group):
    if hasattr(group, 'order'):
        try:
            if group.order() > 100:
                return None
        except Exception:
            return None
    if hasattr(group, 'elements'):
        try:
            return list(group.elements)
        except Exception:
            return None
    if isinstance(group, (list, set, tuple)):
        return list(group)
    return None

def get_mapping(mapping, x):
    if callable(mapping):
        return mapping(x)
    elif isinstance(mapping, dict):
        return mapping[x]
    else:
        return mapping(x)

def is_homomorphism(domain, codomain, mapping):
    if mapping.__class__.__name__ == 'Homomorphism':
        return True
        
    if domain.__class__.__name__ == 'FreeGroup':
        gens = domain.generators
        try:
            for g in gens:
                get_mapping(mapping, g)
            return True
        except Exception:
            return False
            
    elements = get_elements(domain)
    if elements is None:
        return False
        
    for x in elements:
        for y in elements:
            try:
                xy = x * y
                mx = get_mapping(mapping, x)
                my = get_mapping(mapping, y)
                mxy = get_mapping(mapping, xy)
                if mx * my != mxy:
                    return False
            except Exception:
                return False
    return True

def is_surjective(domain, codomain, mapping):
    if mapping.__class__.__name__ == 'Homomorphism':
        try:
            im = mapping.image()
            if hasattr(im, 'order') and hasattr(codomain, 'order'):
                return im.order() == codomain.order()
        except Exception:
            pass

    codomain_elements = get_elements(codomain)
    if codomain_elements is None:
        return False
    try:
        codomain_elements = set(codomain_elements)
    except Exception:
        return False
        
    domain_elements = get_elements(domain)
    if domain_elements is None:
        if isinstance(mapping, dict):
            try:
                return set(mapping.values()) == codomain_elements
            except Exception:
                return False
        return False
        
    image = set()
    for x in domain_elements:
        try:
            image.add(get_mapping(mapping, x))
        except Exception:
            return False
        
    return image == codomain_elements

def check_H1(F):
    try:
        if F.__class__.__name__ == 'FreeGroup':
            return True
        if F.__class__.__name__ == 'FpGroup':
            return len(F.relators) == 0
        if hasattr(F, 'order'):
            return F.order() == 1
        return False
    except Exception:
        return False

def check_H2(G, H, alpha):
    try:
        if not is_homomorphism(G, H, alpha):
            return False
        if not is_surjective(G, H, alpha):
            return False
        return True
    except Exception:
        return False

def check_H3(F, H, beta):
    try:
        return is_homomorphism(F, H, beta)
    except Exception:
        return False

def check_neg_Q(F, G, H, alpha, beta):
    try:
        if F.__class__.__name__ == 'FreeGroup':
            gens_F = F.generators
            for x in gens_F:
                hx = get_mapping(beta, x)
                preimage = None
                if isinstance(alpha, dict):
                    for g, h in alpha.items():
                        if h == hx:
                            preimage = g
                            break
                    if preimage is None:
                        return True
                else:
                    elements_G = get_elements(G)
                    if elements_G is not None:
                        for g in elements_G:
                            if get_mapping(alpha, g) == hx:
                                preimage = g
                                break
                        if preimage is None:
                            return True
                    else:
                        return False
            return False
            
        elements_F = get_elements(F)
        elements_G = get_elements(G)
        
        if elements_F is None or elements_G is None:
            return False
            
        if len(elements_F) == 1:
            id_F = elements_F[0]
            id_G = None
            for g in elements_G:
                try:
                    if g * g == g:
                        id_G = g
                        break
                except Exception:
                    pass
            if id_G is None: return False
            if get_mapping(alpha, id_G) == get_mapping(beta, id_F):
                return False
            return True
            
        if len(elements_F) > 6 or len(elements_G) > 10:
            return False
            
        for mapping_tuple in itertools.product(elements_G, repeat=len(elements_F)):
            mapping = dict(zip(elements_F, mapping_tuple))
            if is_homomorphism(F, G, mapping):
                valid = True
                for x in elements_F:
                    if get_mapping(alpha, mapping[x]) != get_mapping(beta, x):
                        valid = False
                        break
                if valid:
                    return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            G = witness.get('G')
            H = witness.get('H')
            alpha = witness.get('alpha')
            beta = witness.get('beta')
        else:
            F, G, H, alpha, beta = witness
    except Exception:
        return [False, False, False, False]
        
    h1 = check_H1(F)
    h2 = check_H2(G, H, alpha)
    h3 = check_H3(F, H, beta)
    neg_q = check_neg_Q(F, G, H, alpha, beta)
    
    return [h1, h2, h3, neg_q]