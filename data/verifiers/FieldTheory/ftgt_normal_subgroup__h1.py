import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([
    Permutation([[0, 1], [2, 3]]),
    Permutation([[0, 2], [1, 3]])
])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = PermutationGroup([Permutation()])

def conditions(witness) -> list[bool]:
    """
    Expects witness to be a tuple (Omega, U, W) of SymPy PermutationGroups.
    This models the Galois correspondence for a normal closure N of K/F:
      - Omega = Gal(N/F)
      - U = Gal(N/K)
      - W = Gal(N/E)
    """
    try:
        if not (isinstance(witness, tuple) and len(witness) == 3):
            return [False, False, False]
        Omega, U, W = witness
        if not (hasattr(Omega, 'generators') and hasattr(U, 'generators') and hasattr(W, 'generators')):
            return [False, False, False]
    except Exception:
        return [False, False, False]

    def is_subgroup(sub, group):
        try:
            return all(group.contains(g) for g in sub.generators)
        except Exception:
            return False

    def normalizes(g, group):
        try:
            return all(group.contains(g * u * ~g) for u in group.generators)
        except Exception:
            return False

    # H_1: G = Gal(K/F) is the Galois group of K over F
    # In our model, K is an extension of F, so U <= Omega.
    try:
        h1 = is_subgroup(U, Omega)
    except Exception:
        h1 = False

    # H_2: E is an intermediate field corresponding to H <= G
    # This means U <= W <= Omega, and W corresponds to a subgroup of G = N_Omega(U)/U.
    # So W must be a subgroup of N_Omega(U), which means W normalizes U.
    try:
        h2 = is_subgroup(U, W) and is_subgroup(W, Omega) and all(normalizes(w, U) for w in W.generators)
    except Exception:
        h2 = False

    # neg_Q: E/F is normal iff H is normal in G
    # E/F is normal iff W is normal in Omega.
    # H is normal in G iff W is normal in N_Omega(U).
    try:
        W_normal_in_Omega = all(normalizes(g, W) for g in Omega.generators)
        
        try:
            elements = list(Omega.generate())
        except Exception:
            elements = list(Omega.elements)
            
        N_Omega_U = [g for g in elements if normalizes(g, U)]
        W_normal_in_N = all(W.contains(n * w * ~n) for n in N_Omega_U for w in W.generators)
        
        neg_q = (W_normal_in_Omega != W_normal_in_N)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G = Gal(K/F) is the Galois group of K over F",
    "H_2: E is an intermediate field corresponding to the subgroup H <= G",
    "¬Q: E/F is normal is not equivalent to H being a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2