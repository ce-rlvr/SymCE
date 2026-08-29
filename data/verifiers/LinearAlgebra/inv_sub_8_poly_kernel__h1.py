import sympy
from sympy import Matrix, Symbol, Poly, simplify
from sympy.matrices import eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

CONDITION_LABELS = [
    "H_1: T is a linear operator on V",
    "H_2: p(x) is a polynomial with coefficients in F",
    "¬Q: The kernel of the operator p(T) is not a T-invariant subspace of V"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        T, p = witness
    except Exception:
        return [False, False, False]
    
    # H1: T is a linear operator on V
    try:
        h1 = isinstance(T, Matrix) and T.is_square
    except Exception:
        h1 = False
        
    # H2: p(x) is a polynomial with coefficients in F
    try:
        if isinstance(p, list):
            h2 = len(p) > 0
        elif isinstance(p, Matrix):
            h2 = True
        else:
            x = Symbol('x')
            h2 = Poly(p, x).is_Poly
    except Exception:
        h2 = False
        
    # neg_Q: The kernel of the operator p(T) is NOT a T-invariant subspace of V.
    try:
        if isinstance(p, list):
            n = len(p) - 1
            pT = p[0] * (T**n)
            for i in range(1, n + 1):
                pT += p[i] * (T**(n - i))
        elif isinstance(p, Matrix):
            pT = p
        else:
            x = Symbol('x')
            poly = Poly(p, x)
            coeffs = poly.all_coeffs()
            n = len(coeffs) - 1
            pT = coeffs[0] * (T**n)
            for i in range(1, n + 1):
                pT += coeffs[i] * (T**(n - i))
                
        K_basis = pT.nullspace()
        is_invariant = True
        for v in K_basis:
            u = pT * (T * v)
            for val in u:
                if val != 0 and val.is_zero is not True:
                    if simplify(val) != 0:
                        is_invariant = False
                        break
            if not is_invariant:
                break
        neg_q = not is_invariant
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]