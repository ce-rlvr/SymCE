import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy import eye, zeros

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def pad_permutation(p, degree):
    """Pads or truncates a permutation to match the target degree."""
    if p.size < degree:
        return Permutation(p.array_form + list(range(p.size, degree)))
    elif p.size > degree:
        # Ensure all elements beyond the target degree are fixed
        for i in range(degree, p.size):
            if p(i) != i:
                return None
        return Permutation(p.array_form[:degree])
    return p

def normalize_group(G, degree):
    """Returns a new PermutationGroup with all generators padded to the target degree."""
    try:
        if G.degree == degree:
            return G
        new_gens = []
        for g in G.generators:
            p = pad_permutation(g, degree)
            if p is None:
                return None
            new_gens.append(p)
        return PermutationGroup(new_gens)
    except Exception:
        return None

def is_normal_subgroup(G, H):
    """Checks if H is a normal subgroup of G."""
    try:
        if hasattr(H, 'is_normal'):
            return H.is_normal(G)
    except Exception:
        pass
    try:
        if not H.is_subgroup(G):
            return False
        for g in G.generators:
            for h in H.generators:
                if not H.contains(g * h * g**-1):
                    return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness is expected to be a tuple (E, G) where:
      - E is the Galois group of the finite Galois extension L/K.
      - G is a subgroup of E (representing a group acting on L).
    """
    try:
        E, G = witness
    except Exception:
        return [False, False, False]
    
    # H_1: L/K is a finite Galois extension (represented by Galois group E)
    try:
        h1 = isinstance(E, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: G is a group acting on L (represented by subgroup G <= E)
    try:
        if not isinstance(G, PermutationGroup):
            h2 = False
        else:
            degree = max(E.degree, G.degree)
            E_norm = normalize_group(E, degree)
            G_norm = normalize_group(G, degree)
            if E_norm is None or G_norm is None:
                h2 = False
            else:
                h2 = G_norm.is_subgroup(E_norm)
    except Exception:
        h2 = False
        
    # ¬Q: The fixed field L^{Z(G)} is NOT a normal extension of K.
    # By Galois theory, this is true iff Z(G) is NOT a normal subgroup of E.
    try:
        if not h2:
            neg_q = False
        else:
            Z_G = G_norm.center()
            neg_q = not is_normal_subgroup(E_norm, Z_G)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: L/K is a finite Galois extension (represented by Galois group E)",
    "H_2: G is a group acting on L (represented by subgroup G <= E)",
    "¬Q: The fixed field L^{Z(G)} is not a normal extension of K (Z(G) is not normal in E)"
]

N_HYP = 2
NEG_Q_INDEX = 2