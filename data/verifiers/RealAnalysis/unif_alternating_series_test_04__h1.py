import sympy
from sympy import Symbol, limit, oo, Abs, Sum, simplify, Interval, S, maximum
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

x = Symbol('x', real=True)
n = Symbol('n', integer=True, positive=True)
k = Symbol('k', integer=True, positive=True)

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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: {f_n} is a sequence of real-valued functions defined on S",
    "H_2: For each x in S and each n in N, f_{n+1}(x) <= f_n(x)",
    "H_3: The sequence {f_n} converges uniformly to the zero function on S",
    "¬Q: The alternating series does not converge uniformly on S"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f_expr = witness['f']
            domain = witness['S']
            n_sym = witness.get('n', n)
            x_sym = witness.get('x', x)
        else:
            f_expr, domain = witness
            n_sym = n
            x_sym = x
    except Exception:
        return [False, False, False, False]
        
    # H1: f_n is a sequence of real-valued functions defined on S
    try:
        h1 = isinstance(f_expr, sympy.Expr)
    except Exception:
        h1 = False
    
    # H2: f_{n+1}(x) <= f_n(x)
    h2 = False
    try:
        diff = simplify(f_expr.subs(n_sym, n_sym + 1) - f_expr)
        max_diff = maximum(diff, x_sym, domain)
        if max_diff.is_nonpositive:
            h2 = True
        else:
            is_le_0 = True
            for n_val in range(1, 11):
                val = maximum(diff.subs(n_sym, n_val), x_sym, domain)
                if val > 0:
                    is_le_0 = False
                    break
            if is_le_0:
                lim_val = limit(max_diff, n_sym, oo)
                if lim_val > 0:
                    is_le_0 = False
            h2 = is_le_0
    except Exception:
        h2 = False
        
    # H3: f_n(x) -> 0 uniformly on S
    h3 = False
    try:
        sup_f = maximum(Abs(f_expr), x_sym, domain)
        if limit(sup_f, n_sym, oo) == 0:
            h3 = True
    except Exception:
        h3 = False
        
    # neg_Q: The alternating series does NOT converge uniformly on S
    neg_q = False
    try:
        sup_term = maximum(Abs(f_expr), x_sym, domain)
        if limit(sup_term, n_sym, oo) != 0:
            neg_q = True
        else:
            if h2:
                neg_q = False
            else:
                S_inf = Sum((-1)**(k+1) * f_expr.subs(n_sym, k), (k, 1, oo)).doit()
                if not isinstance(S_inf, Sum):
                    S_n = Sum((-1)**(k+1) * f_expr.subs(n_sym, k), (k, 1, n_sym)).doit()
                    R_n = simplify(S_inf - S_n)
                    sup_R = maximum(Abs(R_n), x_sym, domain)
                    if limit(sup_R, n_sym, oo) != 0:
                        neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]