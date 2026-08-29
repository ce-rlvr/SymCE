import sympy as sp
import itertools

QQ = sp.QQ
ZZ = sp.ZZ
x1, x2, x3, x4, x5 = sp.symbols('x1 x2 x3 x4 x5')

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: E = F(x_1, ..., x_n) is the field of rational functions in n variables over F",
    "H_3: s_1, ..., s_n are the elementary symmetric polynomials in the variables x_1, ..., x_n",
    "¬Q: E is not a finite Galois extension of K, or Gal(E/K) is not isomorphic to S_n"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, dict):
            F = witness.get('F', None)
            n = witness.get('n', None)
            K_gens = witness.get('K_gens', None)
        elif isinstance(witness, (list, tuple)) and len(witness) == 3:
            F, n, K_gens = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: F is a field
    try:
        h1 = False
        if F in [sp.QQ, sp.RR, sp.CC]:
            h1 = True
        elif hasattr(F, 'is_Field') and F.is_Field:
            h1 = True
        elif hasattr(F, 'is_field') and F.is_field:
            h1 = True
    except Exception:
        h1 = False

    # H2: E = F(x_1, ..., x_n)
    try:
        h2 = isinstance(n, int) and 1 <= n <= 10
    except Exception:
        h2 = False

    # H3: s_1, ..., s_n are the elementary symmetric polynomials
    try:
        h3 = isinstance(n, int) and 1 <= n <= 10
    except Exception:
        h3 = False

    # neg_Q
    try:
        if not isinstance(K_gens, (list, tuple)):
            neg_q = False
        elif len(K_gens) == 0:
            neg_q = True
        else:
            x = sp.symbols(f'x1:{n+1}')
            J = sp.Matrix(K_gens).jacobian(x)
            if J.rank() < n:
                neg_q = True
            else:
                is_sym = True
                for g in K_gens:
                    for i in range(n-1):
                        swapped = sp.simplify(g.subs({x[i]: x[i+1], x[i+1]: x[i]}, simultaneous=True))
                        if sp.simplify(g - swapped) != 0:
                            is_sym = False
                            break
                    if not is_sym:
                        break
                
                if not is_sym:
                    neg_q = True
                else:
                    s_exprs = []
                    for i in range(1, n+1):
                        s = sum(sp.Mul(*comb) for comb in itertools.combinations(x, i))
                        s_exprs.append(s)
                    
                    k_set = set(sp.simplify(g) for g in K_gens)
                    s_set = set(sp.simplify(s) for s in s_exprs)
                    if k_set == s_set:
                        neg_q = False
                    else:
                        neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]