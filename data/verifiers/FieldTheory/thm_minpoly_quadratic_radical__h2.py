import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import Symbol, simplify, minpoly, QQ, RR, CC, I, sqrt, Matrix, eye, zeros

# Top-level setup for witness expressions
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

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    Returns a list of booleans: [H_1, H_2, H_3, H_4, neg_Q].
    """
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            K = witness.get('K')
            alpha = witness.get('alpha')
        else:
            F, K, alpha = witness
    except Exception:
        return [False, False, False, False, False]

    # H_1: F \subseteq K is a field extension
    try:
        f_is_field = getattr(F, 'is_Field', getattr(F, 'is_field', False))
        if callable(f_is_field):
            f_is_field = f_is_field()
            
        k_is_field = getattr(K, 'is_Field', getattr(K, 'is_field', False))
        if callable(k_is_field):
            k_is_field = k_is_field()
            
        h1 = bool(f_is_field) and bool(k_is_field)
    except Exception:
        h1 = False

    # H_2: \alpha \in K
    try:
        if hasattr(K, '__contains__'):
            h2 = alpha in K
        elif hasattr(K, 'contains'):
            h2 = K.contains(alpha)
        else:
            h2 = True
    except Exception:
        h2 = False

    # H_3: \alpha \notin F
    try:
        if hasattr(F, '__contains__'):
            h3 = alpha not in F
        elif hasattr(F, 'contains'):
            h3 = not F.contains(alpha)
        else:
            h3 = False
    except Exception:
        h3 = False

    # H_4: \alpha^2 \in F
    try:
        try:
            a2 = alpha**2
        except Exception:
            a2 = alpha * alpha
            
        if hasattr(F, '__contains__'):
            h4 = a2 in F
        elif hasattr(F, 'contains'):
            h4 = F.contains(a2)
        else:
            h4 = False
    except Exception:
        h4 = False

    # ¬Q: The minimal polynomial of \alpha over F is not x^2 - \alpha^2
    try:
        x = Symbol('x')
        
        # Compute the minimal polynomial of alpha over F
        if hasattr(alpha, 'minimal_polynomial'):
            mp = alpha.minimal_polynomial(x)
        else:
            try:
                mp = minpoly(alpha, x, domain=F)
            except Exception:
                mp = minpoly(alpha, x)
                
        if hasattr(mp, 'as_expr'):
            mp = mp.as_expr()
            
        # Expected polynomial: x^2 - \alpha^2
        expected = x**2 - a2
        if hasattr(expected, 'as_expr'):
            expected = expected.as_expr()
            
        # Check if they are different
        diff = simplify(mp - expected)
        
        if hasattr(diff, 'is_zero_matrix') and diff.is_zero_matrix:
            neg_q = False
        elif diff == 0:
            neg_q = False
        else:
            diff_expanded = sympy.expand(diff)
            if diff_expanded == 0:
                neg_q = False
            else:
                neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F \\subseteq K is a field extension",
    "H_2: \\alpha \\in K",
    "H_3: \\alpha \\notin F",
    "H_4: \\alpha^2 \\in F",
    "¬Q: The minimal polynomial of \\alpha over F is not x^2 - \\alpha^2"
]

N_HYP = 4
NEG_Q_INDEX = 4