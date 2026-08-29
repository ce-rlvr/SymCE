import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
from itertools import product

try:
    from sympy.combinatorics.homomorphisms import homomorphism
except ImportError:
    homomorphism = None

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_characteristic(G, P):
    if not P.is_subgroup(G):
        return False
    
    if homomorphism is None:
        # Fallback if homomorphism is unavailable; assume characteristic to avoid false positives
        return True
        
    gens = G.generators
    elements_by_order = {}
    for g in G.elements:
        g_order = g.order() if callable(g.order) else g.order
        elements_by_order.setdefault(g_order, []).append(g)
        
    possible_images = []
    for gen in gens:
        gen_order = gen.order() if callable(gen.order) else gen.order
        possible_images.append(elements_by_order.get(gen_order, []))
        
    for images in product(*possible_images):
        try:
            h = homomorphism(G, G, gens, images)
            if h is not None:
                inj = h.is_injective() if callable(h.is_injective) else h.is_injective
                surj = h.is_surjective() if callable(h.is_surjective) else h.is_surjective
                if inj and surj:
                    for p_gen in P.generators:
                        if h(p_gen) not in P:
                            return False
        except Exception:
            pass
    return True

def conditions(witness):
    try:
        G, p, P = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: G is a finite group
    try:
        h1 = bool(isinstance(G, PermutationGroup))
    except Exception:
        h1 = False
        
    # H2: p is a prime dividing the order of G
    try:
        order_G = G.order() if callable(G.order) else G.order
        h2 = bool(isprime(p) and order_G % p == 0)
    except Exception:
        h2 = False
        
    # H3: P is the unique Sylow p-subgroup of G for the prime p
    try:
        order_G = G.order() if callable(G.order) else G.order
        p_power = 1
        while order_G % (p_power * p) == 0:
            p_power *= p
            
        is_sub = P.is_subgroup(G)
        order_P = P.order() if callable(P.order) else P.order
        is_sylow = is_sub and order_P == p_power
        
        is_normal = True
        if is_sylow:
            for g in G.generators:
                for h in P.generators:
                    if (g * h * (~g)) not in P:
                        is_normal = False
                        break
                if not is_normal:
                    break
        h3 = bool(is_sylow and is_normal)
    except Exception:
        h3 = False
        
    # neg_Q: P is NOT a characteristic subgroup of G
    try:
        neg_q = bool(not is_characteristic(G, P))
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime dividing the order of G",
    "H_3: P is the unique Sylow p-subgroup of G for the prime p",
    "¬Q: P is not a characteristic subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3