import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

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
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            X = witness.get('X')
            k = witness.get('k')
        else:
            G, X, k = witness[:3]
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: X is a set with at least two elements
    try:
        h2 = isinstance(X, (set, frozenset, list, tuple)) and len(X) >= 2 and all(isinstance(x, int) and x >= 0 for x in X)
        X_set = set(X)
    except Exception:
        h2 = False

    # H_3: k is an integer strictly greater than 1
    try:
        h3 = isinstance(k, int) and k > 1
    except Exception:
        h3 = False

    # ¬Q: Conclusion fails (LHS != RHS)
    try:
        def get_stabilizer(Grp, x):
            if x >= Grp.degree:
                return Grp
            return Grp.stabilizer(x)

        def is_k_transitive(Grp, subset, m):
            if len(subset) < m:
                return False
            m_tuples = set(itertools.permutations(subset, m))
            if not m_tuples:
                return True
            
            t0 = next(iter(m_tuples))
            orbit = set([t0])
            queue = [t0]
            
            found_count = 1 if t0 in m_tuples else 0
            target_count = len(m_tuples)
            
            if found_count == target_count:
                return True
                
            while queue:
                curr = queue.pop(0)
                for g in Grp.generators:
                    nxt = tuple(g(x) for x in curr)
                    if nxt not in orbit:
                        orbit.add(nxt)
                        queue.append(nxt)
                        if nxt in m_tuples:
                            found_count += 1
                            if found_count == target_count:
                                return True
            return False

        # LHS: G acts k-transitively on X
        lhs = is_k_transitive(G, X_set, k)
        
        # RHS: G acts transitively on X AND for any x in X, G_x acts (k-1)-transitively on X \ {x}
        rhs_transitive = is_k_transitive(G, X_set, 1)
        rhs_stabilizers = True
        if rhs_transitive:
            for x in X_set:
                Gx = get_stabilizer(G, x)
                if not is_k_transitive(Gx, X_set - {x}, k - 1):
                    rhs_stabilizers = False
                    break
        rhs = rhs_transitive and rhs_stabilizers

        neg_q = (lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a set with at least two elements",
    "H_3: k is an integer strictly greater than 1",
    "¬Q: G acts k-transitively on X iff G acts transitively on X and for any x in X, G_x acts (k-1)-transitively on X \\ {x} is FALSE"
]

N_HYP = 3
NEG_Q_INDEX = 3