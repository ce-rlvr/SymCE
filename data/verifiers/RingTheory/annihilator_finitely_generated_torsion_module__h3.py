import sympy
from sympy import ZZ, QQ, Matrix, eye, zeros, Symbol
from sympy.abc import x, y, z

class ModulePresentation:
    """
    Represents a finitely generated module M = R^n / im(A)
    where R is a commutative ring, and A is an n x m presentation matrix.
    """
    def __init__(self, ring, matrix):
        self.ring = ring
        self.matrix = Matrix(matrix)

# Standard algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: M is a finitely generated module over R",
    "¬Q: The annihilator ideal Ann_R(M) is zero"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    h1_ok = False
    h2_ok = False
    neg_q_ok = False

    R = None
    M_matrix = None
    is_agca = False

    try:
        if isinstance(witness, ModulePresentation):
            R = witness.ring
            M_matrix = witness.matrix
        elif isinstance(witness, tuple) and len(witness) == 2:
            R = witness[0]
            if isinstance(witness[1], Matrix) or isinstance(witness[1], list):
                M_matrix = Matrix(witness[1])
            elif hasattr(witness[1], 'annihilator'):
                is_agca = True
                witness = witness[1]
        elif isinstance(witness, Matrix):
            R = ZZ
            M_matrix = witness
        elif isinstance(witness, list):
            R = ZZ
            M_matrix = Matrix(witness)
        elif hasattr(witness, 'ring') and hasattr(witness, 'annihilator'):
            R = witness.ring
            is_agca = True
    except Exception:
        pass

    # H_1: R is an integral domain
    try:
        if R is not None:
            if R in (ZZ, QQ):
                h1_ok = True
            elif hasattr(R, 'is_domain') and R.is_domain:
                h1_ok = True
            elif hasattr(R, 'is_IntegralDomain') and R.is_IntegralDomain:
                h1_ok = True
            elif isinstance(R, sympy.Poly):
                h1_ok = True
            elif R in (sympy.S.Integers, sympy.S.Reals, sympy.S.Rationals):
                h1_ok = True
    except Exception:
        pass

    # H_2: M is a finitely generated module over R
    try:
        if M_matrix is not None and isinstance(M_matrix, Matrix):
            # A finite presentation matrix implies a finitely generated module
            h2_ok = True
        elif is_agca:
            # AGCA modules with an annihilator method are finitely generated in SymPy
            h2_ok = True
    except Exception:
        pass

    # ¬Q: Ann_R(M) is zero
    try:
        if M_matrix is not None and isinstance(M_matrix, Matrix):
            # For a module presented by an n x m matrix A over an integral domain,
            # the annihilator is zero if and only if rank(A) < n.
            neg_q_ok = bool(M_matrix.rank() < M_matrix.rows)
        elif is_agca:
            ann = witness.annihilator()
            if hasattr(ann, 'is_zero') and ann.is_zero:
                neg_q_ok = True
            elif hasattr(ann, 'is_Zero') and ann.is_Zero:
                neg_q_ok = True
            elif hasattr(R, 'ideal') and ann == R.ideal(0):
                neg_q_ok = True
            elif ann == 0 or ann == {0} or ann == [0]:
                neg_q_ok = True
    except Exception:
        pass

    return [h1_ok, h2_ok, neg_q_ok]