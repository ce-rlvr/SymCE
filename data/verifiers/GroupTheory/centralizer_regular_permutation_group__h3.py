import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    # H_1: Let n be a positive integer (implies witness is a permutation group with degree > 0)
    try:
        h1_ok = isinstance(witness, PermutationGroup) and witness.degree > 0
    except Exception:
        h1_ok = False

    # H_2: Let S_n be the symmetric group on n letters
    try:
        h2_ok = h1_ok
    except Exception:
        h2_ok = False

    # ¬Q: The centralizer of G in S_n is not a regular permutation group or is not isomorphic to G
    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            n = witness.degree
            # Limit n to prevent timeout on extremely large groups
            if n > 8:
                neg_q_ok = False
            else:
                Sn = SymmetricGroup(n)
                gens = witness.generators
                
                centralizer_elements = []
                for p in Sn.generate():
                    # Check if p commutes with all generators of G
                    if all(p * g == g * p for g in gens):
                        centralizer_elements.append(p)
                
                C = PermutationGroup(centralizer_elements)
                
                # A permutation group is regular if it is transitive and its order equals its degree.
                # In this context, the degree is n. Transitivity on n points means the orbit of 0 has length n.
                is_regular = (C.order() == n) and (len(C.orbit(0)) == n)
                
                # Check if C is isomorphic to G
                is_iso = C.is_isomorphic(witness)
                
                neg_q_ok = not (is_regular and is_iso)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: Let n be a positive integer",
    "H_2: Let S_n be the symmetric group on n letters",
    "¬Q: The centralizer of G in S_n is not a regular permutation group or is not isomorphic to G"
]

N_HYP = 2
NEG_Q_INDEX = 2