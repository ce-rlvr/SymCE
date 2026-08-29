import itertools
from sympy.combinatorics import PermutationGroup, Permutation, SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
from sympy import eye, zeros

# Standard algebra objects
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, X, action = witness
        else:
            G = witness.G
            X = witness.X
            action = witness.action
    except Exception:
        return [False, False, False]

    # H1: G is a group
    try:
        if hasattr(G, 'elements'):
            elements = list(G.elements)
            h1 = True
        elif hasattr(G, 'is_group') and G.is_group:
            elements = list(G)
            h1 = True
        else:
            # Fallback for custom group implementations
            elements = list(G)
            h1 = len(elements) > 0
    except Exception:
        h1 = False

    # H2: X is a set with |X| >= 2
    try:
        X_list = []
        for x in X:
            if x not in X_list:
                X_list.append(x)
        h2 = len(X_list) >= 2
    except Exception:
        h2 = False

    # neg_Q: The equivalence between 2-transitivity and (transitivity + stabilizer transitivity) fails
    try:
        if isinstance(action, dict):
            act = lambda g, x: action[(g, x)]
        else:
            act = action

        # LHS: G acts 2-transitively on X
        lhs = True
        for x1, x2 in itertools.permutations(X_list, 2):
            for y1, y2 in itertools.permutations(X_list, 2):
                found = False
                for g in elements:
                    if act(g, x1) == y1 and act(g, x2) == y2:
                        found = True
                        break
                if not found:
                    lhs = False
                    break
            if not lhs:
                break

        # RHS Part 1: G acts transitively on X
        rhs_part1 = True
        for x in X_list:
            for y in X_list:
                found = False
                for g in elements:
                    if act(g, x) == y:
                        found = True
                        break
                if not found:
                    rhs_part1 = False
                    break
            if not rhs_part1:
                break

        # RHS Part 2: For any x in X, the stabilizer G_x acts transitively on X \ {x}
        rhs_part2 = True
        for x in X_list:
            Gx = [g for g in elements if act(g, x) == x]
            X_minus_x = [y for y in X_list if y != x]
            for y in X_minus_x:
                for z in X_minus_x:
                    found = False
                    for g in Gx:
                        if act(g, y) == z:
                            found = True
                            break
                    if not found:
                        rhs_part2 = False
                        break
                if not rhs_part2:
                    break
            if not rhs_part2:
                break

        rhs = rhs_part1 and rhs_part2

        # The conjecture claims LHS == RHS. We want the negation (LHS != RHS).
        neg_q = (lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a set with |X| >= 2",
    "¬Q: The equivalence between 2-transitivity and (transitivity + stabilizer transitivity) fails"
]

N_HYP = 2
NEG_Q_INDEX = 2