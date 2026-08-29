import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def parse_witness(witness):
    if isinstance(witness, dict):
        return witness.get('ring'), witness.get('a'), witness.get('b'), witness.get('d')
    elif isinstance(witness, (list, tuple)) and len(witness) == 4:
        return witness[0], witness[1], witness[2], witness[3]
    return None, None, None, None

def conditions(witness) -> list[bool]:
    ring, a, b, d = parse_witness(witness)
    
    # H_1: R is a Euclidean domain and d is a valid Euclidean valuation
    h1 = False
    try:
        if ring == 'Z':
            max_val = 30
            h1 = True
            # Check if d maps non-zero elements to non-negative integers
            for x in range(-max_val, max_val + 1):
                if x != 0:
                    val = d(x)
                    if not isinstance(val, int) or val < 0:
                        h1 = False
                        break
            # Check the division algorithm locally
            if h1:
                for y in range(-max_val, max_val + 1):
                    if y == 0: continue
                    dy = d(y)
                    for x in range(-max_val, max_val + 1):
                        found = False
                        base_q = x // y
                        for q in range(base_q - 5, base_q + 6):
                            r = x - y * q
                            if r == 0:
                                found = True
                                break
                            try:
                                if d(r) < dy:
                                    found = True
                                    break
                            except Exception:
                                pass
                        if not found:
                            h1 = False
                            break
                    if not h1:
                        break
                        
        elif ring == 'Q[x]':
            x_sym = sympy.Symbol('x')
            polys = [sympy.Integer(0)]
            for c0 in [-1, 0, 1]:
                for c1 in [-1, 0, 1]:
                    polys.append(c0 + c1 * x_sym)
            a_expr = sympy.sympify(a)
            b_expr = sympy.sympify(b)
            if a_expr not in polys: polys.append(a_expr)
            if b_expr not in polys: polys.append(b_expr)
            
            h1 = True
            for p in polys:
                if p != 0:
                    val = d(p)
                    if not isinstance(val, int) or val < 0:
                        h1 = False
                        break
            if h1:
                for B in polys:
                    if B == 0: continue
                    dB = d(B)
                    for A in polys:
                        found = False
                        for Q in polys:
                            R = sympy.expand(A - B * Q)
                            if R == 0:
                                found = True
                                break
                            try:
                                if d(R) < dB:
                                    found = True
                                    break
                            except Exception:
                                pass
                        if not found:
                            h1 = False
                            break
                    if not h1:
                        break
    except Exception:
        h1 = False

    # H_2: a and b are non-zero elements of R
    h2 = False
    try:
        if ring == 'Z':
            if isinstance(a, (int, sympy.Integer)) and isinstance(b, (int, sympy.Integer)) and int(a) != 0 and int(b) != 0:
                h2 = True
        elif ring == 'Q[x]':
            x_sym = sympy.Symbol('x')
            a_expr = sympy.sympify(a)
            b_expr = sympy.sympify(b)
            if a_expr != 0 and b_expr != 0 and a_expr.free_symbols.issubset({x_sym}) and b_expr.free_symbols.issubset({x_sym}):
                h2 = True
    except Exception:
        h2 = False

    # H_3: a divides b
    h3 = False
    try:
        if ring == 'Z':
            if int(b) % int(a) == 0:
                h3 = True
        elif ring == 'Q[x]':
            a_expr = sympy.sympify(a)
            b_expr = sympy.sympify(b)
            if sympy.rem(b_expr, a_expr) == 0:
                h3 = True
    except Exception:
        h3 = False

    # H_4: d(a) = d(b)
    h4 = False
    try:
        if d(a) == d(b):
            h4 = True
    except Exception:
        h4 = False

    # ¬Q: a and b are not associate elements in R
    neg_q = False
    try:
        if ring == 'Z':
            if abs(int(a)) != abs(int(b)):
                neg_q = True
        elif ring == 'Q[x]':
            a_expr = sympy.sympify(a)
            b_expr = sympy.sympify(b)
            if sympy.rem(a_expr, b_expr) != 0 or sympy.rem(b_expr, a_expr) != 0:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain with valuation d",
    "H_2: a and b are non-zero elements of R",
    "H_3: a divides b",
    "H_4: d(a) = d(b)",
    "¬Q: a and b are not associate elements in R"
]

N_HYP = 4
NEG_Q_INDEX = 4