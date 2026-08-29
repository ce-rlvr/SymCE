import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import sympy.ntheory

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def get_elements(G):
    if hasattr(G, 'elements'):
        return list(G.elements)
    elif hasattr(G, 'generate'):
        return list(G.generate())
    else:
        return list(G)

def get_center(G):
    if hasattr(G, 'center'):
        c = G.center()
        if isinstance(c, list):
            if len(c) == 0:
                return PermutationGroup([G.identity])
            return PermutationGroup(c)
        return c
    else:
        elements = get_elements(G)
        c = []
        for g in elements:
            if all(g * h == h * g for h in elements):
                c.append(g)
        return PermutationGroup(c)

def get_derived_subgroup(G):
    if hasattr(G, 'derived_subgroup'):
        return G.derived_subgroup()
    else:
        elements = get_elements(G)
        commutators = []
        for g in elements:
            for h in elements:
                commutators.append(g * h * ~g * ~h)
        return PermutationGroup(commutators)

def is_semisimple(G):
    elements = get_elements(G)
    if not elements:
        return False
        
    is_ab = True
    for i in range(len(elements)):
        for j in range(i + 1, len(elements)):
            if elements[i] * elements[j] != elements[j] * elements[i]:
                is_ab = False
                break
        if not is_ab:
            break

    if is_ab:
        exp = 1
        for g in elements:
            exp = sympy.lcm(exp, g.order())
        for p in sympy.ntheory.primefactors(exp):
            if exp % (p**2) == 0:
                return False
        return True

    Z = get_center(G)
    D = get_derived_subgroup(G)
    
    if Z.order() * D.order() != len(elements):
        return False
        
    exp = 1
    for g in get_elements(Z):
        exp = sympy.lcm(exp, g.order())
    for p in sympy.ntheory.primefactors(exp):
        if exp % (p**2) == 0:
            return False
            
    if D.order() > 1:
        DD = get_derived_subgroup(D)
        if DD.order() != D.order():
            return False
        ZD = get_center(D)
        if ZD.order() > 1:
            return False
            
    return True

def apply_alpha(alpha, g):
    if isinstance(alpha, dict):
        return alpha[g]
    else:
        return alpha(g)

def is_automorphism(G, alpha):
    elements = get_elements(G)
    mapped_elements = []
    for g in elements:
        ag = apply_alpha(alpha, g)
        if ag not in elements:
            return False
        mapped_elements.append(ag)
        
    if len(set(mapped_elements)) != len(elements):
        return False
        
    for g in elements:
        for h in elements:
            ag = apply_alpha(alpha, g)
            ah = apply_alpha(alpha, h)
            agh = apply_alpha(alpha, g * h)
            if agh != ag * ah:
                return False
    return True

def is_central_automorphism(G, alpha):
    elements = get_elements(G)
    Z_elements = get_elements(get_center(G))
    for g in elements:
        ag = apply_alpha(alpha, g)
        val = (~g) * ag
        if val not in Z_elements:
            return False
    return True

def is_not_identity(G, alpha):
    elements = get_elements(G)
    for g in elements:
        if apply_alpha(alpha, g) != g:
            return True
    return False

def conditions(witness):
    if isinstance(witness, tuple) and len(witness) == 2:
        G, alpha = witness
    elif isinstance(witness, dict):
        G = witness.get('G')
        alpha = witness.get('alpha')
    else:
        G = getattr(witness, 'G', None)
        alpha = getattr(witness, 'alpha', None)
        
    if G is None or alpha is None:
        return [False, False, False, False]
        
    try:
        h1 = is_semisimple(G)
    except Exception:
        h1 = False
        
    try:
        h2 = is_automorphism(G, alpha)
    except Exception:
        h2 = False
        
    try:
        h3 = is_central_automorphism(G, alpha)
    except Exception:
        h3 = False
        
    try:
        neg_q = is_not_identity(G, alpha)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a semisimple group",
    "H_2: alpha is an automorphism of G",
    "H_3: For all elements g in G, the element g^{-1}*alpha(g) belongs to the center of G",
    "¬Q: The automorphism alpha is not the identity automorphism on G"
]

N_HYP = 3
NEG_Q_INDEX = 3