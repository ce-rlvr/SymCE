import math
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness objects
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

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness should provide the space X and two distance functions/dictionaries d1 and d2.
    """
    try:
        if isinstance(witness, dict):
            X = witness['X']
            d1 = witness['d1']
            d2 = witness['d2']
        else:
            X, d1, d2 = witness
        X = list(X)
    except Exception:
        return [False, False, False]

    def get_d(d, x, y):
        if callable(d):
            return d(x, y)
        elif isinstance(d, dict):
            if (x, y) in d:
                return d[(x, y)]
            elif (y, x) in d:
                return d[(y, x)]
            else:
                raise ValueError("Distance not found")
        else:
            return d[x][y]

    def check_exists_c(A, B):
        min_c = -float('inf')
        max_c = float('inf')
        for x in X:
            for y in X:
                try:
                    a = float(get_d(A, x, y))
                    b = float(get_d(B, x, y))
                except Exception:
                    return False
                
                if abs(a) < 1e-9:
                    if b < -1e-9:
                        return False
                elif a > 0:
                    max_c = min(max_c, b / a)
                else:
                    min_c = max(min_c, b / a)
        return max_c > 0 and min_c <= max_c + 1e-9

    # Hypothesis 1: There exists c > 0 such that c * d1(x, y) <= d2(x, y)
    try:
        h1 = check_exists_c(d1, d2)
    except Exception:
        h1 = False

    # Hypothesis 2: There exists C > 0 such that d2(x, y) <= C * d1(x, y)
    try:
        h2 = check_exists_c(d2, d1)
    except Exception:
        h2 = False

    def is_metric(d):
        for x in X:
            for y in X:
                try:
                    val = float(get_d(d, x, y))
                except Exception:
                    return False
                if val < -1e-9:
                    return False
                if abs(val) < 1e-9:
                    if x != y:
                        return False
                else:
                    if x == y:
                        return False
                try:
                    val_yx = float(get_d(d, y, x))
                except Exception:
                    return False
                if abs(val - val_yx) > 1e-9:
                    return False
                for z in X:
                    try:
                        val_xz = float(get_d(d, x, z))
                        val_yz = float(get_d(d, y, z))
                    except Exception:
                        return False
                    if val_xz > val + val_yz + 1e-9:
                        return False
        return True

    def same_topology(d1, d2):
        def get_Nx(d):
            # For finite spaces, the topology is uniquely determined by the minimal open neighborhood N(x) of each point.
            balls = []
            for center in X:
                distances = set()
                for y in X:
                    distances.add(float(get_d(d, center, y)))
                for r in distances:
                    ball = frozenset(y for y in X if float(get_d(d, center, y)) <= r)
                    balls.append(ball)
            
            Nx = {}
            for x in X:
                nx = frozenset(X)
                for ball in balls:
                    if x in ball:
                        nx = nx.intersection(ball)
                Nx[x] = nx
            return Nx

        try:
            return get_Nx(d1) == get_Nx(d2)
        except Exception:
            return False

    # Conclusion: The metrics d1 and d2 induce the same topology on X
    # This implies d1 and d2 MUST be valid metrics, and they must induce the same topology.
    try:
        q = is_metric(d1) and is_metric(d2) and same_topology(d1, d2)
        neg_q = not q
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: There exists c > 0 such that c * d1(x, y) <= d2(x, y) for all x, y in X",
    "H_2: There exists C > 0 such that d2(x, y) <= C * d1(x, y) for all x, y in X",
    "¬Q: The metrics d1 and d2 do not induce the same topology on X (or are not valid metrics)"
]

N_HYP = 2
NEG_Q_INDEX = 2