import sympy
import sympy.combinatorics.named_groups
import sympy.matrices
from sympy.abc import x, y, z

# Top-level setup for standard algebra objects
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R has a multiplicative identity",
    "H_3: R is an Artinian ring",
    "¬Q: P is not a maximal ideal"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    """
    Evaluates the hypotheses and negated conclusion for the given witness.
    The witness is expected to be a tuple (R_obj, P_obj) representing:
    - R = Z/nZ and P = <p>  (if R_obj=n, P_obj=p are integers)
    - R = Q[x]/<f> and P = <g> (if R_obj=f, P_obj=g are polynomials)
    """
    try:
        if isinstance(witness, dict):
            if "R" in witness and "P" in witness:
                R_obj = witness["R"]
                P_obj = witness["P"]
            elif "n" in witness and "p" in witness:
                R_obj = witness["n"]
                P_obj = witness["p"]
            else:
                return [False, False, False, False]
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            R_obj, P_obj = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # Try integer case: R = Z/nZ, P = <p>
    try:
        n = abs(int(R_obj))
        p = abs(int(P_obj))
        is_int = True
    except Exception:
        is_int = False

    if is_int:
        try:
            h1 = (n != 1)
        except Exception:
            h1 = False
            
        try:
            h2 = (n != 1)
        except Exception:
            h2 = False
            
        try:
            h3 = (n >= 2)
        except Exception:
            h3 = False
            
        try:
            if n == 0:
                neg_q = not sympy.isprime(p)
            else:
                g = sympy.gcd(p, n)
                neg_q = not sympy.isprime(g)
        except Exception:
            neg_q = False
            
        return [h1, h2, h3, neg_q]

    # Try polynomial case: R = Q[x]/<R_expr>, P = <P_expr>
    try:
        R_expr = sympy.sympify(R_obj)
        P_expr = sympy.sympify(P_obj)
        
        if R_expr == 0:
            h1 = True
            h2 = True
            h3 = False
        elif R_expr.is_constant():
            h1 = False
            h2 = False
            h3 = False
        else:
            h1 = True
            h2 = True
            h3 = True
            
        g = sympy.gcd(P_expr, R_expr)
        g_poly = sympy.Poly(g, domain='QQ')
        neg_q = not g_poly.is_irreducible
        
        return [h1, h2, h3, neg_q]
    except Exception:
        pass

    return [False, False, False, False]