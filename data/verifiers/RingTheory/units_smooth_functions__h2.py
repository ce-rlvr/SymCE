import sympy
from sympy import Matrix, Expr, Set, S, solveset, Eq, det, zeros, eye

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        M, f = witness
    except Exception:
        return [False, False, False]

    # H1: M is a smooth manifold
    try:
        h1 = isinstance(M, Set)
    except Exception:
        h1 = False

    # H2: f is an element of C^infty(M)
    try:
        if isinstance(f, Matrix):
            elements = list(f)
        elif isinstance(f, Expr):
            elements = [f]
        else:
            elements = []
            h2 = False
        
        if elements:
            h2 = True
            for el in elements:
                den = sympy.denom(el)
                if den != 1:
                    syms = den.free_symbols
                    if len(syms) == 1:
                        x = list(syms)[0]
                        sols = solveset(den, x, domain=M)
                        if sols.is_empty == False:
                            h2 = False
                            break
                    elif len(syms) == 0:
                        if den == 0:
                            h2 = False
                            break
                    else:
                        h2 = False
                        break
    except Exception:
        h2 = False

    # Conclusion: f is a unit in C^infty(M) if and only if f(p) != 0 for all p in M
    try:
        if isinstance(f, Matrix):
            if f.shape[0] != f.shape[1]:
                is_unit = False
            else:
                d = f.det()
                syms = d.free_symbols
                if len(syms) == 1:
                    x = list(syms)[0]
                    sols = solveset(d, x, domain=M)
                    is_unit = (sols.is_empty == True)
                elif len(syms) == 0:
                    is_unit = (d != 0)
                else:
                    is_unit = False
        elif isinstance(f, Expr):
            syms = f.free_symbols
            if len(syms) == 1:
                x = list(syms)[0]
                sols = solveset(f, x, domain=M)
                is_unit = (sols.is_empty == True)
            elif len(syms) == 0:
                is_unit = (f != 0)
            else:
                is_unit = False
        else:
            is_unit = False
    except Exception:
        is_unit = False

    try:
        if isinstance(f, Matrix):
            syms = f.free_symbols
            if len(syms) == 1:
                x = list(syms)[0]
                common_roots = M
                for el in f:
                    sols = solveset(el, x, domain=M)
                    common_roots = sympy.Intersection(common_roots, sols)
                is_never_zero = (common_roots.is_empty == True)
            elif len(syms) == 0:
                is_never_zero = not f.is_zero_matrix
            else:
                is_never_zero = False
        elif isinstance(f, Expr):
            syms = f.free_symbols
            if len(syms) == 1:
                x = list(syms)[0]
                sols = solveset(f, x, domain=M)
                is_never_zero = (sols.is_empty == True)
            elif len(syms) == 0:
                is_never_zero = (f != 0)
            else:
                is_never_zero = False
        else:
            is_never_zero = False
    except Exception:
        is_never_zero = False

    try:
        neg_q = (is_unit != is_never_zero)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: M is a smooth manifold",
    "H_2: f is an element of C^infty(M)",
    "¬Q: f is a unit in C^infty(M) iff f(p) != 0 for all p in M fails"
]

N_HYP = 2
NEG_Q_INDEX = 2