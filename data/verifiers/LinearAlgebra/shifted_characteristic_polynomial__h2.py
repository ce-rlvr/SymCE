import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
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

N_HYP = 3
NEG_Q_INDEX = 3

CONDITION_LABELS = [
    "H_1: A is an n x n matrix over a field F",
    "H_2: I is the n x n identity matrix",
    "H_3: p(x) is the characteristic polynomial of A",
    "¬Q: The characteristic polynomial of the matrix A - cI is not p(x+c)"
]

def conditions(witness):
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            c = witness.get('c')
            x = witness.get('x', sympy.Symbol('x'))
            I = witness.get('I')
            p = witness.get('p')
        elif isinstance(witness, tuple):
            if len(witness) == 5:
                A, c, I, p, x = witness
            elif len(witness) == 2:
                A, c = witness
                x = sympy.Symbol('x')
                I = None
                p = None
            else:
                return [False, False, False, False]
        else:
            A = getattr(witness, 'A', None)
            c = getattr(witness, 'c', None)
            x = getattr(witness, 'x', sympy.Symbol('x'))
            I = getattr(witness, 'I', None)
            p = getattr(witness, 'p', None)
            
        if A is None or c is None:
            return [False, False, False, False]

        if isinstance(A, (list, tuple)):
            A = sympy.Matrix(A)
        if isinstance(I, (list, tuple)):
            I = sympy.Matrix(I)
        if isinstance(c, (list, tuple)):
            c = sympy.Matrix(c)

        if I is None and isinstance(A, sympy.MatrixBase) and A.is_square:
            I = sympy.eye(A.shape[0])
        if p is None and isinstance(A, sympy.MatrixBase) and A.is_square:
            p = A.charpoly(x).as_expr()
            
    except Exception:
        return [False, False, False, False]

    # H1: A is an n \times n matrix
    try:
        h1 = isinstance(A, sympy.MatrixBase) and A.is_square
    except Exception:
        h1 = False

    # H2: I is the n \times n identity matrix
    try:
        h2 = isinstance(I, sympy.MatrixBase) and I == sympy.eye(A.shape[0])
    except Exception:
        h2 = False

    # H3: p(x) is the characteristic polynomial of A
    try:
        expected_p = A.charpoly(x).as_expr()
        h3 = bool(sympy.simplify(p - expected_p) == 0)
    except Exception:
        h3 = False

    # neg_Q: The characteristic polynomial of A - cI is NOT p(x+c)
    try:
        mat = A - c * I
        charpoly_mat = mat.charpoly(x).as_expr()
        p_x_plus_c = p.subs(x, x + c)
        
        diff = sympy.simplify(charpoly_mat - p_x_plus_c)
        if isinstance(diff, sympy.MatrixBase):
            neg_q = not diff.is_zero_matrix
        else:
            neg_q = bool(diff != 0)
    except Exception:
        # If evaluation fails (e.g., substituting a matrix into a scalar polynomial),
        # the conclusion is ill-formed and thus fails.
        neg_q = True

    return [h1, h2, h3, neg_q]