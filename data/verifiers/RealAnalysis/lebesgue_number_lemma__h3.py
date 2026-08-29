import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (X, d, U) where:
      - X is a finite iterable representing the metric space elements.
      - d is a callable representing the distance function d(x, y).
      - U is an iterable of iterables representing the collection of sets \mathcal{U}.
    """
    try:
        X_orig, d, U = witness
        X = list(X_orig)
        U_list = [set(u_i) for u_i in U]
    except Exception:
        return [False, False, False]
    
    # H1: (X, d) is a metric space
    try:
        h1 = True
        for x in X:
            for y in X:
                dist = float(d(x, y))
                if dist < 0:
                    h1 = False
                if (dist < 1e-9) != (x == y):
                    h1 = False
                if abs(dist - float(d(y, x))) > 1e-9:
                    h1 = False
                for z in X:
                    if float(d(x, z)) > dist + float(d(y, z)) + 1e-7:
                        h1 = False
    except Exception:
        h1 = False

    # H2: X is compact
    try:
        # In our discrete representation, any finite collection is a compact space
        h2 = isinstance(X_orig, (list, set, tuple))
    except Exception:
        h2 = False

    # neg_Q: Conclusion fails
    # Conclusion: There exists a \delta > 0 such that for every x \in X, 
    # the open ball B(x, \delta) is contained in at least one set U \in \mathcal{U}.
    try:
        distances = set()
        for x in X:
            for y in X:
                distances.add(float(d(x, y)))
        
        test_deltas = []
        if len(distances) > 1:
            sorted_d = sorted(list(distances))
            # Test a delta smaller than the minimum non-zero distance
            test_deltas.append(sorted_d[1] / 2.0)
            # Test deltas slightly larger than each possible distance
            for dist in sorted_d:
                test_deltas.append(dist + 1e-5)
        else:
            test_deltas.append(1.0)
            
        conclusion_holds = False
        for delta in test_deltas:
            delta_works = True
            for x in X:
                ball = {y for y in X if float(d(x, y)) < delta}
                contained = False
                for u_i in U_list:
                    if ball.issubset(u_i):
                        contained = True
                        break
                if not contained:
                    delta_works = False
                    break
            if delta_works:
                conclusion_holds = True
                break
                
        neg_q = not conclusion_holds
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: (X, d) is a metric space",
    "H_2: X is compact",
    "¬Q: There is no delta > 0 such that for every x in X, the open ball B(x, delta) is contained in at least one set U in U"
]

N_HYP = 2
NEG_Q_INDEX = 2