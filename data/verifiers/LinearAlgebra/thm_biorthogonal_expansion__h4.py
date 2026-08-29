import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros, Matrix
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
    """
    Checks the hypotheses and negated conclusion for the false Biorthogonal Expansion Theorem.
    The dropped hypothesis was that v is an element of V.
    Witness should be a tuple (B, B_star, v) or a dict with these keys, where:
      - B is a list of column vectors (sympy Matrices) forming a basis for V.
      - B_star is a list of row vectors or callables forming the dual basis.
      - v is a column vector in the ambient space.
    """
    try:
        if isinstance(witness, dict):
            B = witness.get('B')
            B_star = witness.get('B_star')
            v = witness.get('v')
        else:
            B, B_star, v = witness
    except Exception:
        return [False, False, False, False]

    # H1: V is a finite-dimensional vector space over a field F
    try:
        if not isinstance(B, (list, tuple)) or not isinstance(B_star, (list, tuple)):
            h1 = False
        elif len(B) == 0 or len(B_star) == 0:
            h1 = False
        else:
            m = B[0].shape[0]
            h1_B = all(isinstance(b, Matrix) and b.shape == (m, 1) for b in B)
            h1_v = isinstance(v, Matrix) and v.shape == (m, 1)
            h1_B_star = True
            for f in B_star:
                if callable(f):
                    pass
                elif isinstance(f, Matrix) and f.shape == (1, m):
                    pass
                else:
                    h1_B_star = False
                    break
            h1 = h1_B and h1_v and h1_B_star
    except Exception:
        h1 = False

    # H2: B is a basis for V
    try:
        if not h1:
            h2 = False
        else:
            M = Matrix.hstack(*B)
            h2 = M.rank() == len(B)
    except Exception:
        h2 = False

    # H3: B^* is the dual basis for V^* corresponding to B
    try:
        if not h1:
            h3 = False
        else:
            h3 = True
            if len(B) != len(B_star):
                h3 = False
            else:
                for i, f in enumerate(B_star):
                    for j, b in enumerate(B):
                        if callable(f):
                            val = f(b)
                            if isinstance(val, Matrix):
                                val = val[0, 0]
                        else:
                            val = (f * b)[0, 0]
                        expected = 1 if i == j else 0
                        if val != expected and sympy.simplify(val - expected) != 0:
                            h3 = False
                            break
                    if not h3:
                        break
    except Exception:
        h3 = False

    # neg_Q: v != sum(f_i(v) v_i)
    try:
        if not h1:
            neg_q = False
        else:
            v_proj = zeros(v.shape[0], 1)
            for i in range(len(B)):
                f = B_star[i]
                if callable(f):
                    coeff = f(v)
                    if isinstance(coeff, Matrix):
                        coeff = coeff[0, 0]
                else:
                    coeff = (f * v)[0, 0]
                v_proj += coeff * B[i]
            
            diff = v_proj - v
            is_zero = True
            for i in range(diff.shape[0]):
                if diff[i, 0] != 0 and sympy.simplify(diff[i, 0]) != 0:
                    is_zero = False
                    break
            neg_q = not is_zero
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: B is a basis for V",
    "H_3: B^* is the dual basis for V^* corresponding to B",
    "¬Q: v != sum(f_i(v) v_i)"
]

N_HYP = 3
NEG_Q_INDEX = 3