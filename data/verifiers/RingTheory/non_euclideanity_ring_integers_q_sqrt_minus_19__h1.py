import sympy
from sympy.ntheory import factorint

# Top-level setup
Z = sympy.S.Integers
Q = sympy.S.Rationals

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Let R be the ring of integers of K. Then R is a principal ideal domain but is not a Euclidean domain."
    
    The witness is expected to be a square-free integer `d` representing the number field K = Q(sqrt(d)).
    """
    try:
        if isinstance(witness, str):
            s = witness.replace(" ", "").lower()
            if s in ["z[i]", "z[sqrt(-1)]", "q(i)", "q(sqrt(-1))", "gaussianintegers"]:
                d = -1
            elif s in ["z[sqrt(-5)]", "q(sqrt(-5))"]:
                d = -5
            elif s in ["z", "q", "rationals", "integers"]:
                d = 1
            else:
                d = int(witness)
        else:
            d = int(witness)
    except Exception:
        return [False, False]

    # H_1: K is a number field (d is a square-free integer)
    try:
        if d == 0:
            h1 = False
        elif d in (1, -1):
            h1 = True
        else:
            factors = factorint(abs(d))
            h1 = all(v == 1 for v in factors.values())
    except Exception:
        h1 = False

    # neg_Q: R is NOT a PID, OR R IS Euclidean.
    try:
        if d < 0:
            # Known values for imaginary quadratic fields
            pid_d = {-1, -2, -3, -7, -11, -19, -43, -67, -163}
            euclidean_d = {-1, -2, -3, -7, -11}
            is_pid = d in pid_d
            is_euclidean = d in euclidean_d
            neg_q = (not is_pid) or is_euclidean
        elif d > 0 and d <= 100:
            # Known values for real quadratic fields up to d=100
            euclidean_d_pos = {1, 2, 3, 5, 6, 7, 11, 13, 14, 17, 19, 21, 29, 33, 37, 41, 57, 69, 73}
            pid_d_pos = euclidean_d_pos.union({22, 23, 31, 38, 43, 46, 47, 53, 59, 61, 62, 67, 71, 77, 83, 86, 89, 93, 94, 97})
            is_pid = d in pid_d_pos
            is_euclidean = d in euclidean_d_pos
            neg_q = (not is_pid) or is_euclidean
        else:
            # For d > 100, we don't have a hardcoded list.
            # A valid counterexample provided by a user will typically be small.
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K is a number field (witnessed by square-free integer d)",
    "¬Q: R is not a PID or R is a Euclidean domain"
]

N_HYP = 1
NEG_Q_INDEX = 1