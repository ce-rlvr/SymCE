import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0,1)(2,3), Permutation(0,2)(1,3)])
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
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: C_G(H) is the centralizer of H in G",
    "¬Q: The quotient group N_G(H)/C_G(H) is NOT isomorphic to a subgroup of Aut(H)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, H = witness
                C = None
            elif len(witness) == 3:
                G, H, C = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: H is a subgroup of G
    try:
        if isinstance(H, PermutationGroup) and h1_ok:
            h2_ok = all(G.contains(g) for g in H.generators)
        else:
            h2_ok = False
    except Exception:
        h2_ok = False

    # H_3: C_G(H) is the centralizer of H in G
    try:
        if h1_ok and h2_ok:
            C_gens = []
            for g in G.elements:
                if all(g * h == h * g for h in H.generators):
                    C_gens.append(g)
            C_actual = PermutationGroup(C_gens) if C_gens else PermutationGroup([G.identity])
            
            if C is not None:
                h3_ok = isinstance(C, PermutationGroup) and C.order() == C_actual.order() and all(C_actual.contains(g) for g in C.generators)
            else:
                C = C_actual
                h3_ok = True
        else:
            h3_ok = False
    except Exception:
        h3_ok = False

    # ¬Q: N_G(H)/C_G(H) is NOT isomorphic to a subgroup of Aut(H)
    try:
        if h1_ok and h2_ok and h3_ok:
            # Compute N_G(H)
            N_gens = []
            for g in G.elements:
                g_inv = ~g
                if all(H.contains(g * h * g_inv) for h in H.generators):
                    N_gens.append(g)
            N = PermutationGroup(N_gens) if N_gens else PermutationGroup([G.identity])
            
            # Check if C is normal in N
            c_normal = True
            for c in C.generators:
                for n in N.generators:
                    if not C.contains(n * c * ~n):
                        c_normal = False
                        break
                if not c_normal:
                    break
            
            if not c_normal:
                neg_q = True
            else:
                # The map n -> (h -> n*h*n^-1) is a homomorphism N -> Aut(H) with kernel C.
                # By the First Isomorphism Theorem, N/C is isomorphic to the image, which is a subgroup of Aut(H).
                # We verify that the kernel of this homomorphism is exactly C.
                kernel_is_C = True
                for n in N.elements:
                    is_in_ker = all(n * h == h * n for h in H.generators)
                    is_in_C = C.contains(n)
                    if is_in_ker != is_in_C:
                        kernel_is_C = False
                        break
                
                if not kernel_is_C:
                    neg_q = True
                else:
                    neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, neg_q]