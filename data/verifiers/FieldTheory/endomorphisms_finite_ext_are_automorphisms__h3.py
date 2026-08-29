import sympy as sp
from sympy.abc import x, y, z, t
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for standard algebra objects
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
    "H_1: E/F is a finite field extension",
    "H_2: sigma is a field homomorphism from E to E",
    "¬Q: sigma is not surjective or not an F-automorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture:
    "If E/F is a finite field extension and sigma: E -> E is a field homomorphism, 
    then sigma is surjective and therefore an F-automorphism of E."
    """
    # 1. Try dictionary format
    if isinstance(witness, dict):
        try:
            if 'is_finite_extension' in witness:
                h1 = bool(witness.get('is_finite_extension', False))
                h2 = bool(witness.get('is_homomorphism', False))
                is_surjective = bool(witness.get('is_surjective', True))
                is_F_automorphism = bool(witness.get('is_F_automorphism', True))
                neg_q = not (is_surjective and is_F_automorphism)
                return [h1, h2, neg_q]
        except Exception:
            pass

    # 2. Try object with attributes format
    try:
        if hasattr(witness, 'is_finite_extension'):
            h1 = bool(getattr(witness, 'is_finite_extension', False))
            h2 = bool(getattr(witness, 'is_homomorphism', False))
            is_surjective = bool(getattr(witness, 'is_surjective', True))
            is_F_automorphism = bool(getattr(witness, 'is_F_automorphism', True))
            neg_q = not (is_surjective and is_F_automorphism)
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 3. Try tuple (p, f) format representing E = F = F_p(t) and sigma(t) = f(t)
    # This is the standard explicit counterexample in positive characteristic.
    if isinstance(witness, tuple) and len(witness) == 2:
        try:
            p, f = witness
            if isinstance(p, int) and sp.isprime(p):
                f_expr = sp.sympify(f)
                free_syms = f_expr.free_symbols
                
                if len(free_syms) > 1:
                    return [False, False, False]
                elif len(free_syms) == 1:
                    var = list(free_syms)[0]
                else:
                    var = sp.Symbol('t')
                
                # H1: E = F is a finite extension (degree 1)
                h1 = True  
                
                # H2: sigma is a field homomorphism iff f(t) is not a constant
                h2 = len(free_syms) > 0  
                
                f_cancel = sp.cancel(f_expr)
                n, d = f_cancel.as_numer_denom()
                
                if n.is_polynomial(var) and d.is_polynomial(var):
                    deg_n = sp.degree(n, var)
                    deg_d = sp.degree(d, var)
                    # Surjective iff the rational degree is 1
                    is_surjective = (max(deg_n, deg_d) == 1)
                else:
                    is_surjective = False
                
                # It is an F-automorphism iff it is surjective and fixes F (i.e., f(t) = t)
                is_F_auto = is_surjective and (sp.cancel(f_expr - var) == 0)
                
                # The conclusion fails if it is not surjective OR not an F-automorphism
                neg_q = not (is_surjective and is_F_auto)
                
                return [h1, h2, neg_q]
        except Exception:
            pass

    return [False, False, False]