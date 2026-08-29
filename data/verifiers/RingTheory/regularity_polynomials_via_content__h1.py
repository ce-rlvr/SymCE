import sympy
from sympy import eye, zeros

# Top-level setup
x = sympy.Symbol('x')
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_gcd(lst):
    g = 0
    for val in lst:
        g = sympy.gcd(g, val)
    return g

def get_coeffs(witness):
    if hasattr(witness, 'as_expr'):
        try:
            witness = witness.as_expr()
        except Exception:
            pass

    if isinstance(witness, sympy.Expr) and not hasattr(witness, 'rows'):
        witness = sympy.Matrix([[witness]])

    if isinstance(witness, (list, tuple)) and all(hasattr(c, 'rows') for c in witness):
        return list(witness)
        
    if hasattr(witness, 'rows'):
        free_symbols = witness.free_symbols
        if len(free_symbols) > 1:
            return None
        var = list(free_symbols)[0] if free_symbols else sympy.Symbol('x')
        
        max_deg = 0
        for entry in witness:
            entry = sympy.sympify(entry)
            if entry.has(var):
                try:
                    deg = sympy.degree(entry, var)
                    if deg > max_deg:
                        max_deg = deg
                except Exception:
                    pass
                    
        coeffs = []
        for d in range(max_deg + 1):
            mat = sympy.zeros(witness.rows, witness.cols)
            for i in range(witness.rows):
                for j in range(witness.cols):
                    entry = sympy.sympify(witness[i, j])
                    if entry.has(var):
                        try:
                            poly = sympy.Poly(sympy.expand(entry), var)
                            mat[i, j] = poly.nth(d)
                        except Exception:
                            return None
                    elif d == 0:
                        mat[i, j] = entry
            coeffs.append(mat)
        return coeffs
    return None

def parse_witness_full(witness):
    n = 0
    f = witness
    if isinstance(witness, tuple) and len(witness) == 2:
        if isinstance(witness[0], (int, sympy.Integer)):
            n = int(witness[0])
            f = witness[1]
    coeffs = get_coeffs(f)
    return n, coeffs

def conditions(witness) -> list[bool]:
    # H1: f is a polynomial in R[x]
    try:
        n, coeffs = parse_witness_full(witness)
        if not coeffs:
            h1_ok = False
        else:
            k = coeffs[0].rows
            if k == 0 or coeffs[0].cols != k:
                h1_ok = False
            elif not all(mat.shape == (k, k) for mat in coeffs):
                h1_ok = False
            else:
                h1_ok = True
    except Exception:
        h1_ok = False

    # H2: The content ideal c(f) contains at least one non-zero-divisor of R
    try:
        n, coeffs = parse_witness_full(witness)
        if not coeffs:
            h2_ok = False
        else:
            entries = []
            for mat in coeffs:
                for i in range(mat.rows):
                    for j in range(mat.cols):
                        entries.append(mat[i, j])
            
            if n == 0:
                if not all(isinstance(e, (int, sympy.Integer)) for e in entries):
                    h2_ok = False
                else:
                    m = get_gcd(entries)
                    h2_ok = bool(m != 0)
            else:
                n_abs = abs(n)
                if not all(isinstance(e, (int, sympy.Integer)) for e in entries):
                    h2_ok = False
                else:
                    m = get_gcd(entries + [n_abs])
                    h2_ok = bool(m == 1)
    except Exception:
        h2_ok = False

    # not Q: f is NOT a regular element (i.e., f IS a zero-divisor) in R[x]
    try:
        n, coeffs = parse_witness_full(witness)
        if not coeffs:
            neg_q_ok = False
        else:
            var = sympy.Symbol('x')
            k = coeffs[0].rows
            F = sympy.zeros(k, k)
            for d, mat in enumerate(coeffs):
                F += mat * (var**d)
            
            D = F.det()
            D = sympy.expand(D)
            
            if n == 0:
                neg_q_ok = bool(D == 0)
            else:
                n_abs = abs(n)
                if n_abs == 1:
                    neg_q_ok = False
                else:
                    D_poly = sympy.Poly(D, var)
                    if D_poly.is_zero:
                        neg_q_ok = True
                    else:
                        c = D_poly.coeffs()
                        m = get_gcd(c + [n_abs])
                        neg_q_ok = bool(m > 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a polynomial in the ring R",
    "H_2: The content ideal contains at least one non-zero-divisor of R",
    "not Q: f is not a regular element in the polynomial ring"
]

N_HYP = 2
NEG_Q_INDEX = 2