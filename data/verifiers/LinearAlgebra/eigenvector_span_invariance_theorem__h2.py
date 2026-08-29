import sympy
from sympy import Matrix, zeros, eye
import itertools

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: V is a vector space",
    "H_2: S is a subset of V consisting entirely of eigenvectors of T",
    "¬Q: The subspace spanned by S is not invariant under T"
]

N_HYP = 2
NEG_Q_INDEX = 2

def apply_T(T, v):
    if callable(T):
        return T(v)
    else:
        return T * v

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            T = witness['T']
            S = witness['S']
        else:
            T = witness.T
            S = witness.S
    except Exception:
        return [False, False, False]

    # H_1: V is a vector space
    # We verify that S is a collection of column vectors of the same dimension.
    try:
        S_list = list(S)
        if len(S_list) == 0:
            h1 = True
        else:
            shape = S_list[0].shape
            h1 = all(isinstance(v, Matrix) and v.shape == shape and shape[1] == 1 for v in S_list)
    except Exception:
        h1 = False

    # H_2: S is a subset of V consisting entirely of eigenvectors of T
    try:
        h2 = True
        S_list = list(S)
        if len(S_list) == 0:
            h2 = True
        else:
            for v in S_list:
                if v.is_zero_matrix:
                    h2 = False
                    break
                Tv = apply_T(T, v)
                if not isinstance(Tv, Matrix) or Tv.shape != v.shape:
                    h2 = False
                    break
                # v is an eigenvector if Tv is a scalar multiple of v.
                # Since v is non-zero, this is true iff the rank of [v, Tv] is 1.
                M = v.row_join(Tv)
                if M.rank() > 1:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # ¬Q: The subspace spanned by S is not invariant under T
    try:
        neg_q = False
        S_list = list(S)
        if len(S_list) > 0:
            S_mat = S_list[0]
            for v in S_list[1:]:
                S_mat = S_mat.row_join(v)
            rank_S = S_mat.rank()
            
            # Generate linear combinations of elements in S
            coeffs = [-1, 0, 1, 2]
            if len(S_list) > 5:
                combinations = []
                for i in range(len(S_list)):
                    for j in range(i+1, len(S_list)):
                        combinations.append(S_list[i] + S_list[j])
            else:
                combinations = []
                for c in itertools.product(coeffs, repeat=len(S_list)):
                    w = S_list[0] * 0
                    for i, coeff in enumerate(c):
                        if coeff != 0:
                            w += coeff * S_list[i]
                    combinations.append(w)
            
            # Check if T(w) is in span(S) for all generated w
            for w in combinations:
                Tw = apply_T(T, w)
                M = S_mat.row_join(Tw)
                if M.rank() > rank_S:
                    neg_q = True
                    break
        else:
            # If S is empty, span(S) is {0}. We check if T(0) != 0.
            V_dim = witness.get('V_dim') if isinstance(witness, dict) else getattr(witness, 'V_dim', None)
            if V_dim is not None:
                zero = zeros(V_dim, 1)
                if not apply_T(T, zero).is_zero_matrix:
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]