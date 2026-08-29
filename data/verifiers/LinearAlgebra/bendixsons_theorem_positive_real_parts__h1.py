import sympy
from sympy import Matrix, I, re, im, simplify, eye, zeros
import sympy.combinatorics
from sympy.combinatorics import Permutation, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

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

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            A, lam = witness
            explicit_lam = True
        else:
            A = witness
            explicit_lam = False
            
        if not hasattr(A, 'is_square'):
            A = Matrix(A)
    except Exception:
        return [False, False, False]

    # H1: Symmetric part of A is positive definite
    h1 = False
    try:
        if hasattr(A, 'is_square') and A.is_square:
            S = (A + A.T) / 2
            if S.is_positive_definite == True:
                h1 = True
            else:
                # Fallback: S must be real (since it's symmetric, real implies Hermitian)
                # and all its eigenvalues must be strictly positive.
                if S == S.conjugate():
                    evals = S.eigenvals()
                    all_pos = True
                    for e in evals:
                        try:
                            if float(re(e).evalf()) <= 0:
                                all_pos = False
                                break
                        except Exception:
                            if simplify(re(e)) <= 0:
                                all_pos = False
                                break
                    if all_pos and len(evals) > 0:
                        h1 = True
    except Exception:
        h1 = False

    # H2 and neg_Q
    h2 = False
    neg_q = False
    try:
        if hasattr(A, 'is_square') and A.is_square:
            if explicit_lam:
                # Check H2: lam is an eigenvalue of A
                I_mat = eye(A.shape[0])
                char_val = (A - lam * I_mat).det()
                if simplify(char_val) == 0:
                    h2 = True
                else:
                    try:
                        if abs(complex(char_val.evalf())) < 1e-9:
                            h2 = True
                    except Exception:
                        pass
                
                if not h2:
                    evals = A.eigenvals()
                    for e in evals:
                        if simplify(e - lam) == 0:
                            h2 = True
                            break
                        try:
                            if abs(complex((e - lam).evalf())) < 1e-9:
                                h2 = True
                                break
                        except Exception:
                            pass
                            
                # Check neg_Q: Real part of lam is <= 0
                try:
                    if float(re(lam).evalf()) <= 0:
                        neg_q = True
                except Exception:
                    if simplify(re(lam)) <= 0:
                        neg_q = True
            else:
                # If lam is not explicitly provided, check if ANY eigenvalue violates the conclusion.
                evals = A.eigenvals()
                if len(evals) > 0:
                    h2 = True
                for e in evals:
                    try:
                        if float(re(e).evalf()) <= 0:
                            neg_q = True
                            break
                    except Exception:
                        if simplify(re(e)) <= 0:
                            neg_q = True
                            break
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The symmetric part of A, 1/2(A + A^T), is positive definite",
    "H_2: lambda is an eigenvalue of A over the complex numbers",
    "¬Q: The real part of the eigenvalue lambda is not strictly positive (<= 0)"
]

N_HYP = 2
NEG_Q_INDEX = 2