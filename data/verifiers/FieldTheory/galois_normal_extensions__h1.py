import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Standard algebra objects
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample.
    The witness should represent the fields F, E, K via their corresponding 
    subgroups in the Galois group of the normal closure (G_L, V, U).
    F corresponds to G_L (the largest group)
    E corresponds to V (intermediate group)
    K corresponds to U (the smallest group)
    """
    try:
        # Extract groups
        if isinstance(witness, dict) and 'F' in witness and 'E' in witness and 'K' in witness:
            G_L = witness['F']
            V = witness['E']
            U = witness['K']
        elif isinstance(witness, dict) and 'G_L' in witness and 'V' in witness and 'U' in witness:
            G_L = witness['G_L']
            V = witness['V']
            U = witness['U']
        else:
            groups = [g for g in (witness.values() if isinstance(witness, dict) else witness) if hasattr(g, 'generate_dimino')]
            if len(groups) < 3:
                return [False, False, False]
            
            # Take the first 3 groups and sort them by size descending: G_L (F), V (E), U (K)
            first_three = sorted(groups[:3], key=lambda g: len(list(g.generate_dimino())), reverse=True)
            G_L, V, U = first_three[0], first_three[1], first_three[2]
            
        if not all(hasattr(g, 'generate_dimino') for g in [G_L, V, U]):
            return [False, False, False]
            
        degree = G_L.degree
        
        def normalize_group(G, deg):
            elts = []
            for p in G.generate_dimino():
                a = p.array_form
                if len(a) < deg:
                    a = a + list(range(len(a), deg))
                elif len(a) > deg:
                    valid = True
                    for i in range(deg, len(a)):
                        if a[i] != i:
                            valid = False
                            break
                    if not valid:
                        raise ValueError("Permutation moves points beyond degree")
                    a = a[:deg]
                elts.append(Permutation(a))
            return PermutationGroup(elts)

        # Normalize all groups to the same degree to ensure safe element comparison
        V = normalize_group(V, degree)
        U = normalize_group(U, degree)
        G_L = normalize_group(G_L, degree)

        def get_elements(G):
            return list(G.generate_dimino())

        def is_subgroup(G, H):
            G_elts = get_elements(G)
            H_elts = get_elements(H)
            if len(H_elts) > len(G_elts):
                return False
            G_set = set(G_elts)
            return all(h in G_set for h in H_elts)

        def normalizer(G, U_sub):
            G_elts = get_elements(G)
            U_elts = get_elements(U_sub)
            U_set = set(U_elts)
            norm_elts = []
            for g in G_elts:
                if all((g * u * ~g) in U_set for u in U_elts):
                    norm_elts.append(g)
            return PermutationGroup(norm_elts)

        def is_normal_subgroup(G, N):
            if not is_subgroup(G, N):
                return False
            G_elts = get_elements(G)
            N_elts = get_elements(N)
            N_set = set(N_elts)
            for g in G_elts:
                for n in N_elts:
                    if (g * n * ~g) not in N_set:
                        return False
            return True

        # H_1: E is an intermediate field between F and K
        # In Galois correspondence: U <= V <= G_L
        h1_ok = bool(is_subgroup(G_L, V) and is_subgroup(V, U))
        
        # H_2: H is the subgroup Gal(K/E) of the Galois group Gal(K/F)
        # This is structurally true by our definition of the groups
        h2_ok = True
        
        # Conclusion: E is a normal extension of F iff H is a normal subgroup of Gal(K/F)
        # E normal over F <=> V normal in G_L
        E_normal_F = is_normal_subgroup(G_L, V)
        
        # H normal in Gal(K/F) <=> N_V(U) normal in N_{G_L}(U)
        N_G = normalizer(G_L, U)
        N_V = normalizer(V, U)
        H_normal_Gal = is_normal_subgroup(N_G, N_V)
        
        # We want the conclusion to FAIL
        neg_q_ok = bool(E_normal_F != H_normal_Gal)
        
        return [h1_ok, h2_ok, neg_q_ok]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: E is an intermediate field between F and K",
    "H_2: H is the subgroup Gal(K/E) of the Galois group Gal(K/F)",
    "¬Q: The equivalence (E is normal over F iff H is normal in Gal(K/F)) fails"
]

N_HYP = 2
NEG_Q_INDEX = 2