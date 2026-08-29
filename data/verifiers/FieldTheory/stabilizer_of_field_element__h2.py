import sympy
from sympy import Symbol, roots, degree, minpoly, Expr, Poly
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

x = Symbol('x')

def conditions(witness):
    """
    Given a witness, checks if it satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to represent (E, F, alpha, G) or simply (theta, alpha) where theta generates E over Q.
    """
    try:
        theta, alpha = None, None
        if isinstance(witness, dict):
            theta = witness.get('E', witness.get('theta'))
            alpha = witness.get('alpha')
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 4:
                # Common pattern: (E, F, alpha, G)
                theta = witness[0]
                alpha = witness[2]
            elif len(witness) >= 2:
                # Fallback pattern: (theta, alpha)
                theta = witness[0]
                alpha = witness[1]
        else:
            return [False, False]

        if theta is None or alpha is None:
            return [False, False]

        # Extract primitive element if a NumberField object was passed
        if hasattr(theta, 'ext'):
            theta = theta.ext

        # Convert Poly to Expr if necessary
        if isinstance(theta, Poly):
            theta = theta.as_expr()

        # If theta is a polynomial expression, take its first root to be the generator
        if isinstance(theta, Expr) and theta.free_symbols:
            sym = list(theta.free_symbols)[0]
            rts = roots(theta, sym)
            if rts:
                theta = list(rts.keys())[0]

    except Exception:
        return [False, False]

    # H_1: E/F is a finite Galois extension
    # We interpret E = Q(theta) and F = Q. We check if Q(theta)/Q is Galois.
    h1 = False
    try:
        p_theta = minpoly(theta, x)
        deg_theta = degree(p_theta, x)
        if deg_theta >= 1:
            rts = roots(p_theta, x)
            # Must split completely into linear factors
            if sum(rts.values()) == deg_theta:
                is_galois = True
                # Check if all roots are actually in Q(theta)
                for r in rts.keys():
                    # If r is in Q(theta), then Q(theta, r) = Q(theta), so degree remains deg_theta.
                    # We use theta + c*r as a primitive element for Q(theta, r).
                    deg_ext = max(degree(minpoly(theta + c * r, x), x) for c in range(1, 6))
                    if deg_ext > deg_theta:
                        is_galois = False
                        break
                h1 = is_galois
    except Exception:
        h1 = False

    # ¬Q: The conclusion fails.
    # The conclusion assumes alpha is in E. If alpha is not in E, F(alpha) is not an intermediate field,
    # and the stabilizer is not identically Gal(E/F(alpha)).
    # We check if alpha is NOT in Q(theta).
    neg_q = False
    try:
        p_alpha = minpoly(alpha, x)
        deg_alpha = degree(p_alpha, x)
        if deg_alpha >= 1:
            # If alpha is not in Q(theta), the degree of Q(theta, alpha) over Q will be strictly > deg_theta.
            deg_both = max(degree(minpoly(theta + c * alpha, x), x) for c in range(1, 6))
            if deg_both > deg_theta:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: E/F is a finite Galois extension with Galois group G",
    "¬Q: The stabilizer subgroup of alpha under G is not identically Gal(E/F(alpha)) (e.g., alpha is not in E)"
]

N_HYP = 1
NEG_Q_INDEX = 1