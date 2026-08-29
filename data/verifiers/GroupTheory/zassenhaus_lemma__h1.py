import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    Returns a list of booleans: [H_1_ok, H_2_ok, H_3_ok, neg_Q_ok]
    """
    try:
        G, A, B, A_star, B_star = witness
    except Exception:
        return [False, False, False, False]

    def is_subgroup(H, G):
        try:
            return H.is_subgroup(G)
        except Exception:
            return False

    def is_normal_subgroup(N, G):
        try:
            if not is_subgroup(N, G):
                return False
            return N.is_normal(G)
        except Exception:
            return False

    def subgroup_product(H, K):
        try:
            elements = set()
            for h in H.elements:
                for k in K.elements:
                    elements.add(h * k)
            
            elements_list = list(elements)
            for a in elements_list:
                for b in elements_list:
                    if a * b not in elements:
                        return None
            return PermutationGroup(elements_list)
        except Exception:
            return None

    def subgroup_intersection(H, K):
        try:
            elements = set(H.elements).intersection(set(K.elements))
            return PermutationGroup(list(elements))
        except Exception:
            return None

    try:
        h1_ok = is_subgroup(A, G) and is_subgroup(B, G)
    except Exception:
        h1_ok = False

    try:
        h2_ok = is_normal_subgroup(A_star, A)
    except Exception:
        h2_ok = False

    try:
        h3_ok = is_normal_subgroup(B_star, B)
    except Exception:
        h3_ok = False

    try:
        A_cap_B = subgroup_intersection(A, B)
        A_cap_B_star = subgroup_intersection(A, B_star)
        A_star_cap_B = subgroup_intersection(A_star, B)

        L_num = subgroup_product(A_cap_B, A_star)
        L_den = subgroup_product(A_cap_B_star, A_star)
        
        R_num = subgroup_product(A_cap_B, B_star)
        R_den = subgroup_product(A_star_cap_B, B_star)

        if L_num is None or L_den is None or R_num is None or R_den is None:
            neg_q_ok = True
        else:
            L_den_normal = is_normal_subgroup(L_den, L_num)
            R_den_normal = is_normal_subgroup(R_den, R_num)
            
            if not L_den_normal or not R_den_normal:
                neg_q_ok = True
            else:
                def get_cosets(G_grp, N_grp):
                    cosets = []
                    N_elements = set(N_grp.elements)
                    for g in G_grp.elements:
                        found = False
                        for c in cosets:
                            if g in c:
                                found = True
                                break
                        if not found:
                            new_coset = set(g * n for n in N_elements)
                            cosets.append(new_coset)
                    return cosets
                
                def is_isomorphic_quotients(G1, N1, G2, N2):
                    cosets1 = get_cosets(G1, N1)
                    cosets2 = get_cosets(G2, N2)
                    if len(cosets1) != len(cosets2):
                        return False
                    
                    N1_elements = set(N1.elements)
                    N2_elements = set(N2.elements)
                    
                    def get_orders(cosets, N_elements):
                        orders = []
                        for c in cosets:
                            g = next(iter(c))
                            k = 1
                            curr = g
                            while curr not in N_elements:
                                curr = curr * g
                                k += 1
                            orders.append(k)
                        return sorted(orders)
                    
                    return get_orders(cosets1, N1_elements) == get_orders(cosets2, N2_elements)

                neg_q_ok = not is_isomorphic_quotients(L_num, L_den, R_num, R_den)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: A and B are subgroups of G",
    "H_2: A^* is a normal subgroup of A",
    "H_3: B^* is a normal subgroup of B",
    "¬Q: (A \\cap B)A^* / (A \\cap B^*)A^* \\not\\cong (A \\cap B)B^* / (A^* \\cap B)B^*"
]

N_HYP = 3
NEG_Q_INDEX = 3