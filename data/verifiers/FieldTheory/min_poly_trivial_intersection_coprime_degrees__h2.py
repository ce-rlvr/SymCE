import sympy
from sympy import eye, zeros, Matrix
from sympy.abc import x, y, z
from sympy import QQ, ZZ

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (F, alpha, beta) or a dictionary with these keys.
    """
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            alpha = witness.get('alpha')
            beta = witness.get('beta')
        else:
            F, alpha, beta = witness
    except Exception:
        return [False, False, False]

    # H_1: F is a field
    try:
        h1 = bool(hasattr(F, 'is_Field') and F.is_Field)
    except Exception:
        h1 = False

    da = None
    db = None

    # H_2: The degree of the minimal polynomial of α over F and the degree of the minimal polynomial of β over F are coprime integers
    try:
        if isinstance(alpha, Matrix) and isinstance(beta, Matrix):
            def minpoly_degree(M):
                n = M.shape[0]
                I = eye(n)
                vecs = [list(I)]
                for k in range(1, n + 1):
                    vecs.append(list(M**k))
                    mat = Matrix(vecs)
                    if mat.rank() < len(vecs):
                        return k
                return n
            
            da = minpoly_degree(alpha)
            db = minpoly_degree(beta)
        else:
            sym_x = sympy.Symbol('x')
            poly_a = sympy.minpoly(alpha, sym_x, domain=F)
            poly_b = sympy.minpoly(beta, sym_x, domain=F)
            da = sympy.degree(poly_a)
            db = sympy.degree(poly_b)
            
        h2 = bool(sympy.gcd(da, db) == 1)
    except Exception:
        h2 = False

    # ¬Q: The intersection F(α) ∩ F(β) is not equal to F
    try:
        if da is None or db is None:
            neg_q = False
        elif isinstance(alpha, Matrix) and isinstance(beta, Matrix):
            if alpha.shape != beta.shape:
                neg_q = False
            else:
                n = alpha.shape[0]
                I = eye(n)
                
                # F(α) and F(β) as algebras over F are spanned by powers up to their minimal polynomial degrees
                vecs_a = [list(alpha**k) for k in range(da)]
                vecs_b = [list(beta**k) for k in range(db)]
                
                vecs_union = vecs_a + vecs_b
                mat_union = Matrix(vecs_union)
                dim_union = mat_union.rank()
                
                # Grassmann's formula: dim(A ∩ B) = dim(A) + dim(B) - dim(A + B)
                dim_intersection = da + db - dim_union
                
                # F is isomorphic to the span of the identity matrix, which has dimension 1.
                # If the intersection has dimension > 1, it is strictly larger than F.
                neg_q = bool(dim_intersection > 1)
        else:
            # For algebraic numbers in a domain, the intersection of fields with coprime degrees is always F.
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: The degree of the minimal polynomial of α over F and the degree of the minimal polynomial of β over F are coprime integers",
    "¬Q: The intersection F(α) ∩ F(β) is not equal to F"
]

N_HYP = 2
NEG_Q_INDEX = 2