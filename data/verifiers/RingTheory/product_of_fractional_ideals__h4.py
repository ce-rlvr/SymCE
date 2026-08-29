import sympy
from sympy.polys.domains import ZZ, QQ

# Top-level setup
# Witness should be a tuple (R, K, I, J) or a dict with these keys.
# R and K can be sympy.polys.domains.ZZ and QQ.
# I and J can be lists of generators (e.g., [1], [sympy.Rational(1, 2)]), or QQ, or ZZ.

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            K = witness.get('K')
            I = witness.get('I')
            J = witness.get('J')
        else:
            R, K, I, J = witness
    except Exception:
        return [False, False, False, False]

    # H1: R is an integral domain
    try:
        h1 = False
        if hasattr(R, 'is_Domain') and R.is_Domain:
            h1 = True
        elif hasattr(R, 'is_domain') and R.is_domain:
            h1 = True
        elif R in [ZZ, QQ]:
            h1 = True
    except Exception:
        h1 = False

    # H2: K is the field of fractions of R
    try:
        h2 = (K == R.get_field())
    except Exception:
        h2 = False

    def normalize_ideal(X, R):
        if X == R:
            return [1]
        return X

    def is_frac_ideal(X, R, K):
        if isinstance(X, (list, tuple, set)):
            for x in X:
                try:
                    if hasattr(K, 'from_sympy'):
                        K.from_sympy(sympy.sympify(x))
                    else:
                        if x not in K:
                            return False
                except Exception:
                    return False
            return True
        if X == K:
            return R == K
        return False

    # H3: I is a fractional ideal of R
    try:
        h3 = is_frac_ideal(normalize_ideal(I, R), R, K)
    except Exception:
        h3 = False

    # neg_Q: IJ is NOT a fractional ideal of R
    try:
        def product_ideal(I_norm, J_norm, K):
            if isinstance(I_norm, (list, tuple, set)) and isinstance(J_norm, (list, tuple, set)):
                return [sympy.sympify(i) * sympy.sympify(j) for i in I_norm for j in J_norm]
            
            def is_zero(X):
                if isinstance(X, (list, tuple, set)):
                    return all(sympy.sympify(x) == 0 for x in X)
                return False

            if I_norm == K and isinstance(J_norm, (list, tuple, set)):
                return [0] if is_zero(J_norm) else K
            if J_norm == K and isinstance(I_norm, (list, tuple, set)):
                return [0] if is_zero(I_norm) else K
            if I_norm == K and J_norm == K:
                return K
            
            return None
        
        IJ = product_ideal(normalize_ideal(I, R), normalize_ideal(J, R), K)
        neg_q = not is_frac_ideal(IJ, R, K)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: K is the field of fractions of R",
    "H_3: I is a fractional ideal of R",
    "¬Q: The product IJ is not a fractional ideal of R"
]

N_HYP = 3
NEG_Q_INDEX = 3