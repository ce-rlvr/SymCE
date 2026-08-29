import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics import Permutation
from sympy.abc import x

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    H1 = False
    neg_Q = False
    
    try:
        n = None
        if hasattr(witness, 'is_square') and witness.is_square:
            is_perm = True
            for i in range(witness.rows):
                row_ones = sum(1 for val in witness[i, :] if val == 1)
                row_zeros = sum(1 for val in witness[i, :] if val == 0)
                if row_ones != 1 or row_zeros != witness.cols - 1:
                    is_perm = False
                    break
            if is_perm:
                for j in range(witness.cols):
                    col_ones = sum(1 for val in witness[:, j] if val == 1)
                    col_zeros = sum(1 for val in witness[:, j] if val == 0)
                    if col_ones != 1 or col_zeros != witness.rows - 1:
                        is_perm = False
                        break
            
            if is_perm:
                p_list = []
                for i in range(witness.rows):
                    for j in range(witness.cols):
                        if witness[i, j] == 1:
                            p_list.append(j)
                            break
                
                perm = Permutation(p_list)
                cycles = perm.cyclic_form
                if len(cycles) == 1:
                    n = len(cycles[0])
                    H1 = True
    except Exception:
        H1 = False

    try:
        if H1 and n is not None:
            char_poly = witness.charpoly(x).as_expr()
            expected_poly = x**n - 1
            if sympy.expand(char_poly - expected_poly) != 0:
                neg_Q = True
    except Exception:
        neg_Q = False

    return [H1, neg_Q]

CONDITION_LABELS = [
    "H_1: The permutation associated with P is a single cyclic permutation of length n",
    "¬Q: The characteristic polynomial of P is not x^n - 1"
]

N_HYP = 1
NEG_Q_INDEX = 1