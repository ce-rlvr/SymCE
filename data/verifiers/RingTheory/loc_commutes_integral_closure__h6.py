import sympy
from sympy import I, sqrt, Rational, Integer, symbols
from sympy.polys.domains import ZZ, QQ

# Top-level setup: named object bindings that the witness expression may reference.
try:
    QQ_I = QQ.algebraic_field(I)
except Exception:
    QQ_I = None

try:
    from sympy.polys.domains import ZZ_I
except ImportError:
    ZZ_I = None

def conditions(witness) -> list[bool]:
    h1 = h2 = h3 = h4 = h5 = neg_q = False

    def get_prop(name):
        if isinstance(witness, dict) and name in witness:
            val = witness[name]
            if callable(val):
                return val()
            return val
        if hasattr(witness, name):
            val = getattr(witness, name)
            if callable(val):
                return val()
            return val
        return None

    # Extract components if witness is a tuple
    tup_R = tup_K = tup_L = tup_A = tup_S = None
    if isinstance(witness, tuple) and len(witness) >= 5:
        tup_R, tup_K, tup_L, tup_A, tup_S = witness[:5]

    # H_1: R is an integral domain
    try:
        prop = get_prop('R_is_integral_domain')
        if prop is not None:
            h1 = bool(prop)
        else:
            R = get_prop('R')
            if R is None: R = tup_R
            if R is not None:
                h1 = bool(getattr(R, 'is_domain', False) or getattr(R, 'is_integral_domain', False))
    except Exception:
        pass

    # H_2: K is the field of fractions of R
    try:
        prop = get_prop('K_is_field_of_fractions')
        if prop is not None:
            h2 = bool(prop)
        else:
            R = get_prop('R')
            if R is None: R = tup_R
            K = get_prop('K')
            if K is None: K = tup_K
            
            if R is not None and K is not None:
                get_f = getattr(R, 'get_field', None)
                if get_f and callable(get_f) and K == get_f():
                    h2 = True
                elif K == getattr(R, 'frac_field', None):
                    h2 = True
    except Exception:
        pass

    # H_3: L is an algebraic field extension of K
    try:
        prop = get_prop('L_is_algebraic_extension')
        if prop is not None:
            h3 = bool(prop)
        else:
            K = get_prop('K')
            if K is None: K = tup_K
            L = get_prop('L')
            if L is None: L = tup_L
            
            if K is not None and L is not None:
                h3 = bool(getattr(L, 'domain', None) == K or getattr(L, 'is_AlgebraicExtension', False))
    except Exception:
        pass

    # H_4: A is the integral closure of R in L
    try:
        prop = get_prop('A_is_integral_closure')
        if prop is not None:
            h4 = bool(prop)
        else:
            R = get_prop('R')
            if R is None: R = tup_R
            L = get_prop('L')
            if L is None: L = tup_L
            A = get_prop('A')
            if A is None: A = tup_A
            
            if A is not None:
                if hasattr(A, 'is_integral_closure'):
                    h4 = bool(A.is_integral_closure(R, L))
                elif str(R) == 'ZZ' and 'I' in str(A):
                    h4 = True
    except Exception:
        pass

    # H_5: S is a multiplicatively closed subset of R
    try:
        prop = get_prop('S_is_multiplicatively_closed')
        if prop is not None:
            h5 = bool(prop)
        else:
            S = get_prop('S')
            if S is None: S = tup_S
            
            if S is not None:
                if hasattr(S, 'is_multiplicatively_closed'):
                    if callable(S.is_multiplicatively_closed):
                        h5 = bool(S.is_multiplicatively_closed())
                    else:
                        h5 = bool(S.is_multiplicatively_closed)
                else:
                    h5 = (1 in S) and all((a * b in S) for a in S for b in S)
    except Exception:
        pass

    # ¬Q: The localized ring S^{-1}A is not the integral closure of S^{-1}R in L
    try:
        prop = get_prop('conclusion_fails')
        if prop is not None:
            neg_q = bool(prop)
        else:
            S = get_prop('S')
            if S is None: S = tup_S
            
            if S is not None:
                # If 0 is in S, S^{-1}R is the zero ring, which cannot be a subring of the field L.
                # Thus, the integral closure of S^{-1}R in L is undefined or not S^{-1}A.
                if 0 in S:
                    neg_q = True
    except Exception:
        pass

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: K is the field of fractions of R",
    "H_3: L is an algebraic field extension of K",
    "H_4: A is the integral closure of R in L",
    "H_5: S is a multiplicatively closed subset of R",
    "¬Q: The localized ring S^{-1}A is not the integral closure of S^{-1}R in L"
]

N_HYP = 5
NEG_Q_INDEX = 5