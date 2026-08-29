import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
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

def conditions(witness):
    try:
        G, p, P = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: Let p be a prime dividing the order of G
    try:
        h1 = isprime(p) and (G.order() % p == 0)
    except Exception:
        h1 = False
        
    # H_2: Let P be a Sylow p-subgroup of G
    try:
        if not isinstance(P, PermutationGroup) or not P.is_subgroup(G):
            h2 = False
        else:
            order_G = G.order()
            order_P = P.order()
            k = 0
            temp = order_G
            while temp % p == 0 and p > 1:
                k += 1
                temp //= p
            h2 = (order_P == p**k)
    except Exception:
        h2 = False
        
    # H_3: Assume P is the unique Sylow p-subgroup of G for the prime p
    try:
        if h2:
            # By Sylow's theorems, a Sylow p-subgroup is unique iff it is normal in G
            h3 = P.is_normal(G)
        else:
            h3 = False
    except Exception:
        h3 = False
        
    # ¬Q: P is NOT a characteristic subgroup of G
    try:
        if not isinstance(P, PermutationGroup) or not P.is_subgroup(G):
            neg_q = True
        elif not P.is_normal(G):
            # Every characteristic subgroup must be normal (invariant under inner automorphisms)
            neg_q = True
        else:
            is_char = True
            gens = G.generators
            
            # Group elements by order to optimize finding valid generator images
            elements_by_order = {}
            for x in G.elements:
                o = x.order()
                if o not in elements_by_order:
                    elements_by_order[o] = []
                elements_by_order[o].append(x)
                
            candidates = []
            for g in gens:
                order = g.order()
                candidates.append(elements_by_order.get(order, []))
            
            try:
                from sympy.combinatorics.homomorphisms import homomorphism
                for images in itertools.product(*candidates):
                    try:
                        H_img = PermutationGroup(*images)
                        if H_img.order() != G.order():
                            continue
                        phi = homomorphism(G, G, gens, images)
                        if phi is not None:
                            # Check if the automorphism maps P to itself
                            for p_gen in P.generators:
                                if phi(p_gen) not in P:
                                    is_char = False
                                    break
                    except Exception:
                        pass
                    if not is_char:
                        break
            except ImportError:
                # Fallback if homomorphism cannot be imported
                if h2 and h3:
                    is_char = True
                else:
                    is_char = P.is_normal(G)
                    
            neg_q = not is_char
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is a prime dividing the order of G",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: P is the unique Sylow p-subgroup of G for the prime p",
    "¬Q: P is not a characteristic subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3