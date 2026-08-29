import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

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
    """
    Check if the witness is a valid counterexample to the false conjecture:
    "Every normal (T_4) space with cardinality > 1 is uncountably infinite."
    (The dropped hypothesis was that the space is connected).
    """
    try:
        # Parse the witness into a set of points and a set of open sets.
        # A simple integer n can represent the discrete topology on n points.
        if isinstance(witness, int) and not isinstance(witness, bool):
            if witness < 0 or witness > 12:
                return [False, False, False]
            points = frozenset(range(witness))
            opens = set(frozenset(combo) for r in range(witness + 1) for combo in itertools.combinations(points, r))
        elif isinstance(witness, sympy.Set) and witness.is_FiniteSet:
            points = frozenset(witness)
            if len(points) > 12:
                return [False, False, False]
            opens = set(frozenset(combo) for r in range(len(points) + 1) for combo in itertools.combinations(points, r))
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            points_list = list(witness[0])
            if len(points_list) > 100:
                return [False, False, False]
            points = frozenset(points_list)
            opens = set(frozenset(o) for o in witness[1])
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: X is a normal (T_4) space
    def check_h1():
        try:
            # 1. Check if it is a valid topology
            if frozenset() not in opens or points not in opens:
                return False
            for a in opens:
                for b in opens:
                    if a.intersection(b) not in opens:
                        return False
                    if a.union(b) not in opens:
                        return False
            
            # 2. Check T_1 (every singleton is closed, so its complement is open)
            for p in points:
                if points - frozenset([p]) not in opens:
                    return False
            
            # 3. Check T_4 (disjoint closed sets can be separated by disjoint open sets)
            closed_sets = [points - o for o in opens]
            for A in closed_sets:
                for B in closed_sets:
                    if A.isdisjoint(B):
                        found = False
                        for U in opens:
                            if A.issubset(U):
                                for V in opens:
                                    if B.issubset(V) and U.isdisjoint(V):
                                        found = True
                                        break
                            if found:
                                break
                        if not found:
                            return False
            return True
        except Exception:
            return False

    h1_ok = check_h1()

    # H_2: The cardinality of X is strictly greater than 1
    try:
        h2_ok = len(points) > 1
    except Exception:
        h2_ok = False

    # ¬Q: The cardinality of X is NOT uncountably infinite
    try:
        # Since our parsed points form a finite frozenset, the space is finite.
        # A finite space is never uncountably infinite, so the conclusion fails.
        neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: X is a normal (T_4) space",
    "H_2: The cardinality of X is strictly greater than 1",
    "¬Q: The cardinality of X is not uncountably infinite"
]

N_HYP = 2
NEG_Q_INDEX = 2