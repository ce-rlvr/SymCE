import math
import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def convergent(a, k):
    """
    Computes the k-th convergent of the continued fraction a.
    Returns (p_k, q_k) in lowest terms with q_k > 0.
    """
    if k < 0 or k >= len(a):
        raise ValueError("Invalid convergent index")
    if k == 0:
        return a[0], 1
    
    num = a[k]
    den = 1
    for i in range(k-1, -1, -1):
        new_num = a[i] * num + den
        new_den = num
        num, den = new_num, new_den
        
    g = abs(math.gcd(num, den))
    num //= g
    den //= g
    if den < 0:
        num = -num
        den = -den
    return num, den

def conditions(witness) -> list[bool]:
    # Parse witness: can be a tuple (a, n) or just the list `a` (where n is implicitly len(a)-1)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            a, n = witness
        else:
            a = witness
            n = len(a) - 1
    except Exception:
        return [False, False, False]

    # H_1: Let x = [a_0; a_1, a_2, ...] be a simple continued fraction
    try:
        h1 = isinstance(a, (list, tuple)) and len(a) > 0 and isinstance(a[0], int)
        if h1:
            for x in a[1:]:
                if not isinstance(x, int) or x < 1:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H_2: Let p_n / q_n denote the n-th convergent of x
    # (n must be a valid index for the sequence of convergents of x)
    try:
        h2 = isinstance(n, int) and 0 <= n < len(a)
    except Exception:
        h2 = False

    # Conclusion: The matrix [[p_n, p_{n-1}], [q_n, q_{n-1}]] is equal to the matrix product
    try:
        p_n, q_n = convergent(a, n)
        p_n_minus_1, q_n_minus_1 = convergent(a, n-1)
        
        LHS = Matrix([[p_n, p_n_minus_1], [q_n, q_n_minus_1]])
        
        RHS = Matrix([[1, 0], [0, 1]])
        for k in range(n + 1):
            RHS = RHS * Matrix([[a[k], 1], [1, 0]])
            
        conclusion = (LHS == RHS)
    except Exception:
        # If any error occurs (e.g. n=0 means p_{-1} is undefined), the conclusion fails.
        conclusion = False

    neg_q = not conclusion

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x is a simple continued fraction",
    "H_2: p_n / q_n is the n-th convergent of x, expressed in lowest terms",
    "¬Q: The matrix equation fails"
]

N_HYP = 2
NEG_Q_INDEX = 2