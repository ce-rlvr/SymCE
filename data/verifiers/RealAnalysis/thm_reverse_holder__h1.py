import math
import sympy as sp
from sympy import eye, zeros, Rational, Integer, Symbol
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness expressions
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: p in (0, 1) and q = p/(p-1)",
    "H_2: f and g are strictly positive measurable functions on Omega",
    "H_3: f in L^p(mu) and g in L^q(mu)",
    "H_4: integral of g^q dmu > 0",
    "not Q: integral of fg dmu < (integral of f^p dmu)^{1/p} * (integral of g^q dmu)^{1/q}"
]

N_HYP = 4
NEG_Q_INDEX = 4

def to_float(val):
    if hasattr(val, 'evalf'):
        return float(val.evalf())
    return float(val)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            q = witness.get('q')
            f = witness.get('f')
            g = witness.get('g')
            mu = witness.get('mu', None)
            Omega = witness.get('Omega', None)
            x = witness.get('x', None)
        else:
            p = getattr(witness, 'p', None)
            q = getattr(witness, 'q', None)
            f = getattr(witness, 'f', None)
            g = getattr(witness, 'g', None)
            mu = getattr(witness, 'mu', None)
            Omega = getattr(witness, 'Omega', None)
            x = getattr(witness, 'x', None)

        if mu is None:
            if hasattr(f, '__iter__') and not isinstance(f, str):
                mu = [1.0] * len(list(f))
            else:
                mu = 1.0

        # H1: p in (0, 1) and q = p/(p-1)
        try:
            p_val = to_float(p)
            q_val = to_float(q)
            h1 = (0 < p_val < 1) and math.isclose(q_val, p_val / (p_val - 1), rel_tol=1e-5)
        except Exception:
            h1 = False

        # H2 & Integrals
        h2 = False
        int_fp = float('inf')
        int_gq = float('inf')
        int_fg = float('inf')

        try:
            if hasattr(f, '__iter__') and not isinstance(f, str):
                f_list = list(f)
                g_list = list(g)
                mu_list = list(mu)
                h2 = all(to_float(fi) > 0 for fi in f_list) and all(to_float(gi) > 0 for gi in g_list)
                
                int_fp = sum((to_float(fi)**p_val) * to_float(mi) for fi, mi in zip(f_list, mu_list))
                int_gq = sum((to_float(gi)**q_val) * to_float(mi) for gi, mi in zip(g_list, mu_list))
                int_fg = sum(to_float(fi) * to_float(gi) * to_float(mi) for fi, gi, mi in zip(f_list, g_list, mu_list))
            else:
                if Omega is None:
                    Omega = (0, 1)
                
                if hasattr(Omega, 'start'):
                    O_start = to_float(Omega.start)
                    O_end = to_float(Omega.end)
                else:
                    O_start = to_float(Omega[0])
                    O_end = to_float(Omega[1])
                
                if callable(f):
                    N = 1000
                    dx = (O_end - O_start) / N
                    pts = [O_start + dx * (i + 0.5) for i in range(N)]
                    h2 = all(to_float(f(pt)) > 0 for pt in pts) and all(to_float(g(pt)) > 0 for pt in pts)
                    
                    def eval_mu(pt):
                        return to_float(mu(pt)) if callable(mu) else to_float(mu)
                        
                    int_fp = sum((to_float(f(pt))**p_val) * eval_mu(pt) * dx for pt in pts)
                    int_gq = sum((to_float(g(pt))**q_val) * eval_mu(pt) * dx for pt in pts)
                    int_fg = sum(to_float(f(pt)) * to_float(g(pt)) * eval_mu(pt) * dx for pt in pts)
                else:
                    if x is None:
                        x = sp.Symbol('x')
                    
                    pts = [O_start + (O_end - O_start) * i / 10.0 for i in range(1, 10)]
                    h2 = all(to_float(f.subs(x, pt)) > 0 for pt in pts) and all(to_float(g.subs(x, pt)) > 0 for pt in pts)
                    
                    int_fp = to_float(sp.integrate((f**p_val) * mu, (x, O_start, O_end)))
                    int_gq = to_float(sp.integrate((g**q_val) * mu, (x, O_start, O_end)))
                    int_fg = to_float(sp.integrate(f * g * mu, (x, O_start, O_end)))
        except Exception:
            pass

        # H3: f in L^p(mu) and g in L^q(mu)
        try:
            h3 = (int_fp < float('inf')) and (int_gq < float('inf'))
        except Exception:
            h3 = False

        # H4: integral of g^q dmu > 0
        try:
            h4 = int_gq > 0
        except Exception:
            h4 = False

        # Conclusion: integral of fg dmu >= (integral of f^p dmu)^{1/p} * (integral of g^q dmu)^{1/q}
        try:
            rhs = (int_fp ** (1.0 / p_val)) * (int_gq ** (1.0 / q_val))
            neg_q = int_fg < rhs - 1e-7
        except Exception:
            neg_q = False

        return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]
    except Exception:
        return [False, False, False, False, False]