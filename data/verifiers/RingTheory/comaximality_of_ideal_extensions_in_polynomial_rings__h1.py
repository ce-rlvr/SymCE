import sympy
from sympy import Matrix, zeros, eye, Rational, Integer

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_rank(matrices):
    if not matrices:
        return 0
    try:
        M = sympy.Matrix([list(m) for m in matrices])
        return M.rank()
    except Exception:
        return 0

def is_subspace(A, B):
    if not A:
        return True
    if not B:
        return get_rank(A) == 0
    rank_B = get_rank(B)
    rank_AB = get_rank(A + B)
    return rank_AB == rank_B

def spans_equal(A, B):
    if not A and not B:
        return True
    rank_A = get_rank(A)
    rank_B = get_rank(B)
    if rank_A != rank_B:
        return False
    return get_rank(A + B) == rank_A

def conditions(witness) -> list[bool]:
    try:
        R_basis = list(witness[0])
        I_basis = list(witness[1])
        J_basis = list(witness[2])
    except Exception:
        return [False] * 5

    try:
        all_matrices = R_basis + I_basis + J_basis
        if all_matrices:
            shape = all_matrices[0].shape
            if shape[0] != shape[1]:
                return [False] * 5
            for m in all_matrices:
                if m.shape != shape:
                    return [False] * 5
    except Exception:
        return [False] * 5

    try:
        R_mult = [A * B for A in R_basis for B in R_basis]
        h1 = is_subspace(R_mult, R_basis)
    except Exception:
        h1 = False

    try:
        h2_sub = is_subspace(I_basis, R_basis)
        I_mult_R = [A * B for A in I_basis for B in R_basis]
        R_mult_I = [A * B for A in R_basis for B in I_basis]
        h2_ideal = is_subspace(I_mult_R + R_mult_I, I_basis)
        h2 = h2_sub and h2_ideal
    except Exception:
        h2 = False

    try:
        h3_sub = is_subspace(J_basis, R_basis)
        J_mult_R = [A * B for A in J_basis for B in R_basis]
        R_mult_J = [A * B for A in R_basis for B in J_basis]
        h3_ideal = is_subspace(J_mult_R + R_mult_J, J_basis)
        h3 = h3_sub and h3_ideal
    except Exception:
        h3 = False

    try:
        h4 = spans_equal(I_basis + J_basis, R_basis)
    except Exception:
        h4 = False

    try:
        R_I = [A * B for A in R_basis for B in I_basis]
        I_R = [A * B for A in I_basis for B in R_basis]
        I_x = R_I + I_R
        
        R_J = [A * B for A in R_basis for B in J_basis]
        J_R = [A * B for A in J_basis for B in R_basis]
        J_x = R_J + J_R
        
        neg_q = not spans_equal(I_x + J_x, R_basis)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: I is an ideal of R",
    "H_3: J is an ideal of R",
    "H_4: I and J are comaximal in R",
    "¬Q: The extended ideals of I and J are not comaximal in the polynomial ring"
]

N_HYP = 4
NEG_Q_INDEX = 4