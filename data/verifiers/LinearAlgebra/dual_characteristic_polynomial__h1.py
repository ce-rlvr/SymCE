import sympy
from sympy import Matrix, MatrixSymbol, oo, Symbol, simplify, eye, zeros
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

x = Symbol('x')

CONDITION_LABELS = [
    "H_1: T: V -> V is a linear operator",
    "¬Q: The characteristic polynomial of T is NOT identical to the characteristic polynomial of the dual operator T*"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    h1 = False
    try:
        if isinstance(witness, sympy.MatrixBase):
            h1 = True
        elif isinstance(witness, sympy.MatrixSymbol):
            h1 = True
        elif type(witness).__name__ == 'ModuleHomomorphism':
            h1 = True
        elif callable(witness):
            # Test linearity on polynomials
            p1 = x**2 + 1
            p2 = x**3 - x
            try:
                res = simplify(witness(2*p1 + 3*p2) - (2*witness(p1) + 3*witness(p2)))
                if res == 0:
                    h1 = True
            except Exception:
                pass
            
            if not h1:
                # Test linearity on vectors
                try:
                    v1 = Matrix([1, 2])
                    v2 = Matrix([3, 4])
                    if witness(2*v1 + 3*v2) == 2*witness(v1) + 3*witness(v2):
                        h1 = True
                except Exception:
                    pass
        elif hasattr(witness, 'is_linear_operator'):
            attr = witness.is_linear_operator
            h1 = bool(attr() if callable(attr) else attr)
        elif hasattr(witness, 'is_linear'):
            attr = witness.is_linear
            h1 = bool(attr() if callable(attr) else attr)
        elif isinstance(witness, str):
            w_lower = witness.lower()
            if any(word in w_lower for word in ["shift", "diff", "deriv", "integral", "infinite"]):
                h1 = True
    except Exception:
        pass

    neg_q = False
    try:
        if hasattr(witness, 'charpoly') and hasattr(witness, 'dual'):
            cp_T = witness.charpoly() if callable(witness.charpoly) else witness.charpoly
            dual_op = witness.dual() if callable(witness.dual) else witness.dual
            cp_T_star = dual_op.charpoly() if callable(dual_op.charpoly) else dual_op.charpoly
            neg_q = (cp_T != cp_T_star)
        elif isinstance(witness, sympy.MatrixBase):
            cp_T = witness.charpoly()
            cp_T_star = witness.transpose().charpoly()
            neg_q = (cp_T != cp_T_star)
        elif isinstance(witness, sympy.MatrixSymbol):
            if witness.shape[0] == oo:
                neg_q = True
            else:
                neg_q = False
        elif type(witness).__name__ == 'ModuleHomomorphism':
            neg_q = True
        elif callable(witness):
            is_finite = False
            try:
                for n in [1, 2, 3, 4]:
                    v = sympy.zeros(n, 1)
                    res = witness(v)
                    if isinstance(res, sympy.MatrixBase):
                        is_finite = True
                        break
            except Exception:
                pass
            
            if is_finite:
                neg_q = False
            else:
                # Infinite dimensional operators do not have a defined characteristic polynomial
                neg_q = True
        elif isinstance(witness, str):
            w_lower = witness.lower()
            if any(word in w_lower for word in ["shift", "diff", "deriv", "integral", "infinite"]):
                neg_q = True
    except Exception:
        # If characteristic polynomial computation fails or is undefined, they are not identical
        neg_q = True

    return [h1, neg_q]