import z3
import math
import itertools
import functools
import sympy
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def check_valid(formula, timeout=1000):
    """
    Checks if a Z3 formula is valid (i.e., its negation is unsatisfiable).
    Returns False if it is invalid or if the solver times out.
    """
    s = z3.Solver()
    s.set("timeout", timeout)
    s.add(z3.Not(formula))
    return s.check() == z3.unsat

def conditions(witness):
    """
    Evaluates the hypotheses and the negated conclusion for a given witness.
    The witness is expected to be a dictionary with:
      - "n": int (dimension of x)
      - "m": int (dimension of y)
      - "x_0": list of numbers (length n)
      - "K": function taking a list of m Z3 Reals and returning a Z3 Bool
      - "N": function taking a list of n+m Z3 Reals and returning a Z3 Bool
    """
    try:
        n = int(witness["n"])
        m = int(witness["m"])
        x_0 = witness["x_0"]
        K_pred = witness["K"]
        N_pred = witness["N"]
    except Exception:
        return [False, False, False, False]
        
    if n <= 0 or m <= 0:
        return [False, False, False, False]
        
    if len(x_0) != n:
        return [False, False, False, False]
        
    # H_1: x_0 is a point in R^n
    try:
        x_0_vals = [float(x) for x in x_0]
        h1 = True
    except Exception:
        h1 = False

    # H_2: K is a compact subset of R^m (closed and bounded)
    try:
        y = [z3.Real(f'y_{i}') for i in range(m)]
        z = [z3.Real(f'z_{i}') for i in range(m)]
        M = z3.Real('M')
        eps = z3.Real('eps')
        
        K_y = K_pred(y)
        K_z = K_pred(z)
        
        # Bounded: Exists M > 0, ForAll y in K, ||y||^2 <= M
        norm_y_sq = sum([yi**2 for yi in y])
        bounded = z3.Exists(M, z3.And(M > 0, z3.ForAll(y, z3.Implies(K_y, norm_y_sq <= M))))
        
        # Closed: Complement is open
        dist_yz_sq = sum([(yi - zi)**2 for yi, zi in zip(y, z)])
        closed = z3.ForAll(y, z3.Implies(z3.Not(K_y), 
                    z3.Exists(eps, z3.And(eps > 0, 
                        z3.ForAll(z, z3.Implies(dist_yz_sq < eps, z3.Not(K_z)))))))
                        
        h2 = check_valid(bounded) and check_valid(closed)
    except Exception:
        h2 = False

    # H_3: N is an open subset of R^{n+m}
    try:
        p = [z3.Real(f'p_{i}') for i in range(n+m)]
        q = [z3.Real(f'q_{i}') for i in range(n+m)]
        eps2 = z3.Real('eps2')
        
        N_p = N_pred(p)
        N_q = N_pred(q)
        dist_pq_sq = sum([(pi - qi)**2 for pi, qi in zip(p, q)])
        
        open_N = z3.ForAll(p, z3.Implies(N_p, 
                    z3.Exists(eps2, z3.And(eps2 > 0, 
                        z3.ForAll(q, z3.Implies(dist_pq_sq < eps2, N_q))))))
                        
        h3 = check_valid(open_N)
    except Exception:
        h3 = False

    # ¬Q: There does NOT exist an open set U in R^n containing x_0 such that U x K \subseteq N
    # The conclusion Q is equivalent to:
    # Exists eps3 > 0, ForAll y in K, ForAll x in R^n, ||x - x_0||^2 < eps3 => N(x, y)
    try:
        x_vars = [z3.Real(f'x_{i}') for i in range(n)]
        eps3 = z3.Real('eps3')
        
        dist_x_x0_sq = sum([(xi - x0i)**2 for xi, x0i in zip(x_vars, x_0_vals)])
        xy = x_vars + y
        N_xy = N_pred(xy)
        
        conclusion = z3.Exists(eps3, z3.And(eps3 > 0, 
                        z3.ForAll(y, z3.Implies(K_pred(y), 
                            z3.ForAll(x_vars, z3.Implies(dist_x_x0_sq < eps3, N_xy))))))
                            
        neg_q = check_valid(z3.Not(conclusion))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: x_0 is a point in R^n",
    "H_2: K is a compact subset of R^m",
    "H_3: N is an open subset of R^{n+m}",
    "¬Q: There does not exist an open set U in R^n containing x_0 such that U x K is contained in N"
]

N_HYP = 3
NEG_Q_INDEX = 3