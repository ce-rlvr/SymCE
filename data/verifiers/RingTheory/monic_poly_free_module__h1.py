import sympy
from sympy import eye, zeros, Matrix, Symbol, Rational, Integer
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = ["H_1: f is a polynomial", "H_2: f is monic", "H_3: degree of f is at least 1", "not Q: factor ring is not a free module"]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, (list, tuple)):
            h1 = True
            if len(witness) == 0:
                h1 = False
            else:
                first = witness[0]
                if hasattr(first, 'is_Matrix') and first.is_Matrix:
                    k = first.rows
                    if first.cols != k:
                        h1 = False
                    else:
                        for c in witness:
                            if not (hasattr(c, 'is_Matrix') and c.is_Matrix and c.rows == k and c.cols == k):
                                h1 = False
                                break
        elif hasattr(witness, 'is_Poly') and witness.is_Poly:
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if isinstance(witness, (list, tuple)) and h1:
            cleaned_witness = list(witness)
            while len(cleaned_witness) > 0:
                last = cleaned_witness[-1]
                if hasattr(last, 'is_Matrix') and last.is_Matrix:
                    if last.is_zero_matrix:
                        cleaned_witness.pop()
                    else:
                        break
                else:
                    if last == 0:
                        cleaned_witness.pop()
                    else:
                        break
            witness_to_use = cleaned_witness
        else:
            witness_to_use = witness
    except Exception:
        witness_to_use = witness

    try:
        if isinstance(witness_to_use, list) and h1 and len(witness_to_use) > 0:
            lc = witness_to_use[-1]
            if hasattr(lc, 'is_Matrix') and lc.is_Matrix:
                h2 = bool(lc == eye(lc.rows))
            else:
                h2 = bool(lc == 1)
        elif hasattr(witness_to_use, 'is_Poly') and witness_to_use.is_Poly:
            h2 = bool(witness_to_use.LC() == 1)
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        if isinstance(witness_to_use, list) and h1:
            h3 = bool(len(witness_to_use) >= 2)
        elif hasattr(witness_to_use, 'is_Poly') and witness_to_use.is_Poly:
            h3 = bool(witness_to_use.degree() >= 1)
        else:
            h3 = False
    except Exception:
        h3 = False

    try:
        neg_q = False
        if isinstance(witness_to_use, list) and h1:
            for c in witness_to_use:
                if hasattr(c, 'is_Matrix') and c.is_Matrix:
                    k = c.rows
                    if k == 0:
                        continue
                    val = c[0, 0]
                    is_scalar = True
                    for i in range(k):
                        for j in range(k):
                            if i == j:
                                if c[i, j] != val:
                                    is_scalar = False
                            else:
                                if c[i, j] != 0:
                                    is_scalar = False
                    if not is_scalar:
                        neg_q = True
                        break
                    if hasattr(val, 'is_commutative') and val.is_commutative is False:
                        neg_q = True
                        break
                else:
                    if hasattr(c, 'is_commutative') and c.is_commutative is False:
                        neg_q = True
                        break
        elif hasattr(witness_to_use, 'is_Poly') and witness_to_use.is_Poly:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]