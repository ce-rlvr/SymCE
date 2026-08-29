import sympy
from sympy import Matrix, zeros
import itertools

# Top-level setup: named object bindings that the witness expression may reference.
# We provide standard groups and matrices as requested.
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def is_over_Z(M):
    """Check if all elements of the matrix are integers."""
    return all(val.is_integer for val in M)

def is_pure(M):
    """
    Check if the column space of M is a pure submodule.
    Over Z, this is true iff the GCD of all r x r minors is 1, where r is the rank of M.
    """
    r = M.rank()
    if r == 0:
        return True
        
    minors = []
    for row_indices in itertools.combinations(range(M.rows), r):
        for col_indices in itertools.combinations(range(M.cols), r):
            submat = M.extract(row_indices, col_indices)
            minors.append(submat.det())
            
    g_val = minors[0]
    for m in minors[1:]:
        g_val = sympy.gcd(g_val, m)
        if g_val == 1 or g_val == -1:
            return True
            
    if is_over_Z(M):
        try:
            return int(g_val) in [1, -1]
        except TypeError:
            return False
    else:
        return g_val != 0

def conditions(witness) -> list[bool]:
    """
    Given a witness (f, g) representing the linear maps U -> V -> W,
    checks if it satisfies the hypotheses and fails the conclusion.
    """
    try:
        # The witness should be a tuple of two sympy Matrices (f, g)
        if not (isinstance(witness, tuple) and len(witness) == 2):
            return [False, False, False]
            
        f, g = witness
        
        # H1: U, V, W are vector spaces over a field F
        # We verify that f and g are valid matrices that can be composed.
        h1_ok = isinstance(f, Matrix) and isinstance(g, Matrix) and (f.rows == g.cols)
        if not h1_ok:
            return [False, False, False]
            
        # H2: The sequence U -> V -> W is exact at V, meaning Im(f) = ker(g)
        # Over a ring (like Z), this requires:
        # 1. g * f == 0
        # 2. Rank condition: rank(f) + rank(g) == dim(V)
        # 3. Im(f) is a pure submodule (so it equals the pure submodule ker(g))
        try:
            is_complex = (g * f == zeros(g.rows, f.cols))
            rank_condition = (f.rank() + g.rank() == f.rows)
            pure_f = is_pure(f)
            h2_ok = bool(is_complex and rank_condition and pure_f)
        except Exception:
            h2_ok = False
            
        # neg_Q: The dual sequence W* -> V* -> U* is NOT exact at V*
        # Exactness of the dual sequence Im(g*) = ker(f*) requires Im(g*) to be pure.
        # Since g* = g.T, and the minors of g.T are the same as g, this is equivalent to Im(g) being pure.
        # The conclusion FAILS if Im(g) is NOT pure.
        try:
            neg_q_ok = not is_pure(g)
        except Exception:
            neg_q_ok = False
            
        return [h1_ok, h2_ok, neg_q_ok]
        
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: U, V, W are vector spaces over a field F (represented by valid composable matrices)",
    "H_2: The sequence is exact at V, meaning Im(f) = ker(g)",
    "¬Q: The dual sequence is NOT exact at V*, meaning Im(g*) != ker(f*)"
]

N_HYP = 2
NEG_Q_INDEX = 2