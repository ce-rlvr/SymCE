import sympy
from sympy import ZZ, QQ, Matrix, Symbol, degree
from sympy.combinatorics import CyclicGroup, SymmetricGroup, AlternatingGroup, DihedralGroup

# Top-level setup: named object bindings
x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
V4 = DihedralGroup(2)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture:
    "Let R be a Euclidean domain. Then M is a torsion-free module."
    
    The witness can be a tuple (R, M) where R is the ring and M represents the module,
    or just M (in which case R is assumed to be ZZ).
    M can be represented as:
      - An integer `n` or polynomial `p`, representing the cyclic module R/<M>.
      - A finite abelian group (for R = ZZ).
      - A presentation matrix over ZZ.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, M = witness
        else:
            R = ZZ
            M = witness

        # H_1: R is a Euclidean domain
        h1_ok = False
        try:
            if R in (ZZ, QQ):
                h1_ok = True
            elif str(R) == 'ZZ' or str(R) == 'QQ':
                h1_ok = True
            elif hasattr(R, 'is_PID') and R.is_PID:
                h1_ok = True
            elif hasattr(R, 'domain') and hasattr(R, 'gens'):
                # Polynomial ring over a field in one variable
                if getattr(R.domain, 'is_Field', False) and len(R.gens) == 1:
                    h1_ok = True
            elif hasattr(R, 'is_Field') and R.is_Field:
                h1_ok = True
        except Exception:
            pass

        # neg_Q: M is NOT a torsion-free module (i.e., M has torsion)
        neg_q = False
        try:
            if isinstance(M, int) or (hasattr(M, 'is_Integer') and M.is_Integer):
                # M represents ZZ/<M>. It has torsion if M is not 0 and not a unit (1, -1).
                if M != 0 and abs(M) != 1:
                    neg_q = True
            elif hasattr(M, 'is_group') and M.is_group:
                # A finite abelian group has torsion if it is non-trivial.
                if M.is_abelian and M.order() > 1:
                    neg_q = True
            elif hasattr(M, 'is_Matrix') and M.is_Matrix:
                # M is a presentation matrix over ZZ.
                if R == ZZ or str(R) == 'ZZ':
                    snf = M.smith_normal_form()
                    for i in range(min(snf.rows, snf.cols)):
                        val = abs(snf[i, i])
                        if val > 1:
                            neg_q = True
                            break
            else:
                # Try to interpret M as an element of R, representing R/<M>.
                if R == ZZ or str(R) == 'ZZ':
                    val = int(M)
                    if val != 0 and abs(val) != 1:
                        neg_q = True
                else:
                    # For polynomial rings over a field, non-zero non-units have degree > 0.
                    deg = degree(M)
                    if deg > 0:
                        neg_q = True
        except Exception:
            pass

        return [h1_ok, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "¬Q: M is not a torsion-free module"
]

N_HYP = 1
NEG_Q_INDEX = 1