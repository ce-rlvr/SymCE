import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)
from sympy.combinatorics.permutations import Permutation

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (G, H, phi_map, S)
    where:
      - G, H are SymPy PermutationGroup objects.
      - phi_map is a dict or callable mapping elements of G to elements of H.
      - S is a subset (iterable) of elements of G.
    """
    try:
        G, H, phi_map, S = witness
    except Exception:
        return [False, False]
        
    if isinstance(phi_map, dict):
        phi = lambda x: phi_map.get(x, None)
    else:
        phi = phi_map

    # H_1: phi: G -> H is a group homomorphism
    try:
        h1_ok = True
        G_elements = list(G.elements)
        H_elements = list(H.elements)
        
        # Check if phi maps G into H
        for g in G_elements:
            val = phi(g)
            if val not in H_elements:
                h1_ok = False
                break
                
        # Check the homomorphism property: phi(x * y) == phi(x) * phi(y)
        if h1_ok:
            for x in G_elements:
                for y in G_elements:
                    if phi(x * y) != phi(x) * phi(y):
                        h1_ok = False
                        break
                if not h1_ok:
                    break
    except Exception:
        h1_ok = False

    # ¬Q: The restriction phi|_S is not a group homomorphism or its kernel is not ker(phi) \cap S.
    # The conclusion holds if and only if S is a subgroup of G.
    # If S is a subgroup, phi|_S is a homomorphism and its kernel is exactly ker(phi) \cap S.
    # If S is not a subgroup, S is not a group under the inherited operation, so phi|_S cannot be a group homomorphism.
    try:
        S_list = list(S)
        is_subset = all(s in G_elements for s in S_list)
        
        if not is_subset:
            is_subgroup = False
        else:
            is_subgroup = True
            if len(S_list) == 0:
                is_subgroup = False
            else:
                id_G = G.identity
                if id_G not in S_list:
                    is_subgroup = False
                else:
                    for x in S_list:
                        if x**-1 not in S_list:
                            is_subgroup = False
                            break
                        for y in S_list:
                            if x * y not in S_list:
                                is_subgroup = False
                                break
                        if not is_subgroup:
                            break
                            
        neg_q_ok = not is_subgroup
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: phi: G -> H is a group homomorphism",
    "¬Q: The restriction phi|_S is not a group homomorphism or its kernel is not ker(phi) cap S"
]

N_HYP = 1
NEG_Q_INDEX = 1