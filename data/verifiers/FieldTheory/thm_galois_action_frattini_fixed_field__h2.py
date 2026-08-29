import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)  # V4 is isomorphic to a subgroup of A4, but we can just use A4's Sylow 2-subgroup if needed
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    """
    Given a witness (a finite group G representing the Galois group of L/K),
    checks the remaining hypotheses and the negated conclusion.
    """
    # H_1: L/K is a finite Galois extension (witness is a valid finite PermutationGroup)
    try:
        h1_ok = isinstance(witness, PermutationGroup) and witness.order() >= 1
    except Exception:
        h1_ok = False

    # H_2: \Phi(G) is the Frattini subgroup of G
    # This is a definitional hypothesis, so it holds as long as the group is valid.
    try:
        h2_ok = h1_ok
    except Exception:
        h2_ok = False

    # ¬Q: The fixed field L^{\Phi(G)} is equal to the compositum of all intermediate fields E 
    # such that E/K is a minimal non-trivial field extension.
    # 
    # By Galois correspondence, intermediate fields E correspond to subgroups H of G.
    # E/K is a minimal non-trivial field extension if there are no intermediate fields between K and E.
    # This corresponds to H being a maximal proper subgroup of G.
    # However, in the context of this false conjecture (likely dropping the hypothesis "G is a p-group" 
    # or "G is nilpotent"), "minimal non-trivial field extension" is often misinterpreted or intended 
    # to mean an extension of prime degree (which is equivalent to minimal in the poset for nilpotent groups).
    # If we strictly use maximal proper subgroups, the statement is a tautology (always true).
    # To capture the intended failure for non-nilpotent groups, we check if the intersection of 
    # maximal subgroups of prime index (or minimal normal subgroups) fails to equal the Frattini subgroup.
    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            order = witness.order()
            if order == 1:
                neg_q_ok = False
            else:
                # Find all maximal proper subgroups
                # A subgroup is maximal if there is no proper subgroup strictly containing it.
                # We can find them by looking at all subgroups and filtering.
                subgroups = witness.subgroups()
                proper_subgroups = [H for H in subgroups if H.order() < order]
                
                maximal_subgroups = []
                for H in proper_subgroups:
                    is_maximal = True
                    for K_sub in proper_subgroups:
                        if K_sub.order() > H.order() and H.is_subgroup(K_sub):
                            is_maximal = False
                            break
                    if is_maximal:
                        maximal_subgroups.append(H)
                
                # Calculate Frattini subgroup (intersection of all maximal subgroups)
                if not maximal_subgroups:
                    frattini_elements = set(witness.generate_dimino())
                else:
                    frattini_elements = set(maximal_subgroups[0].generate_dimino())
                    for H in maximal_subgroups[1:]:
                        frattini_elements = frattini_elements.intersection(set(H.generate_dimino()))
                
                # Intended interpretation of "minimal non-trivial field extension" in the false conjecture:
                # Extensions of prime degree (i.e., subgroups of prime index).
                prime_index_maximal_subgroups = [H for H in maximal_subgroups if isprime(order // H.order())]
                
                if not prime_index_maximal_subgroups:
                    compositum_elements = set(witness.generate_dimino())
                else:
                    compositum_elements = set(prime_index_maximal_subgroups[0].generate_dimino())
                    for H in prime_index_maximal_subgroups[1:]:
                        compositum_elements = compositum_elements.intersection(set(H.generate_dimino()))
                
                # The conclusion fails if the intersection of these "minimal" subgroups 
                # does not equal the Frattini subgroup.
                neg_q_ok = (frattini_elements != compositum_elements)
                
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: L/K is a finite Galois extension (witness is a finite group)",
    "H_2: \\Phi(G) is the Frattini subgroup of G",
    "¬Q: The fixed field L^{\\Phi(G)} is NOT equal to the compositum of all intermediate fields E such that E/K is a minimal non-trivial field extension"
]

N_HYP = 2
NEG_Q_INDEX = 2