import sympy
import itertools

# Top-level setup
x = sympy.Symbol('x')
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def get_monic_invariant_factors(A, x):
    n = A.shape[0]
    M = x * sympy.eye(n) - A
    D = [sympy.S.One]
    for k in range(1, n + 1):
        minors = []
        for row_indices in itertools.combinations(range(n), k):
            for col_indices in itertools.combinations(range(n), k):
                sub_M = M.extract(row_indices, col_indices)
                minors.append(sub_M.det())
        g = minors[0]
        for m in minors[1:]:
            g = sympy.gcd(g, m)
        LC = sympy.LC(g, x)
        if LC != 0:
            g = sympy.simplify(g / LC)
        D.append(g)
    inv_factors = []
    for k in range(1, n + 1):
        inv = sympy.simplify(D[k] / D[k-1])
        inv_factors.append(inv)
    return inv_factors

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and FAILS the conclusion.
    witness is expected to be a tuple: (A, F)
    where A is a sympy Matrix and F is a list of polynomials in x.
    """
    try:
        A, F = witness
        A = sympy.Matrix(A)
    except Exception:
        return [False, False, False]
    
    # H_1: f_1(x), ..., f_k(x) are the invariant factors of A
    try:
        monic_invs = get_monic_invariant_factors(A, x)
        n = A.shape[0]
        if len(F) > n or len(F) == 0:
            h1 = False
        else:
            # Pad F with 1s at the beginning to match the length of monic_invs
            padded_F = [sympy.S.One] * (n - len(F)) + list(F)
            h1 = True
            for f, inv in zip(padded_F, monic_invs):
                f_sym = sympy.sympify(f)
                inv_sym = sympy.sympify(inv)
                if f_sym.is_zero and inv_sym.is_zero:
                    continue
                if f_sym.is_zero or inv_sym.is_zero:
                    h1 = False
                    break
                if sympy.degree(f_sym, x) != sympy.degree(inv_sym, x):
                    h1 = False
                    break
                q = sympy.cancel(f_sym / inv_sym)
                num, den = q.as_numer_denom()
                if sympy.degree(den, x) != 0 or sympy.degree(num, x) != 0:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H_2: f_i(x) divides f_{i+1}(x) for all 1 <= i < k
    try:
        h2 = True
        if len(F) > 1:
            for i in range(len(F) - 1):
                f1 = sympy.sympify(F[i])
                f2 = sympy.sympify(F[i+1])
                if f1.is_zero:
                    if not f2.is_zero:
                        h2 = False
                        break
                else:
                    q = sympy.cancel(f2 / f1)
                    num, den = q.as_numer_denom()
                    if sympy.degree(den, x) != 0:
                        h2 = False
                        break
    except Exception:
        h2 = False

    # neg_Q: The minimal polynomial of A is NOT f_k(x)
    try:
        # The minimal polynomial is exactly the largest (last) monic invariant factor
        min_poly = monic_invs[-1]
        fk = sympy.sympify(F[-1])
        diff = sympy.simplify(min_poly - fk)
        neg_q = not diff.is_zero
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f_1(x), ..., f_k(x) are the invariant factors of A",
    "H_2: f_i(x) divides f_{i+1}(x) for all 1 <= i < k",
    "¬Q: The minimal polynomial of A is not f_k(x)"
]

N_HYP = 2
NEG_Q_INDEX = 2