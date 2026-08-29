import sympy
from sympy import Poly, minpoly
from sympy.abc import x

# Top-level setup for potential witness expressions
Z2 = sympy.CyclicGroup(2)
Z3 = sympy.CyclicGroup(3)
Z4 = sympy.CyclicGroup(4)
Z6 = sympy.CyclicGroup(6)
S3 = sympy.SymmetricGroup(3)
S4 = sympy.SymmetricGroup(4)
A4 = sympy.AlternatingGroup(4)
D4 = sympy.DihedralGroup(4)
C4 = sympy.CyclicGroup(4)
V4 = sympy.AlternatingGroup(4)
trivial = sympy.CyclicGroup(1)
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

N_HYP = 3
NEG_Q_INDEX = 3

CONDITION_LABELS = [
    "H_1: F \\subseteq K is a field extension",
    "H_2: \\alpha \\in K is algebraic over F",
    "H_3: L is an algebraically closed field containing F",
    "¬Q: The number of distinct F-homomorphisms from F(\\alpha) to L is NOT exactly the number of distinct roots of m(x) in L"
]

def conditions(witness):
    """
    Given a witness dictionary, checks the hypotheses and the negated conclusion.
    Expected witness format:
    {
        'F': <sympy domain, e.g., QQ>,
        'K': <sympy domain, e.g., QQ.algebraic_field(I)>,
        'alpha': <algebraic element in K>,
        'L': <sympy domain, e.g., CC>,
        'm': <sympy polynomial expression in x>
    }
    """
    if not isinstance(witness, dict):
        return [False, False, False, False]
        
    try:
        F = witness.get('F')
        K = witness.get('K')
        alpha = witness.get('alpha')
        L = witness.get('L')
        m = witness.get('m')
    except Exception:
        return [False, False, False, False]
        
    # H_1: F \subseteq K is a field extension
    try:
        h1 = getattr(F, 'is_Field', False) and getattr(K, 'is_Field', False)
        if h1:
            # Check if F is a subfield of K by attempting to convert F's identity
            K.convert(F.one)
    except Exception:
        h1 = False

    # H_2: \alpha \in K is algebraic over F
    try:
        # Check if alpha belongs to K
        K.convert(alpha)
        # Check if alpha is algebraic over F (minpoly will succeed and have degree > 0)
        mp = minpoly(alpha, x, domain=F)
        h2 = Poly(mp, x).degree() > 0
    except Exception:
        h2 = False

    # H_3: L is an algebraically closed field containing F
    try:
        # In sympy, CC and QQbar are the standard algebraically closed fields
        h3 = str(L) in ['CC', 'Complexes', 'C', 'QQbar'] or getattr(L, 'is_algebraically_closed', False)
        if h3 and hasattr(L, 'convert') and hasattr(F, 'one'):
            try:
                L.convert(F.one)
            except Exception:
                pass
    except Exception:
        h3 = False

    # ¬Q: The number of distinct F-homomorphisms from F(\alpha) to L 
    # is NOT exactly the number of distinct roots of m(x) in L.
    try:
        # The number of distinct F-homomorphisms to an algebraically closed field
        # is the number of distinct roots of the minimal polynomial of alpha over F.
        mp = minpoly(alpha, x, domain=F)
        mp_poly = Poly(mp, x)
        if mp_poly.is_zero:
            num_hom = -1
        else:
            num_hom = mp_poly.sqf_part().degree()
            
        # The number of distinct roots of m(x) in L
        m_poly = Poly(m, x)
        if m_poly.is_zero:
            num_roots_m = -1
        else:
            num_roots_m = m_poly.sqf_part().degree()
            
        neg_q = (num_hom != num_roots_m)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]