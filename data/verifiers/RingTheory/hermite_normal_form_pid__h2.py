import sympy
from sympy import S, Matrix
from sympy.polys.domains import ZZ
import sympy.combinatorics as combinatorics

# Top-level setup
S3 = combinatorics.SymmetricGroup(3)
S4 = combinatorics.SymmetricGroup(4)
A4 = combinatorics.AlternatingGroup(4)
D4 = combinatorics.DihedralGroup(4)
C4 = combinatorics.CyclicGroup(4)
V4 = combinatorics.AlternatingGroup(4)
Z2 = combinatorics.CyclicGroup(2)
Z3 = combinatorics.CyclicGroup(3)
Z4 = combinatorics.CyclicGroup(4)
Z6 = combinatorics.CyclicGroup(6)
trivial = combinatorics.CyclicGroup(1)
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The dropped hypothesis was likely "Let A be an m by n matrix over R".
    Without it, A is unbound and can be a non-matrix or a matrix not over R,
    making the conclusion fail.
    """
    # The witness could be a tuple (R, A) or just A (with R implicitly ZZ)
    if isinstance(witness, tuple) and len(witness) == 2:
        R, A = witness
    else:
        R = S.Integers
        A = witness

    # H_1: Let R be a principal ideal domain
    h1 = False
    try:
        if R == S.Integers or R == ZZ:
            h1 = True
        elif hasattr(R, 'is_PID') and R.is_PID:
            h1 = True
        elif hasattr(R, 'is_Field') and R.is_Field:
            h1 = True
        elif hasattr(R, 'is_Poly') and getattr(R, 'is_Poly', False):
            if len(R.gens) == 1 and getattr(R.domain, 'is_Field', False):
                h1 = True
    except Exception:
        h1 = False

    # ¬Q: There does NOT exist an invertible m by m matrix U over R such that UA is in Hermite normal form.
    neg_q = False
    try:
        if not isinstance(A, Matrix):
            # If A is not a matrix, UA is undefined, so the conclusion fails.
            neg_q = True
        else:
            # Check if A is a valid matrix over R
            is_over_R = True
            for e in A:
                if R == S.Integers or R == ZZ:
                    if not e.is_integer:
                        is_over_R = False
                        break
                else:
                    in_r = False
                    if hasattr(R, 'contains'):
                        in_r = R.contains(e)
                    elif hasattr(R, '__contains__'):
                        in_r = (e in R)
                    else:
                        in_r = True
                    if not in_r:
                        is_over_R = False
                        break
            
            if not is_over_R:
                # If A has elements outside R, U over R cannot make UA an HNF over R.
                neg_q = True
            else:
                # If A is a valid matrix over R, and R is a PID, HNF generally exists.
                # For ZZ, we can explicitly verify if SymPy can compute it.
                if R == S.Integers or R == ZZ:
                    try:
                        A.hermite_normal_form()
                        neg_q = False
                    except Exception:
                        neg_q = True
                else:
                    neg_q = False
    except Exception:
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "¬Q: There does not exist an invertible m by m matrix U over R such that UA is in Hermite normal form"
]

N_HYP = 1
NEG_Q_INDEX = 1