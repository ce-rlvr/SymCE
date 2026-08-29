import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def get_subgroups_containing(N_elements, H_elements):
    """Finds all subgroups of N that contain H."""
    subgroups = {frozenset(H_elements)}
    added = True
    while added:
        added = False
        new_subgroups = set()
        for S in subgroups:
            for g in N_elements:
                if g not in S:
                    # Generate the closure of S U {g}
                    closure = set(S)
                    closure.add(g)
                    queue = [g]
                    while queue:
                        x = queue.pop()
                        new_elements = set()
                        for y in closure:
                            xy = x * y
                            if xy not in closure:
                                new_elements.add(xy)
                            yx = y * x
                            if yx not in closure:
                                new_elements.add(yx)
                        for elem in new_elements:
                            closure.add(elem)
                            queue.append(elem)
                    
                    H_new = frozenset(closure)
                    if H_new not in subgroups and H_new not in new_subgroups:
                        new_subgroups.add(H_new)
                        added = True
        if added:
            subgroups.update(new_subgroups)
    return subgroups

def get_maximal_subgroups(subgroups, N_elements):
    """Filters the subgroups to find the maximal proper subgroups of N."""
    N_fs = frozenset(N_elements)
    proper_subgroups = [S for S in subgroups if S != N_fs]
    maximal = []
    for S in proper_subgroups:
        is_maximal = True
        for K in proper_subgroups:
            if S != K and S.issubset(K):
                is_maximal = False
                break
        if is_maximal:
            maximal.append(S)
    return maximal

def get_P(N_elements, H_elements):
    """
    Computes P, the preimage in N of the Frattini subgroup of N/H.
    This is the intersection of all maximal subgroups of N containing H.
    """
    N_fs = frozenset(N_elements)
    H_fs = frozenset(H_elements)
    if N_fs == H_fs:
        return H_fs
    subgroups = get_subgroups_containing(N_elements, H_elements)
    maximal = get_maximal_subgroups(subgroups, N_elements)
    if not maximal:
        return H_fs
    P = set(maximal[0])
    for M in maximal[1:]:
        P = P.intersection(M)
    return frozenset(P)

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness is expected to be a tuple (Gamma, H) representing the Galois 
    correspondence of the field extension L/K within a normal closure N/K, 
    where Gamma = Gal(N/K) and H = Gal(N/L).
    """
    try:
        Gamma, H = witness
        
        # H_1: Gamma and H are valid permutation groups representing the extension
        h1 = isinstance(Gamma, PermutationGroup) and isinstance(H, PermutationGroup)
        
        # H_2: H is a subgroup of Gamma
        if h1:
            Gamma_elements = frozenset(Gamma.elements)
            h2 = all(g in Gamma_elements for g in H.generators)
        else:
            h2 = False
            
        neg_q = False
        if h1 and h2:
            H_elements = frozenset(H.elements)
            
            # Compute N_Gamma(H), the normalizer of H in Gamma
            N_elements = []
            for g in Gamma_elements:
                normalizes = True
                for h in H.generators:
                    if (g * h * ~g) not in H_elements:
                        normalizes = False
                        break
                if normalizes:
                    N_elements.append(g)
            
            # Compute P, the subgroup corresponding to the fixed field L^{\Phi(G)}
            P_elements = get_P(N_elements, H_elements)
            
            # Check if P is a normal subgroup of Gamma
            # If P is NOT normal, then L^{\Phi(G)} is NOT a normal extension of K
            P_is_normal = True
            for g in Gamma_elements:
                for p in P_elements:
                    if (g * p * ~g) not in P_elements:
                        P_is_normal = False
                        break
                if not P_is_normal:
                    break
            
            neg_q = not P_is_normal
            
    except Exception:
        h1 = False
        h2 = False
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G = Gal(L/K) is the Galois group of the extension (Gamma and H are valid groups)",
    "H_2: Phi(G) is the Frattini subgroup of G (H is a valid subgroup of Gamma)",
    "¬Q: The fixed field L^Phi(G) is NOT a normal extension of K"
]

N_HYP = 2
NEG_Q_INDEX = 2