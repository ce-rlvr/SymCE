from sympy import Matrix, eye, zeros, Rational, Integer, Symbol, gcd
from sympy.abc import x, y, z
import itertools

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 1",
    "H_2: A is an invertible matrix in GL_n(R)",
    "H_3: j is a fixed column index such that 1 <= j <= n",
    "¬Q: The sum of the principal ideals is not equal to R"
]

N_HYP = 3
NEG_Q_INDEX = 3

def parse_witness(witness):
    if isinstance(witness, tuple):
        if len(witness) == 3:
            A, k, j = witness
            if hasattr(A, 'as_explicit'):
                A = A.as_explicit()
            elif isinstance(A, list):
                A = Matrix(A)
            return A, k, j
        elif len(witness) == 2:
            A, j = witness
            if hasattr(A, 'blocks'):
                k = A.blocks[0,0].shape[0]
                A = A.as_explicit()
                return A, k, j
            else:
                if isinstance(A, list):
                    A = Matrix(A)
                return A, 1, j
    return None, None, None

def determine_ring(A):
    has_sym = False
    has_rat = False
    for e in A:
        if hasattr(e, 'free_symbols') and e.free_symbols:
            has_sym = True
        if getattr(e, 'is_Rational', False) and not getattr(e, 'is_Integer', False):
            has_rat = True
        if getattr(e, 'is_Float', False):
            has_rat = True
            
    if has_sym:
        return 'Qx' if has_rat else 'Zx'
    else:
        return 'Q' if has_rat else 'Z'

def is_unit(val, ring_type):
    try:
        if val == 0:
            return False
        if ring_type == 'Z':
            return abs(val) == 1
        elif ring_type == 'Q':
            return True
        elif ring_type == 'Zx':
            if hasattr(val, 'free_symbols') and val.free_symbols:
                return False
            return abs(val) == 1
        elif ring_type == 'Qx':
            if hasattr(val, 'free_symbols') and val.free_symbols:
                return False
            return True
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        A, k, j = parse_witness(witness)
        if A is None:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        ring_type = determine_ring(A)
    except Exception:
        ring_type = 'Q'

    # H_1: n is an integer strictly greater than 1
    try:
        n = A.shape[0] // k
        h1 = (n > 1) and (A.shape[0] % k == 0) and (A.shape[0] == A.shape[1])
    except Exception:
        h1 = False

    # H_2: A is an invertible matrix in GL_n(R)
    try:
        h2 = False
        if A.shape[0] == A.shape[1]:
            det = A.det()
            if is_unit(det, ring_type):
                h2 = True
    except Exception:
        h2 = False

    # H_3: j is a fixed column index such that 1 <= j <= n
    try:
        h3 = isinstance(j, int) and (1 <= j <= n)
    except Exception:
        h3 = False

    # ¬Q: The sum of the principal ideals is not equal to R
    # For a non-commutative ring represented by k x k blocks, the right ideal generated
    # by the block column is R iff the horizontal concatenation of the blocks has a right inverse,
    # which over a commutative center means the GCD of its k x k minors is a unit.
    try:
        neg_q = False
        if h1 and h3:
            blocks = []
            for i in range(n):
                block = A[i*k : (i+1)*k, (j-1)*k : j*k]
                blocks.append(block)
            M = Matrix.hstack(*blocks)
            
            cols = M.shape[1]
            minors = []
            for combo in itertools.combinations(range(cols), k):
                subM = M[:, combo]
                minors.append(subM.det())
                
            if not minors:
                neg_q = True
            else:
                g = minors[0]
                for m in minors[1:]:
                    g = gcd(g, m)
                    
                if not is_unit(g, ring_type):
                    neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]