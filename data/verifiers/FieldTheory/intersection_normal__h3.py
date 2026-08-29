import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: K_1/F is a normal extension",
    "H_2: K_2/F is a normal extension",
    "¬Q: The intersection K_1 \\cap K_2 is not a normal extension of F"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_subgroup(H, G):
    try:
        return all(g in G for g in H.generators)
    except Exception:
        return False

def is_normal(H, G):
    try:
        if not is_subgroup(H, G):
            return False
        for h in H.generators:
            for g in G.generators:
                conj = g * h * (~g)
                if conj not in H:
                    return False
                conj_inv = (~g) * h * g
                if conj_inv not in H:
                    return False
        return True
    except Exception:
        return False

def conditions(witness):
    """
    Witness is expected to be a tuple (G, H1, H2) where:
    - G is a PermutationGroup representing the Galois group of a common overfield E/F.
    - H1, H2 are PermutationGroups representing the subgroups corresponding to K1, K2.
    By Galois correspondence:
    - K_i/F is normal iff H_i is a normal subgroup of G.
    - K_1 \\cap K_2 corresponds to the join <H1, H2>.
    """
    try:
        G, H1, H2 = witness
        
        if isinstance(G, list): 
            G = PermutationGroup(G)
        if isinstance(H1, list): 
            H1 = PermutationGroup(H1)
        if isinstance(H2, list): 
            H2 = PermutationGroup(H2)
        
        if not (isinstance(G, PermutationGroup) and 
                isinstance(H1, PermutationGroup) and 
                isinstance(H2, PermutationGroup)):
            return [False, False, False]
            
        h1_ok = is_normal(H1, G)
        h2_ok = is_normal(H2, G)
        
        # K_1 \cap K_2 corresponds to the join of H1 and H2
        gens = list(H1.generators) + list(H2.generators)
        if not gens:
            return [False, False, False]
            
        H_join = PermutationGroup(gens)
        
        # Conclusion: K_1 \cap K_2 is normal in F
        # corresponds to H_join being normal in G
        q_ok = is_normal(H_join, G)
        
        neg_q_ok = not q_ok
        
        return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]
    except Exception:
        return [False, False, False]