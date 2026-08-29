import itertools
from sympy import Matrix, eye, zeros, gcd, Rational, Integer, Symbol

# Top-level setup for witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if len(witness) != 4:
            return [False, False, False]
        a, b, x, y = witness
    except Exception:
        return [False, False, False]
    
    is_matrix = hasattr(a, 'is_Matrix') and a.is_Matrix
    
    # H_1: Let a and b be elements of R.
    try:
        if is_matrix:
            if not (hasattr(b, 'is_Matrix') and b.is_Matrix and 
                    hasattr(x, 'is_Matrix') and x.is_Matrix and 
                    hasattr(y, 'is_Matrix') and y.is_Matrix):
                H1 = False
            elif a.shape != b.shape or a.shape != x.shape or a.shape != y.shape:
                H1 = False
            elif a.rows != a.cols:
                H1 = False
            else:
                H1 = True
        else:
            H1 = True
    except Exception:
        H1 = False

    # H_2: Assume there exist elements x, y \in R such that ax + by = 1.
    try:
        if is_matrix and H1:
            I = eye(a.rows)
            H2 = bool(a * x + b * y == I)
        else:
            H2 = bool(a * x + b * y == 1)
    except Exception:
        H2 = False

    # neg_Q: The principal left ideals (a) and (b) are NOT comaximal in R.
    # For matrices, Ra + Rb = R iff the block matrix [a \n b] has a left inverse.
    try:
        if is_matrix and H1:
            n = a.rows
            stacked = a.col_join(b)
            
            if stacked.rank() < n:
                # Rank is less than n, so it cannot have a left inverse over any commutative ring.
                neg_Q = True
            else:
                # Check if it has a left inverse over Z by checking the gcd of all n x n minors.
                def is_int(m):
                    if isinstance(m, int):
                        return True
                    if hasattr(m, 'is_Integer') and m.is_Integer:
                        return True
                    return False
                
                def is_int_matrix(mat):
                    for i in range(mat.rows):
                        for j in range(mat.cols):
                            if not is_int(mat[i, j]):
                                return False
                    return True

                if is_int_matrix(a) and is_int_matrix(b) and is_int_matrix(x) and is_int_matrix(y):
                    minors = []
                    for rows in itertools.combinations(range(2 * n), n):
                        submat = stacked.extract(rows, range(n))
                        minors.append(submat.det())
                    
                    g = minors[0]
                    for m in minors[1:]:
                        g = gcd(g, m)
                    
                    # If gcd is not 1 or -1, there is no left inverse over Z.
                    neg_Q = (g not in (1, -1))
                else:
                    # Over a field, full rank implies a left inverse exists.
                    neg_Q = False
        else:
            # For commutative rings, ax + by = 1 implies (a) + (b) = R.
            neg_Q = False
    except Exception:
        neg_Q = False

    return [H1, H2, neg_Q]

CONDITION_LABELS = [
    "H_1: a and b are elements of R",
    "H_2: There exist elements x, y in R such that ax + by = 1",
    "¬Q: The principal ideals (a) and (b) are not comaximal in R"
]

N_HYP = 2
NEG_Q_INDEX = 2