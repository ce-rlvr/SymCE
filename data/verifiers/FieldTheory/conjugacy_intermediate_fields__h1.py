import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for standard algebra objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    """
    Verifier for the conjecture:
    M_1 and M_2 are conjugate extensions over K iff H_1 and H_2 are conjugate subgroups in G.
    
    The witness is expected to be a dictionary or a 4-tuple (Gamma, U, V1, V2) representing 
    the field extensions via the Galois correspondence:
      - Gamma represents the Galois group of a Galois closure E/K.
      - U represents the subgroup fixing L, so L = E^U.
      - V1, V2 represent the subgroups fixing M_1, M_2, so M_i = E^{V_i}.
    """
    try:
        if isinstance(witness, dict):
            Gamma = witness.get('Gamma')
            U = witness.get('U')
            V1 = witness.get('V1')
            V2 = witness.get('V2')
        else:
            witness_list = list(witness)
            if len(witness_list) != 4:
                return [False, False, False, False]
            Gamma, U, V1, V2 = witness_list
            
        if any(x is None for x in (Gamma, U, V1, V2)):
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    def is_subgroup(sub, super_grp):
        try:
            return all(g in super_grp for g in sub.generators)
        except Exception:
            return False

    # H_1: G is the Galois group of L/K
    # In our model, L/K corresponds to U <= Gamma.
    try:
        h1 = (isinstance(Gamma, PermutationGroup) and 
              isinstance(U, PermutationGroup) and 
              is_subgroup(U, Gamma))
    except Exception:
        h1 = False

    # H_2: M_1 and M_2 are intermediate fields between K and L
    # Corresponds to U <= V_i <= Gamma
    try:
        h2 = (isinstance(V1, PermutationGroup) and 
              isinstance(V2, PermutationGroup) and 
              is_subgroup(U, V1) and is_subgroup(V1, Gamma) and 
              is_subgroup(U, V2) and is_subgroup(V2, Gamma))
    except Exception:
        h2 = False

    # H_3: H_1 and H_2 are the subgroups of G fixing M_1 and M_2 respectively
    # This is structurally guaranteed by the Galois correspondence model if H1 and H2 hold.
    try:
        h3 = h1 and h2
    except Exception:
        h3 = False

    # Conclusion: M_1 and M_2 are conjugate over K iff H_1 and H_2 are conjugate in G
    try:
        def normalizer(G_grp, sub_grp):
            sub_gens = sub_grp.generators
            norm_elements = []
            for g in G_grp.generate():
                g_inv = g**-1
                if all((g * u * g_inv) in sub_grp for u in sub_gens):
                    norm_elements.append(g)
            return PermutationGroup(norm_elements)

        def group_intersection(A, B):
            elements = []
            for g in A.generate():
                if g in B:
                    elements.append(g)
            return PermutationGroup(elements)

        def are_conjugate_subgroups(K, A, B):
            try:
                order_A = A.order()
            except TypeError:
                order_A = A.order
            try:
                order_B = B.order()
            except TypeError:
                order_B = B.order
                
            if order_A != order_B:
                return False
                
            A_gens = A.generators
            for k in K.generate():
                k_inv = k**-1
                if all((k * g * k_inv) in B for g in A_gens):
                    return True
            return False

        # M_1 and M_2 are conjugate over K iff V_1 and V_2 are conjugate in Gamma
        m1_m2_conj = are_conjugate_subgroups(Gamma, V1, V2)
        
        # G = N_Gamma(U) / U. We represent G by N_Gamma(U).
        # H_i = (V_i \cap N_Gamma(U)) / U. We represent H_i by V_i \cap N_Gamma(U).
        N_U = normalizer(Gamma, U)
        H1_pre = group_intersection(V1, N_U)
        H2_pre = group_intersection(V2, N_U)
        
        # H_1 and H_2 are conjugate in G iff their preimages are conjugate in N_Gamma(U)
        h1_h2_conj = are_conjugate_subgroups(N_U, H1_pre, H2_pre)
        
        # The conclusion fails if the equivalence does not hold
        neg_q = (m1_m2_conj != h1_h2_conj)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is the Galois group of L/K",
    "H_2: M_1 and M_2 are intermediate fields between K and L",
    "H_3: H_1 and H_2 are the subgroups of G fixing M_1 and M_2 respectively",
    "¬Q: The equivalence (M_1, M_2 conjugate over K iff H_1, H_2 conjugate in G) fails"
]

N_HYP = 3
NEG_Q_INDEX = 3