import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_elements(G):
    if hasattr(G, 'elements'):
        if callable(G.elements):
            return G.elements()
        return G.elements
    elif hasattr(G, 'generate'):
        return list(G.generate())
    else:
        return list(G)

def invert(g):
    try:
        return ~g
    except Exception:
        return g**-1

def normalizes(G, g, H):
    if hasattr(G, 'normalizes'):
        return G.normalizes(g, H)
    
    try:
        inv_g = invert(g)
    except Exception:
        return False

    if hasattr(H, 'generators') and hasattr(H, 'contains'):
        for h in H.generators:
            try:
                conj = g * h * inv_g
            except Exception:
                return False
            if not H.contains(conj):
                return False
        return True
    
    try:
        H_elements = list(get_elements(H))
    except Exception:
        return False
        
    for h in H_elements:
        try:
            conj = g * h * inv_g
        except Exception:
            return False
        if conj not in H_elements:
            return False
    return True

def check_is_subgroup(H, G):
    if hasattr(H, 'is_subgroup'):
        return H.is_subgroup(G)
    if hasattr(G, 'has_subgroup'):
        return G.has_subgroup(H)
    try:
        for h in get_elements(H):
            if hasattr(G, 'contains'):
                if not G.contains(h):
                    return False
            else:
                if h not in get_elements(G):
                    return False
        return True
    except Exception:
        return False

def get_normalizer(G, H):
    if hasattr(G, 'normalizer'):
        return G.normalizer(H)
    
    norm_elements = []
    for g in get_elements(G):
        if normalizes(G, g, H):
            norm_elements.append(g)
            
    if hasattr(G, 'subgroup_from_elements'):
        return G.subgroup_from_elements(norm_elements)
    
    try:
        return PermutationGroup(norm_elements)
    except Exception:
        return norm_elements

def check_equality(H1, H2):
    if hasattr(H1, 'is_subgroup') and hasattr(H2, 'is_subgroup'):
        try:
            return H1.is_subgroup(H2) and H2.is_subgroup(H1)
        except Exception:
            pass
    try:
        e1 = list(get_elements(H1))
        e2 = list(get_elements(H2))
        try:
            return set(e1) == set(e2)
        except TypeError:
            if len(e1) != len(e2):
                return False
            for x in e1:
                if x not in e2:
                    return False
            return True
    except Exception:
        return H1 == H2

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 4:
            G, p, P, N_G_P = witness
        elif len(witness) == 3:
            G, p, P = witness
            N_G_P = get_normalizer(G, P)
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: p is a prime number
    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False

    # H2: P is a Sylow p-subgroup of G
    try:
        if hasattr(G, 'is_sylow'):
            h2 = bool(G.is_sylow(P, p))
        else:
            is_sub = check_is_subgroup(P, G)
            order_G = G.order() if hasattr(G, 'order') else len(list(get_elements(G)))
            order_P = P.order() if hasattr(P, 'order') else len(list(get_elements(P)))
            if order_G == sympy.oo:
                h2 = False
            else:
                k = 0
                while order_G % (p**(k+1)) == 0:
                    k += 1
                h2 = is_sub and (order_P == p**k)
    except Exception:
        h2 = False

    # H3: N_G(P) is the normalizer of P in G
    try:
        if hasattr(G, 'normalizer'):
            expected_N = G.normalizer(P)
            h3 = check_equality(N_G_P, expected_N)
        else:
            is_sub_N = check_is_subgroup(N_G_P, G)
            
            normalizes_P = True
            for g in get_elements(N_G_P):
                if not normalizes(G, g, P):
                    normalizes_P = False
                    break
            
            maximal = True
            if normalizes_P:
                for g in get_elements(G):
                    if normalizes(G, g, P):
                        if hasattr(N_G_P, 'contains'):
                            if not N_G_P.contains(g):
                                maximal = False
                                break
                        else:
                            if g not in get_elements(N_G_P):
                                maximal = False
                                break
            h3 = is_sub_N and normalizes_P and maximal
    except Exception:
        h3 = False

    # NegQ: The normalizer of N_G(P) in G is NOT equal to N_G(P)
    try:
        NN = get_normalizer(G, N_G_P)
        neg_q = not check_equality(NN, N_G_P)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: N_G(P) is the normalizer of P in G",
    "¬Q: The normalizer of N_G(P) in G is not equal to N_G(P)"
]

N_HYP = 3
NEG_Q_INDEX = 3