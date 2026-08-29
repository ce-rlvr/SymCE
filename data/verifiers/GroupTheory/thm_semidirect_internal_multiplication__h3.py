import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (G, N, H, n1, n2, h1, h2)
    """
    try:
        if len(witness) != 7:
            return [False, False, False]
        G, N, H, n1, n2, h1, h2 = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is the internal semidirect product of a normal subgroup N and a subgroup H
    try:
        h1_ok = False
        if isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and isinstance(H, PermutationGroup):
            if N.is_subgroup(G) and H.is_subgroup(G) and N.is_normal(G):
                # Internal semidirect product requires trivial intersection and NH = G
                if N.intersect(H).order() == 1 and N.order() * H.order() == G.order():
                    h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: n_1, n_2 are elements of N
    # (We also verify h_1, h_2 are in G so the product expression is well-defined in G)
    try:
        h2_ok = (n1 in N) and (n2 in N) and (h1 in G) and (h2 in G)
    except Exception:
        h2_ok = False

    # ¬Q: The conclusion FAILS at the witness
    # Conclusion claims: (n1*h1)*(n2*h2) == (n1 * h1 * n2 * h1^-1) * (h1 * h2)
    # AND (n1 * h1 * n2 * h1^-1) in N
    # AND (h1 * h2) in H
    try:
        lhs = (n1 * h1) * (n2 * h2)
        
        part1 = n1 * h1 * n2 * (~h1)
        part2 = h1 * h2
        rhs = part1 * part2
        
        eq_holds = (lhs == rhs)
        part1_in_N = (part1 in N)
        part2_in_H = (part2 in H)
        
        q_ok = eq_holds and part1_in_N and part2_in_H
        neg_q_ok = not q_ok
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is the internal semidirect product of a normal subgroup N and a subgroup H",
    "H_2: n_1, n_2 are elements of N",
    "¬Q: The product formula fails or the components are not in N and H respectively"
]

N_HYP = 2
NEG_Q_INDEX = 2