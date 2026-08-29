import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness expressions
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Given a witness (G1, G2, N1, N2), checks the hypotheses and the negated conclusion.
    Returns [H1_ok, H2_ok, neg_Q_ok].
    """
    try:
        G1, G2, N1, N2 = witness
    except Exception:
        return [False, False, False]

    def is_normal_subgroup(H, G):
        if not isinstance(H, PermutationGroup) or not isinstance(G, PermutationGroup):
            return False
        # Check if H is a subgroup of G
        for h in H.generators:
            if h not in G:
                return False
        # Check normality: g * h * ~g in H for all generators
        for h in H.generators:
            for g in G.generators:
                if (g * h * ~g) not in H:
                    return False
        return True

    # H_1: N1 is a normal subgroup of G1
    try:
        h1 = is_normal_subgroup(N1, G1)
    except Exception:
        h1 = False

    # H_2: N2 is a normal subgroup of G2
    try:
        h2 = is_normal_subgroup(N2, G2)
    except Exception:
        h2 = False

    # ¬Q: The quotient group (G1 × G2) / (N1 × N2) is NOT isomorphic to (G1 / N1) × (G2 / N2)
    try:
        if not (isinstance(G1, PermutationGroup) and isinstance(G2, PermutationGroup) and 
                isinstance(N1, PermutationGroup) and isinstance(N2, PermutationGroup)):
            neg_q = False
        elif G1.order() * G2.order() > 4000:
            # Prevent timeout for excessively large groups
            neg_q = False
        else:
            def direct_product(H1, H2, d1, d2):
                gens = []
                for g in H1.generators:
                    arr = list(g.array_form)
                    if len(arr) < d1:
                        arr += list(range(len(arr), d1))
                    arr += list(range(d1, d1 + d2))
                    gens.append(Permutation(arr))
                for g in H2.generators:
                    arr = list(g.array_form)
                    if len(arr) < d2:
                        arr += list(range(len(arr), d2))
                    p = list(range(d1)) + [x + d1 for x in arr]
                    gens.append(Permutation(p))
                    
                if not gens:
                    return PermutationGroup([Permutation(d1 + d2 - 1)])
                return PermutationGroup(gens)

            def get_quotient_group(G, N):
                G_els = list(G.generate())
                N_els = set(N.generate())
                
                cosets = []
                coset_reps = []
                seen = set()
                for e in G_els:
                    if e in seen:
                        continue
                    coset = frozenset({e * n for n in N_els})
                    cosets.append(coset)
                    coset_reps.append(e)
                    seen.update(coset)
                    
                n_cosets = len(cosets)
                el_to_coset = {}
                for i, c in enumerate(cosets):
                    for el in c:
                        el_to_coset[el] = i
                        
                perms = []
                for i in range(n_cosets):
                    p = [el_to_coset[coset_reps[i] * coset_reps[j]] for j in range(n_cosets)]
                    perms.append(Permutation(p))
                    
                if not perms:
                    return PermutationGroup([Permutation(0)])
                return PermutationGroup(perms)

            d1 = max(1, G1.degree, N1.degree)
            d2 = max(1, G2.degree, N2.degree)
            
            G1xG2 = direct_product(G1, G2, d1, d2)
            N1xN2 = direct_product(N1, N2, d1, d2)
            
            Q_LHS = get_quotient_group(G1xG2, N1xN2)
            
            Q1 = get_quotient_group(G1, N1)
            Q2 = get_quotient_group(G2, N2)
            
            qd1 = max(1, Q1.degree)
            qd2 = max(1, Q2.degree)
            Q_RHS = direct_product(Q1, Q2, qd1, qd2)
            
            if Q_LHS.order() == Q_RHS.order() == 1:
                q_holds = True
            else:
                q_holds = Q_LHS.is_isomorphic(Q_RHS)
                
            neg_q = not q_holds
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: N1 is a normal subgroup of G1",
    "H_2: N2 is a normal subgroup of G2",
    "¬Q: The quotient group (G1 × G2) / (N1 × N2) is not isomorphic to (G1 / N1) × (G2 / N2)"
]

N_HYP = 2
NEG_Q_INDEX = 2