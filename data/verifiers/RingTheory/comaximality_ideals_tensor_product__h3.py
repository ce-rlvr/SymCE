import sympy as sp

# Top-level setup
Q = sp.QQ

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample.
    
    The witness should be a dictionary representing a finite-dimensional 
    commutative algebra A over the field R = Q. We fix B = Q.
    
    Expected keys in witness:
      'n': int, dimension of A over Q
      'mult': 3D list of size n x n x n, where mult[i][j][k] is the coefficient 
              of e_k in the product e_i * e_j.
      'identity': list of length n, the identity element of A.
      'I_basis': list of lists, basis vectors for the Q-subspace I.
      'J_basis': list of lists, basis vectors for the Q-subspace J.
    """
    try:
        if not isinstance(witness, dict):
            return [False, False, False, False]
            
        n = int(witness['n'])
        if n <= 0:
            return [False, False, False, False]
        
        def to_sym(val):
            if isinstance(val, (int, sp.Integer, sp.Rational)):
                return val
            if isinstance(val, float):
                return sp.Rational(str(val))
            return sp.sympify(val)

        mult = [[[to_sym(c) for c in row] for row in mat] for mat in witness['mult']]
        identity = [to_sym(c) for c in witness['identity']]
        I_basis = [[to_sym(c) for c in row] for row in witness['I_basis']]
        J_basis = [[to_sym(c) for c in row] for row in witness['J_basis']]
        
        if len(mult) != n or any(len(row) != n for row in mult) or any(len(col) != n for row in mult for col in row):
            return [False, False, False, False]
        if len(identity) != n:
            return [False, False, False, False]
        if any(len(row) != n for row in I_basis):
            return [False, False, False, False]
        if any(len(row) != n for row in J_basis):
            return [False, False, False, False]
            
    except Exception:
        return [False, False, False, False]

    # H1: R is a commutative ring
    # We fix R = Q, which is a commutative ring.
    h1 = True

    # H2: A and B are commutative R-algebras
    # We fix B = Q, which is a commutative Q-algebra.
    # We check if A is a commutative Q-algebra.
    h2 = True
    try:
        # Commutativity
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if sp.expand(mult[i][j][k] - mult[j][i][k]) != 0:
                        h2 = False
                        break
                if not h2: break
            if not h2: break

        if h2:
            # Associativity
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        left = [0]*n
                        for m in range(n):
                            for p in range(n):
                                left[p] += mult[i][j][m] * mult[m][k][p]
                        right = [0]*n
                        for m in range(n):
                            for p in range(n):
                                right[p] += mult[j][k][m] * mult[i][m][p]
                        if any(sp.expand(left[p] - right[p]) != 0 for p in range(n)):
                            h2 = False
                            break
                    if not h2: break
                if not h2: break

        if h2:
            # Identity
            for i in range(n):
                res = [0]*n
                for j in range(n):
                    for k in range(n):
                        res[k] += identity[j] * mult[j][i][k]
                expected = [0]*n
                expected[i] = 1
                if any(sp.expand(res[k] - expected[k]) != 0 for k in range(n)):
                    h2 = False
                    break
    except Exception:
        h2 = False

    # H3: I + J = A
    h3 = False
    try:
        vectors = I_basis + J_basis
        if vectors:
            M = sp.Matrix(vectors)
            if M.rank() == n:
                h3 = True
        else:
            if n == 0:
                h3 = True
    except Exception:
        h3 = False

    # neg_Q: The extended ideals I \otimes_R B and J \otimes_R B are NOT comaximal in A \otimes_R B.
    # Since B = Q, A \otimes_R B = A, and the extended ideals are just I and J.
    # For them to be comaximal ideals, they must BE ideals.
    # Since I + J = A, if they are both ideals, they are comaximal ideals.
    # So neg_Q is True iff I is not an ideal OR J is not an ideal.
    neg_q = False
    try:
        def is_ideal(basis):
            if not basis:
                return True
            M_basis = sp.Matrix(basis)
            rank_basis = M_basis.rank()
            for v in basis:
                for i in range(n):
                    prod = [0]*n
                    for j in range(n):
                        for k in range(n):
                            prod[k] += v[j] * mult[i][j][k]
                    M_test = sp.Matrix(basis + [prod])
                    if M_test.rank() > rank_basis:
                        return False
            return True

        I_is_ideal = is_ideal(I_basis)
        J_is_ideal = is_ideal(J_basis)
        
        neg_q = not (I_is_ideal and J_is_ideal)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: A and B are commutative R-algebras",
    "H_3: I + J = A",
    "¬Q: The extended ideals I \\otimes_R B and J \\otimes_R B are not comaximal in A \\otimes_R B"
]

N_HYP = 3
NEG_Q_INDEX = 3