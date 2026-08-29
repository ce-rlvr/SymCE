import sympy as sp
from sympy.abc import x
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Standard algebra objects
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Let R be a Noetherian ring. The homomorphism f is injective, and therefore an isomorphism."
    
    The witness can be:
    1. A SymPy expression in `x` representing the image of x under an endomorphism of Q[x].
    2. A SymPy matrix representing an endomorphism of the ring Q^n (with element-wise multiplication).
    3. A dictionary containing one of the above under the keys 'expr', 'matrix', or 'f'.
    4. A callable function f(x).
    """
    h1 = False
    neg_q = False
    
    try:
        # Unpack dictionary witness if provided
        if isinstance(witness, dict):
            if 'matrix' in witness:
                witness = witness['matrix']
            elif 'expr' in witness:
                witness = witness['expr']
            elif 'f' in witness:
                witness = witness['f']

        # Evaluate callable witness on the symbol x
        if callable(witness):
            try:
                witness = witness(x)
            except Exception:
                pass

        if isinstance(witness, sp.Matrix):
            # Check if it's a valid endomorphism of the Noetherian ring Q^n
            # For Q^n with element-wise multiplication, a linear map is a ring endomorphism
            # iff every row of its matrix has exactly one 1 and the rest 0s.
            if witness.rows == witness.cols and witness.rows > 0:
                n = witness.rows
                is_hom = True
                for i in range(n):
                    row = list(witness.row(i))
                    if row.count(1) != 1 or row.count(0) != n - 1:
                        is_hom = False
                        break
                if is_hom:
                    h1 = True
                    # It is an isomorphism (and injective) iff the determinant is non-zero
                    if witness.det() == 0:
                        neg_q = True
        else:
            # Check if it's a valid endomorphism of the Noetherian ring Q[x]
            witness_expr = sp.sympify(witness)
            if witness_expr.is_polynomial(x) or witness_expr.is_number:
                h1 = True
                deg = sp.degree(witness_expr, x)
                # It is an isomorphism iff the degree is exactly 1.
                # If degree <= 0, it is not injective.
                # If degree > 1, it is injective but not surjective (hence not an isomorphism).
                if deg != 1:
                    neg_q = True
                    
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Noetherian ring",
    "¬Q: The homomorphism f is not injective (or not an isomorphism)"
]

N_HYP = 1
NEG_Q_INDEX = 1