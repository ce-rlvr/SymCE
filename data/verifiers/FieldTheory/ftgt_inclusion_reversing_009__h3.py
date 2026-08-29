import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]])])
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
    Checks if the witness is a valid counterexample.
    The witness should provide the Galois group G, and subgroups E1, E2, H1, H2.
    Note: Intermediate fields E_1 and E_2 are represented by their corresponding 
    Galois groups Gal(K/E_1) and Gal(K/E_2) as subgroups of G.
    Thus, E_1 \subseteq E_2 is equivalent to Gal(K/E_2) \subseteq Gal(K/E_1).
    """
    G = E1 = E2 = H1 = H2 = None
    if isinstance(witness, dict):
        G = witness.get('G')
        E1 = witness.get('E1')
        E2 = witness.get('E2')
        H1 = witness.get('H1')
        H2 = witness.get('H2')
    elif isinstance(witness, (list, tuple)) and len(witness) == 5:
        G, E1, E2, H1, H2 = witness
    else:
        try:
            G = witness.G
            E1 = witness.E1
            E2 = witness.E2
            H1 = witness.H1
            H2 = witness.H2
        except AttributeError:
            pass

    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    try:
        h2_ok = (isinstance(E1, PermutationGroup) and 
                 isinstance(E2, PermutationGroup) and 
                 E1.is_subgroup(G) and 
                 E2.is_subgroup(G))
    except Exception:
        h2_ok = False

    try:
        # E1 \subseteq E2 iff Gal(K/E2) \subseteq Gal(K/E1)
        e1_sub_e2 = E2.is_subgroup(E1)
        h2_sub_h1 = H2.is_subgroup(H1)
        neg_q_ok = bool(e1_sub_e2 != h2_sub_h1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: K/F is a finite Galois extension with Galois group G",
    "H_2: E_1 and E_2 are intermediate fields between F and K",
    "¬Q: The equivalence (E_1 \\subseteq E_2 iff H_2 \\subseteq H_1) fails"
]

N_HYP = 2
NEG_Q_INDEX = 2