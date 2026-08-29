import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.free_groups import FreeGroup
from sympy.combinatorics.fp_groups import FpGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

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

def conditions(witness) -> list[bool]:
    try:
        F = witness['F']
        G = witness['G']
        H = witness['H']
        alpha = witness['alpha']
        beta = witness['beta']
    except Exception:
        return [False, False, False, False]

    # H_1: F is a free group
    try:
        h1 = isinstance(F, FreeGroup) or (isinstance(F, FpGroup) and len(F.relators) == 0)
    except Exception:
        h1 = False

    # H_2: G and H are groups
    try:
        h2 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h2 = False

    # H_3: alpha is a surjective group homomorphism
    try:
        G_elems = list(G.generate())
        H_elems = list(H.generate())
        
        is_hom = True
        im_alpha = set()
        for g1 in G_elems:
            a_g1 = alpha(g1) if callable(alpha) else alpha[g1]
            im_alpha.add(a_g1)
            for g2 in G_elems:
                a_g2 = alpha(g2) if callable(alpha) else alpha[g2]
                a_g1g2 = alpha(g1 * g2) if callable(alpha) else alpha[g1 * g2]
                if a_g1g2 != a_g1 * a_g2:
                    is_hom = False
                    break
            if not is_hom:
                break
        
        is_surj = (im_alpha == set(H_elems))
        h3 = is_hom and is_surj
    except Exception:
        h3 = False

    # ¬Q: There is no group homomorphism gamma: F -> G such that alpha(gamma(x)) = beta(x)
    try:
        F_gens = F.generators
        G_elems = list(G.generate())
        G_id = G.identity
        
        gamma_exists = False
        for assignment in itertools.product(G_elems, repeat=len(F_gens)):
            gamma_gens = {str(g): val for g, val in zip(F_gens, assignment)}
            
            works = True
            for w, expected_h in beta.items():
                res = G_id
                for gen, exp in w.array_form:
                    g = gamma_gens[str(gen)]
                    if exp < 0:
                        g = g**-1
                    for _ in range(abs(exp)):
                        res = res * g
                
                a_res = alpha(res) if callable(alpha) else alpha[res]
                if a_res != expected_h:
                    works = False
                    break
            
            if works:
                gamma_exists = True
                break
        
        neg_q = not gamma_exists
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "H_2: G and H are groups",
    "H_3: alpha is a surjective group homomorphism",
    "¬Q: There is no group homomorphism gamma: F -> G such that alpha(gamma(x)) = beta(x)"
]

N_HYP = 3
NEG_Q_INDEX = 3