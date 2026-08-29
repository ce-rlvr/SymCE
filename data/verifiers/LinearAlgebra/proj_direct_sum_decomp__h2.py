import sympy
from sympy import eye, zeros
import z3
import itertools
import functools
import math

# Top-level setup
# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

# The witness should be a tuple (n, P_func)
# where n is an integer (the dimension of the vector space R^n)
# and P_func is a callable taking a list of n elements and returning a list of n elements.
# Note: P_func will be evaluated with z3.Real variables to rigorously verify the properties.
# It must use only operations supported by z3 (e.g., +, -, *, /). 
# Conditional logic can be implemented using z3.If.

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False]
        n, P_func = witness
        if not isinstance(n, int) or n < 1:
            return [False, False, False]
        if not callable(P_func):
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: V is a vector space
    # R^n is always a vector space for n >= 1.
    h1 = True

    try:
        x = [z3.Real(f'x{i}') for i in range(n)]
        Px = P_func(x)
        if len(Px) != n:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_2: P^2 = P
    try:
        PPx = P_func(Px)
        solver = z3.Solver()
        solver.set("timeout", 2000)
        condition = z3.Or([PPx[i] != Px[i] for i in range(n)])
        solver.add(condition)
        res = solver.check()
        h2 = (res == z3.unsat)
    except Exception:
        h2 = False

    # ¬Q: V = ker(P) \oplus im(P) is FALSE
    # The conclusion means:
    # 1. im(P) is a subspace
    # 2. ker(P) is a subspace
    # 3. V = ker(P) + im(P)
    # (Intersection is automatically {0} if P^2 = P)
    # If any of these fail, the conclusion is false (neg_Q is True).
    neg_q = False
    try:
        u = [z3.Real(f'u{i}') for i in range(n)]
        v = [z3.Real(f'v{i}') for i in range(n)]
        a = z3.Real('a')
        b = z3.Real('b')
        
        Pu = P_func(u)
        Pv = P_func(v)
        
        # Check 1: Is im(P) a subspace?
        lin_comb = [a * Pu[i] + b * Pv[i] for i in range(n)]
        P_lin_comb = P_func(lin_comb)
        
        solver1 = z3.Solver()
        solver1.set("timeout", 2000)
        solver1.add(z3.Or([P_lin_comb[i] != lin_comb[i] for i in range(n)]))
        if solver1.check() == z3.sat:
            neg_q = True

        # Check 2: Is ker(P) a subspace?
        if not neg_q:
            solver2 = z3.Solver()
            solver2.set("timeout", 2000)
            solver2.add(z3.And([Pu[i] == 0 for i in range(n)]))
            solver2.add(z3.And([Pv[i] == 0 for i in range(n)]))
            
            comb = [a * u[i] + b * v[i] for i in range(n)]
            P_comb = P_func(comb)
            solver2.add(z3.Or([P_comb[i] != 0 for i in range(n)]))
            if solver2.check() == z3.sat:
                neg_q = True

        # Check 3: Is V = ker(P) + im(P)?
        if not neg_q:
            m = [z3.Real(f'm{i}') for i in range(n)]
            Pm = P_func(m)
            m_is_im = z3.And([Pm[i] == m[i] for i in range(n)])
            x_minus_m = [x[i] - m[i] for i in range(n)]
            P_x_minus_m = P_func(x_minus_m)
            x_minus_m_is_ker = z3.And([P_x_minus_m[i] == 0 for i in range(n)])
            
            valid_decomp = z3.And(m_is_im, x_minus_m_is_ker)
            
            solver3 = z3.Solver()
            solver3.set("timeout", 2000)
            # Check if there exists an x that CANNOT be decomposed into k + m
            solver3.add(z3.ForAll(m, z3.Not(valid_decomp)))
            if solver3.check() == z3.sat:
                neg_q = True

    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a vector space",
    "H_2: P^2 = P",
    "¬Q: V is not the direct sum of ker(P) and im(P)"
]

N_HYP = 2
NEG_Q_INDEX = 2