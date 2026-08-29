import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
import math

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

def is_internal_direct_product(G, H, K):
    try:
        G_elems = list(G.elements)
        H_elems = list(H.elements)
        K_elems = list(K.elements)
        
        # Check if H and K are subgroups of G
        for h in H_elems:
            if h not in G_elems: return False
        for k in K_elems:
            if k not in G_elems: return False
            
        # Check if H and K are normal in G
        for g in G.generators:
            for h in H.generators:
                if (g * h * ~g) not in H_elems: return False
        for g in G.generators:
            for k in K.generators:
                if (g * k * ~g) not in K_elems: return False
                
        # Check if G = HK and H intersect K = {1}
        # Since H and K are subgroups, |HK| = |H||K| / |H \cap K| <= |G|
        # Thus |H||K| == |G| implies |H \cap K| = 1 and HK = G.
        if H.order() * K.order() != G.order():
            return False
            
        return True
    except Exception:
        return False

def is_semisimple(G):
    """
    A finite group is semisimple (completely reducible) iff it is a direct product of simple groups.
    This is equivalent to G being a direct product of its perfect derived subgroup and its center,
    where the center has a square-free exponent.
    """
    try:
        if G.is_abelian:
            exponent = 1
            for g in G.elements:
                exponent = sympy.lcm(exponent, g.order())
            for p in sympy.primefactors(exponent):
                if exponent % (p**2) == 0:
                    return False
            return True
        else:
            G_prime = G.derived_subgroup()
            if G_prime.order() == 1:
                return False
            if G_prime.derived_subgroup().order() != G_prime.order():
                return False
            
            if hasattr(G_prime, 'center'):
                Z_prime = G_prime.center()
            else:
                center_gens = [g for g in G_prime.elements if all(g * x == x * g for x in G_prime.generators)]
                Z_prime = PermutationGroup(center_gens) if center_gens else PermutationGroup([G_prime.identity])
                
            if Z_prime.order() != 1:
                return False
                
            if hasattr(G, 'center'):
                Z = G.center()
            else:
                center_gens = [g for g in G.elements if all(g * x == x * g for x in G.generators)]
                Z = PermutationGroup(center_gens) if center_gens else PermutationGroup([G.identity])
                
            exponent = 1
            for g in Z.elements:
                exponent = sympy.lcm(exponent, g.order())
            for p in sympy.primefactors(exponent):
                if exponent % (p**2) == 0:
                    return False
                    
            return is_internal_direct_product(G, G_prime, Z)
    except Exception:
        return False

def conditions(witness):
    try:
        if not isinstance(witness, tuple) or len(witness) != 3:
            return [False, False, False, False]
        G, H, K = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: G is a finite semisimple group
    try:
        h1 = is_semisimple(G)
    except Exception:
        h1 = False
        
    # H_2: G is the internal direct product of H and K
    try:
        h2 = is_internal_direct_product(G, H, K)
    except Exception:
        h2 = False
        
    # H_3: H is a solvable group
    try:
        h3 = bool(H.is_solvable)
    except Exception:
        h3 = False
        
    # ¬Q: H is not the trivial subgroup or K is not equal to G
    try:
        h_trivial = (H.order() == 1)
        k_equals_g = (K.order() == G.order())
        neg_q = not (h_trivial and k_equals_g)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite semisimple group",
    "H_2: G is the internal direct product of H and K",
    "H_3: H is a solvable group",
    "¬Q: H is not the trivial subgroup or K is not equal to G"
]

N_HYP = 3
NEG_Q_INDEX = 3