import sympy
from sympy import Matrix, Mod, eye, zeros, Rational, Integer, Symbol
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math

# Top-level setup: named object bindings
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
    # H_1: Let A commute with its conjugate transpose, such that A* A = A A*
    try:
        if witness * witness.H == witness.H * witness:
            H1 = True
        else:
            # Fallback for symbolic matrices where equality might not evaluate trivially
            diff = witness * witness.H - witness.H * witness
            diff = sympy.simplify(diff)
            H1 = all(e == 0 or e.is_zero for e in diff)
    except Exception:
        H1 = False

    # ¬Q: The Jordan canonical form of A is NOT a diagonal matrix
    neg_Q = False
    
    # 1. Try standard sympy is_diagonalizable
    try:
        diag = witness.is_diagonalizable()
        if diag is False:
            neg_Q = True
    except Exception:
        pass

    # 2. Try computing the Jordan form directly
    if not neg_Q:
        try:
            J = witness.jordan_form()[1]
            if J.is_diagonal() is False:
                neg_Q = True
        except Exception:
            pass

    # 3. Try finite field check (where sympy's standard methods often fail)
    # A matrix over GF(p) is diagonalizable over the algebraic closure iff A**(p**L) == A
    # where L is the least common multiple of 1, 2, ..., n (n being the matrix dimension).
    if not neg_Q:
        try:
            p = None
            for e in witness:
                if isinstance(e, Mod):
                    p = e.q
                    break
                elif hasattr(e, 'mod'):
                    p = e.mod
                    break
            
            if p is not None:
                n = witness.shape[0]
                L = 1
                for i in range(1, n + 1):
                    L = (L * i) // math.gcd(L, i)
                
                power = p**L
                B = witness**power
                if B != witness:
                    neg_Q = True
        except Exception:
            pass

    return [H1, neg_Q]

CONDITION_LABELS = [
    "H_1: A commutes with its conjugate transpose (A* A = A A*)",
    "¬Q: The Jordan canonical form of A is not a diagonal matrix"
]

N_HYP = 1
NEG_Q_INDEX = 1