import sympy

CONDITION_LABELS = [
    "H_1: n is an integer with n >= 3",
    "H_2: tau is the complex conjugation automorphism on C",
    "not Q: The restriction of tau to Q(zeta_n) is NOT a non-trivial Galois automorphism of order 2 that maps zeta_n to zeta_n^{-1}"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    n = None
    tau = None
    zeta_n = None
    
    if isinstance(witness, dict):
        n = witness.get('n')
        tau = witness.get('tau')
        zeta_n = witness.get('zeta_n')
    elif isinstance(witness, tuple):
        if len(witness) == 3:
            n, tau, zeta_n = witness
        elif len(witness) == 2:
            if callable(witness[1]):
                n, tau = witness
            else:
                n, zeta_n = witness
        elif len(witness) == 1:
            n = witness[0]
    else:
        n = witness

    if tau is None:
        tau = sympy.conjugate

    # H_1: n is an integer with n >= 3
    try:
        h1 = (isinstance(n, (int, sympy.Integer)) or (isinstance(n, float) and n.is_integer())) and n >= 3
    except Exception:
        h1 = False

    # H_2: tau is the complex conjugation automorphism on C
    try:
        if callable(tau):
            I = sympy.I
            # Check if tau behaves like complex conjugation on a few test points
            h2 = (tau(1 + I) == 1 - I) and (tau(I) == -I) and (tau(2) == 2)
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: The restriction of tau to Q(zeta_n) is NOT a non-trivial Galois automorphism 
    # of order 2 that maps zeta_n to zeta_n^{-1}
    try:
        if zeta_n is None:
            # If zeta_n is not provided, default to the standard primitive n-th root of unity
            zeta_n = sympy.exp(2 * sympy.pi * sympy.I / n)
            
        tz = tau(zeta_n)
        
        # Check if tau maps zeta_n to its inverse
        diff1 = sympy.simplify(tz - 1/zeta_n)
        try:
            maps_to_inv = (diff1 == 0) or (abs(complex(diff1)) < 1e-9)
        except Exception:
            maps_to_inv = (diff1 == 0)
            
        # Check if the automorphism is non-trivial (i.e., tau(zeta_n) != zeta_n)
        diff2 = sympy.simplify(tz - zeta_n)
        try:
            is_non_trivial = (diff2 != 0) and (abs(complex(diff2)) > 1e-9)
        except Exception:
            is_non_trivial = (diff2 != 0)
            
        # Check if the automorphism has order 2 (i.e., tau(tau(zeta_n)) == zeta_n)
        ttz = tau(tz)
        diff3 = sympy.simplify(ttz - zeta_n)
        try:
            order_2 = (diff3 == 0) or (abs(complex(diff3)) < 1e-9)
        except Exception:
            order_2 = (diff3 == 0)
            
        q = maps_to_inv and is_non_trivial and order_2
        neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]