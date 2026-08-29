import sympy
from sympy import Matrix, eye, zeros, Symbol, minpoly, Poly, factor_list

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: Let V be a finite-dimensional vector space over a field F
    # We interpret this as the witness being a square matrix, which implicitly defines V = F^n.
    try:
        if not hasattr(witness, 'is_square'):
            h1 = False
        else:
            h1 = bool(witness.is_square)
    except Exception:
        h1 = False

    # ¬Q: T is diagonalizable if and only if the minimal polynomial of T is a product of distinct linear factors over F
    try:
        x = Symbol('x')
        p = minpoly(witness, x)
        poly_p = Poly(p, x)
        domain = poly_p.domain.get_field()
        
        # Factor the minimal polynomial over the field of the matrix entries
        factors = factor_list(p, domain=domain)
        
        is_prod_distinct_linear = True
        for f, m in factors[1]:
            if Poly(f, x).degree() != 1 or m != 1:
                is_prod_distinct_linear = False
                break
                
        # SymPy's is_diagonalizable() checks diagonalizability over the algebraic closure (e.g., C)
        is_diag = bool(witness.is_diagonalizable())
        
        # The conclusion is the equivalence of these two properties
        q = (is_diag == is_prod_distinct_linear)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "¬Q: The equivalence between T being diagonalizable and its minimal polynomial being a product of distinct linear factors over F fails"
]

N_HYP = 1
NEG_Q_INDEX = 1