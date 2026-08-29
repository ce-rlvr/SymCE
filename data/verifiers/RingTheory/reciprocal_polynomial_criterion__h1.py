import sympy
from sympy import Poly, degree, simplify, Symbol
from sympy.abc import x
from sympy.matrices import eye, zeros, Matrix

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Evaluates the remaining hypotheses and the negated conclusion for the given witness.
    
    Hypotheses:
      H1: f(x) is a polynomial of degree n >= 1
      H2: The constant term a_0 is non-zero
      H3: The reciprocal polynomial f*(x) = x^n f(1/x) is irreducible
      
    Negated Conclusion:
      neg_Q: f(x) is reducible
    """
    # Helper to check if an expression is a valid polynomial and get its degree
    def get_degree(expr):
        try:
            p = Poly(expr, x)
            return p.degree()
        except Exception:
            return -1

    # Helper to check irreducibility
    def check_irreducible(expr):
        try:
            if isinstance(expr, Poly):
                return expr.is_irreducible
            return sympy.is_irreducible(expr)
        except Exception:
            return False

    # H1: Degree n >= 1
    try:
        n = get_degree(witness)
        H1 = (n >= 1)
    except Exception:
        H1 = False

    # H2: Constant term a_0 is non-zero
    try:
        if isinstance(witness, Poly):
            a0 = witness.coeff_monomial(1)
        else:
            a0 = Poly(witness, x).coeff_monomial(1)
        
        if isinstance(a0, Matrix):
            H2 = not a0.is_zero_matrix
        else:
            H2 = (a0 != 0)
    except Exception:
        H2 = False

    # H3: Reciprocal polynomial f*(x) is irreducible
    try:
        if H1:
            if isinstance(witness, Poly):
                expr = witness.as_expr()
            else:
                expr = witness
            
            # Compute f*(x) = x^n * f(1/x)
            f_star_expr = simplify(x**n * expr.subs(x, 1/x))
            
            if isinstance(witness, Poly):
                f_star = Poly(f_star_expr, x, domain=witness.domain)
            else:
                f_star = f_star_expr
                
            H3 = check_irreducible(f_star)
        else:
            H3 = False
    except Exception:
        H3 = False

    # neg_Q: f(x) is reducible (not irreducible)
    try:
        neg_Q = not check_irreducible(witness)
    except Exception:
        neg_Q = False

    return [H1, H2, H3, neg_Q]

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial of degree n >= 1",
    "H_2: The constant term a_0 is non-zero",
    "H_3: The reciprocal polynomial f*(x) is irreducible",
    "¬Q: f(x) is reducible"
]

N_HYP = 3
NEG_Q_INDEX = 3