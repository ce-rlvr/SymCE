import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings for the witness expression
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]])])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = PermutationGroup([Permutation(0)])

def is_normal(G, H):
    if not H.is_subgroup(G):
        return False
    for g in G.generators:
        for h in H.generators:
            if (g * h * ~g) not in H:
                return False
    return True

def set_product(H1, H2):
    if H1.order() > 1000 or H2.order() > 1000:
        raise ValueError("Group too large")
    elems1 = list(H1.generate())
    elems2 = list(H2.generate())
    prod = set()
    for h1 in elems1:
        for h2 in elems2:
            prod.add(h1 * h2)
    return prod

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) < 3:
            return [False, False, False]
            
        # Group theory witness (via Galois correspondence)
        # A tuple of PermutationGroups: (H_K, H_L, H_E)
        if hasattr(witness[0], 'generators') or (len(witness) == 4 and hasattr(witness[1], 'generators')):
            if len(witness) == 4 and hasattr(witness[1], 'generators'):
                G, H_K, H_L, H_E = witness[:4]
            else:
                H_K, H_L, H_E = witness[:3]
                
            # H1: L/K is a finite Galois extension
            # In Galois correspondence, this means H_L is a normal subgroup of H_K
            h1 = is_normal(H_K, H_L)
            
            # H2: L and E are subfields of a common overfield
            # Any two permutation groups can be embedded in a common symmetric group
            h2 = True
            
            # neg_Q: L and E are NOT linearly disjoint over L \cap E
            # In Galois correspondence, this means H_L H_E != H_E H_L
            neg_q = set_product(H_L, H_E) != set_product(H_E, H_L)
            
            return [bool(h1), bool(h2), bool(neg_q)]
            
        # Field theory witness fallback
        # A tuple of algebraic generators: (K_gen, L_gen, E_gen)
        else:
            from sympy import minpoly, primitive_element, QQ
            from sympy.abc import x
            
            K_gen, L_gen, E_gen = witness[:3]
            
            def deg(gens):
                gens = [g for g in gens if not getattr(g, 'is_rational', False)]
                if not gens: return 1
                if len(gens) == 1: return minpoly(gens[0], x, domain=QQ).degree()
                _, poly = primitive_element(gens, x, domain=QQ)
                return poly.degree()
            
            deg_K = deg([K_gen])
            deg_L = deg([L_gen])
            deg_E = deg([E_gen])
            deg_LK = deg([L_gen, K_gen])
            deg_LE = deg([L_gen, E_gen])
            
            deg_L_over_K = deg_L // deg_K
            
            # H1: L/K is a finite Galois extension
            # We confidently know it's Galois if K <= L and the relative degree is 1 or 2
            h1 = (deg_LK == deg_L) and (deg_L % deg_K == 0) and (deg_L_over_K in (1, 2))
            
            # H2: L and E are subfields of a common overfield
            h2 = True
            
            # neg_Q: L and E are NOT linearly disjoint over L \cap E
            # If they are linearly disjoint, X = [L \cap E : Q] must be an integer.
            # If X is not an integer, they are definitely not linearly disjoint.
            X = (deg_L * deg_E) / deg_LE
            neg_q = (X != int(X))
            
            return [bool(h1), bool(h2), bool(neg_q)]
            
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: L/K is a finite Galois extension",
    "H_2: L and E are subfields of a common overfield",
    "¬Q: L and E are NOT linearly disjoint over L \\cap E"
]

N_HYP = 2
NEG_Q_INDEX = 2