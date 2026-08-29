import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import exp, oo, integrate, diff, pi, factorial, sqrt, S, cancel, real_roots
from sympy.abc import x

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

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def get_gauss_hermite(n):
    if n == 1:
        return [(S(0), sqrt(pi))]
    elif n == 2:
        return [(-1/sqrt(S(2)), sqrt(pi)/2),
                (1/sqrt(S(2)), sqrt(pi)/2)]
    elif n == 3:
        return [(S(0), 2*sqrt(pi)/3),
                (-sqrt(S(3)/2), sqrt(pi)/6),
                (sqrt(S(3)/2), sqrt(pi)/6)]
    elif n == 4:
        r1 = sqrt((3 - sqrt(S(6)))/2)
        r2 = sqrt((3 + sqrt(S(6)))/2)
        w1 = (3 + sqrt(S(6))) * sqrt(pi) / 12
        w2 = (3 - sqrt(S(6))) * sqrt(pi) / 12
        return [(-r1, w1), (r1, w1), (-r2, w2), (r2, w2)]
    elif n == 5:
        r1 = sqrt((5 - sqrt(S(10)))/2)
        r2 = sqrt((5 + sqrt(S(10)))/2)
        w0 = 8*sqrt(pi)/15
        w1 = (7 + 2*sqrt(S(10))) * sqrt(pi) / 60
        w2 = (7 - 2*sqrt(S(10))) * sqrt(pi) / 60
        return [(S(0), w0), (-r1, w1), (r1, w1), (-r2, w2), (r2, w2)]
    else:
        raise ValueError("n too large")

def conditions(witness) -> list[bool]:
    try:
        f, n = witness
        if not isinstance(n, int) or n < 1:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: f is 2n times continuously differentiable on R
    try:
        d2n = diff(f, x, 2*n)
        num, den = cancel(d2n).as_numer_denom()
        if den.is_constant():
            h1_ok = True
        else:
            if den.is_polynomial(x):
                roots = real_roots(den)
                h1_ok = (len(roots) == 0)
            else:
                h1_ok = True # Fallback
    except Exception:
        h1_ok = False

    # H_2: The integral converges
    try:
        integ = integrate(exp(-x**2) * f, (x, -oo, oo))
        if integ.has(sympy.Integral) or integ in [oo, -oo, sympy.nan, sympy.zoo]:
            h2_ok = False
        else:
            h2_ok = True
    except Exception:
        h2_ok = False

    # ¬Q: The error term is NOT in the image of K * f^(2n)(c)
    try:
        if not h2_ok:
            neg_q_ok = False
        else:
            nodes_weights = get_gauss_hermite(n)
            I_n = sum(w * f.subs(x, node) for node, w in nodes_weights)
            E_n = sympy.simplify(integ - I_n)
            
            K = factorial(n) * sqrt(pi) / (2**n * factorial(2*n))
            V = sympy.simplify(E_n / K)
            
            g = d2n
            eq = sympy.simplify(g - V)
            
            if eq == 0:
                neg_q_ok = False
            else:
                num, den = cancel(eq).as_numer_denom()
                if num.is_constant() and num != 0:
                    neg_q_ok = True
                else:
                    if num.is_polynomial(x):
                        roots = real_roots(num)
                        neg_q_ok = (len(roots) == 0)
                    else:
                        sol = sympy.solveset(num, x, domain=S.Reals)
                        if sol == S.EmptySet:
                            neg_q_ok = True
                        elif sol != S.EmptySet and isinstance(sol, sympy.Set):
                            neg_q_ok = False
                        else:
                            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is 2n times continuously differentiable on R",
    "H_2: The integral of exp(-x^2)*f(x) converges",
    "¬Q: There is no c in R such that E_n(f) = K * f^(2n)(c)"
]

N_HYP = 2
NEG_Q_INDEX = 2