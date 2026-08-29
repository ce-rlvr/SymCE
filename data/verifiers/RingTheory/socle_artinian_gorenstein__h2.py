import sympy
from sympy import Matrix, eye, zeros, diag, Rational

# Top-level setup for witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If R is a commutative Artinian Gorenstein ring, then its socle is a 1-dimensional vector space."
    
    The witness should be a list of sympy.Matrix objects representing the regular 
    representation of the basis elements of a finite-dimensional algebra over Q.
    """
    try:
        M = [sympy.Matrix(m) for m in witness]
        n = len(M)
        if n == 0:
            return [False] * 4
        for m in M:
            if m.shape != (n, n):
                return [False] * 4
    except Exception:
        return [False] * 4

    # H_1: R is a commutative ring
    try:
        is_commutative = True
        for i in range(n):
            for j in range(n):
                for m in range(n):
                    if M[i][m, j] != M[j][m, i]:
                        is_commutative = False
                        break
                if not is_commutative: break
            if not is_commutative: break
        
        is_associative = True
        if is_commutative:
            for i in range(n):
                for j in range(n):
                    prod = M[i] * M[j]
                    expected = sympy.zeros(n, n)
                    for m in range(n):
                        expected += M[i][m, j] * M[m]
                    if prod != expected:
                        is_associative = False
                        break
                if not is_associative: break

        has_identity = False
        if is_commutative and is_associative:
            # Check if there is an identity element u such that sum u_k M_k = I_n
            A_eq = sympy.Matrix([[M[k][i, j] for k in range(n)] for i in range(n) for j in range(n)])
            b_eq = sympy.Matrix([1 if i == j else 0 for i in range(n) for j in range(n)])
            sols = sympy.linsolve((A_eq, b_eq))
            has_identity = len(sols) > 0

        h1_ok = is_commutative and is_associative and has_identity
    except Exception:
        h1_ok = False

    # H_2: R is an Artinian ring
    # Any finite-dimensional algebra over a field is Artinian. We enforce the field to be Q.
    try:
        is_artinian = True
        for m in M:
            for val in m:
                if not val.is_Rational:
                    is_artinian = False
                    break
            if not is_artinian: break
        h2_ok = h1_ok and is_artinian
    except Exception:
        h2_ok = False

    # H_3: R is a Gorenstein ring
    # A finite-dimensional commutative algebra over a field is Gorenstein iff it is a Frobenius algebra.
    try:
        if h2_ok:
            c = sympy.symbols(f'c0:{n}')
            B = sympy.zeros(n, n)
            for i in range(n):
                for j in range(n):
                    val = 0
                    for k in range(n):
                        val += c[k] * M[i][k, j]
                    B[i, j] = val
            det_B = sympy.expand(B.det())
            h3_ok = (det_B != 0)
        else:
            h3_ok = False
    except Exception:
        h3_ok = False

    # ¬Q: The socle of R is not a one-dimensional vector space over k
    try:
        if h2_ok:
            # Compute the trace form matrix
            T = sympy.zeros(n, n)
            for i in range(n):
                for j in range(n):
                    T[i, j] = (M[i] * M[j]).trace()
            
            # The Jacobson radical J is the nullspace of the trace form (since char = 0)
            J_basis = T.nullspace()
            
            if len(J_basis) == 0:
                # J is 0, so the socle is the annihilator of 0, which is the whole ring
                socle_dim = n
            else:
                # The socle is the annihilator of J
                stacked = []
                for y in J_basis:
                    M_y = sympy.zeros(n, n)
                    for m in range(n):
                        M_y += y[m, 0] * M[m]
                    stacked.append(M_y)
                
                Big_M = sympy.Matrix.vstack(*stacked)
                socle_basis = Big_M.nullspace()
                socle_dim = len(socle_basis)
                
            neg_q_ok = (socle_dim != 1)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is an Artinian ring",
    "H_3: R is a Gorenstein ring",
    "¬Q: The socle of R is not a one-dimensional vector space over k"
]

N_HYP = 3
NEG_Q_INDEX = 3