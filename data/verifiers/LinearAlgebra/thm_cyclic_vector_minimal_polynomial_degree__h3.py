import sympy
from sympy import Symbol, factor_list, Poly
from sympy.matrices import MatrixBase, eye, zeros, Matrix

# Standard linear algebra objects that might be used as witnesses
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: V is a finite-dimensional vector space of dimension n
    # We represent the vector space and the operator via a matrix.
    try:
        h1 = isinstance(witness, MatrixBase)
    except Exception:
        h1 = False

    # H_2: T is a linear operator on V
    # This means the matrix must be square and have dimension > 0.
    try:
        h2 = h1 and witness.is_square and witness.shape[0] > 0
    except Exception:
        h2 = False

    # ¬Q: The minimal polynomial of T does NOT have degree n OR does NOT coincide with the characteristic polynomial.
    # For a square matrix of size n, the minimal polynomial divides the characteristic polynomial.
    # They coincide if and only if they have the same degree (which is n).
    # Thus, the conclusion fails iff the minimal polynomial has degree strictly less than n.
    # This happens iff there is some irreducible factor of the characteristic polynomial with multiplicity > 1
    # such that dividing the characteristic polynomial by one instance of this factor still annihilates the matrix.
    try:
        neg_q = False
        if h2:
            n = witness.shape[0]
            x = Symbol('x')
            cp = witness.charpoly(x).as_expr()
            coeff, factors = factor_list(cp)
            
            for f, e in factors:
                if e > 1:
                    # Construct the test polynomial: charpoly / f
                    test_expr = coeff
                    for f_inner, e_inner in factors:
                        if f_inner == f:
                            test_expr *= f_inner**(e_inner - 1)
                        else:
                            test_expr *= f_inner**e_inner
                    
                    p = Poly(test_expr, x)
                    res = zeros(n, n)
                    
                    # Evaluate the test polynomial at the matrix witness
                    for degs, c in p.terms():
                        d = degs[0]
                        if d == 0:
                            res += c * eye(n)
                        else:
                            res += c * (witness**d)
                    
                    # Check if the resulting matrix is the zero matrix
                    is_zero = True
                    for i in range(n):
                        for j in range(n):
                            if res[i, j] != 0:
                                if res[i, j].simplify() != 0:
                                    is_zero = False
                                    break
                        if not is_zero:
                            break
                    
                    if is_zero:
                        neg_q = True
                        break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space of dimension n",
    "H_2: T is a linear operator on V",
    "¬Q: The minimal polynomial of T has degree < n (does not coincide with characteristic polynomial)"
]

N_HYP = 2
NEG_Q_INDEX = 2