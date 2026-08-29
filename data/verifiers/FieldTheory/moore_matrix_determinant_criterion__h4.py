import sympy
from sympy import Matrix, eye, zeros
from sympy.ntheory import factorint
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Standard group theory bindings
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

# Standard linear algebra bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    def get_val(name):
        if isinstance(witness, dict) and name in witness:
            return witness[name]
        elif hasattr(witness, name):
            return getattr(witness, name)
        raise ValueError(f"Missing {name}")

    # H_1: F_q is a finite field with q elements
    try:
        q = get_val('q')
        factors = factorint(q)
        h1 = (len(factors) == 1) and (q >= 2)
        p = list(factors.keys())[0]
    except Exception:
        h1 = False
        p = 2

    # H_2: n is a positive integer
    try:
        n = get_val('n')
        h2 = isinstance(n, int) and n > 0
    except Exception:
        h2 = False

    # H_3: alpha_1, alpha_2, ..., alpha_n are elements of the extension field F_{q^n}
    try:
        alphas = get_val('alphas')
        h3 = isinstance(alphas, (list, tuple)) and len(alphas) == n
    except Exception:
        h3 = False

    # ¬Q: The determinant of M is non-zero if and only if alphas are linearly independent over F_q (must fail)
    try:
        M = get_val('M')
        det_M = M.det()
        
        # Evaluate if determinant is non-zero in the field of characteristic p
        if hasattr(det_M, 'is_Integer') and det_M.is_Integer:
            det_nonzero = (det_M % p != 0)
        elif isinstance(det_M, int):
            det_nonzero = (det_M % p != 0)
        else:
            det_nonzero = (det_M != 0)
            
        # Evaluate linear independence of alphas over F_q
        if all(isinstance(a, int) for a in alphas):
            if n == 1:
                indep = (alphas[0] % p != 0)
            else:
                # n > 1 elements in F_q are always linearly dependent over F_q
                indep = False
        elif all(isinstance(a, (list, tuple)) for a in alphas):
            mat = Matrix(alphas)
            indep = (mat.rank() == n)
        else:
            if n == 1:
                indep = (alphas[0] != 0)
            else:
                indep = False
                
        q_holds = (det_nonzero == indep)
        neg_q = not q_holds
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: n is a positive integer",
    "H_3: alpha_1, alpha_2, ..., alpha_n are elements of the extension field F_{q^n}",
    "¬Q: det(M) != 0 is not equivalent to alphas being linearly independent over F_q"
]

N_HYP = 3
NEG_Q_INDEX = 3