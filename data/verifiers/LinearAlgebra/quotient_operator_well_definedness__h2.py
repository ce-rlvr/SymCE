import itertools
from sympy import Matrix, eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Group theory
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

# Linear algebra
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: V is a vector space",
    "H_2: W is a subspace of V",
    "¬Q: The equivalence 'T_bar is well-defined linear operator iff W is T-invariant' fails"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    """
    witness is expected to be a tuple: (n, W_basis, T)
    where:
      n: int, dimension of the vector space V = R^n
      W_basis: list of n x 1 sympy Matrices spanning the subspace W
      T: callable T(v) representing the mapping V -> V
    """
    try:
        n, W_basis, T = witness
    except Exception:
        return [False, False, False]
        
    # H1: V is a vector space
    try:
        h1 = isinstance(n, int) and n > 0
    except Exception:
        h1 = False
        
    # H2: W is a subspace of V
    try:
        h2 = True
        if not isinstance(W_basis, list):
            h2 = False
        else:
            for w in W_basis:
                if not isinstance(w, Matrix) or w.shape != (n, 1):
                    h2 = False
                    break
    except Exception:
        h2 = False
        
    if not (h1 and h2):
        return [h1, h2, False]
        
    try:
        if len(W_basis) > 0:
            W_matrix = W_basis[0]
            for w in W_basis[1:]:
                W_matrix = W_matrix.row_join(w)
        else:
            W_matrix = Matrix(n, 0, [])
            
        def in_W(v):
            return W_matrix.rank() == W_matrix.row_join(v).rank()
            
        def safe_T(v):
            res = T(v)
            if not isinstance(res, Matrix):
                res = Matrix(res)
            return res
            
        # Check P: W is T-invariant
        coeffs = [-2, -1, 0, 1, 2]
        P_true = True
        if len(W_basis) > 0:
            for i, c in enumerate(itertools.product(coeffs, repeat=len(W_basis))):
                if i >= 50: break
                w = sum((c[j]*W_basis[j] for j in range(len(W_basis))), Matrix.zeros(n, 1))
                if not in_W(safe_T(w)):
                    P_true = False
                    break
        else:
            if not in_W(safe_T(Matrix.zeros(n, 1))):
                P_true = False
                
        # Check Q: \bar{T} is well-defined and linear
        Q_well_defined = True
        Q_linear = True
        
        # Generate test vectors in V
        V_basis = [eye(n)[:, i] for i in range(n)]
        V_test_vectors = []
        for c in itertools.product([-1, 0, 1], repeat=n):
            v = sum((c[i]*V_basis[i] for i in range(n)), Matrix.zeros(n, 1))
            V_test_vectors.append(v)
            if len(V_test_vectors) >= 27:
                break
                
        # Generate test vectors in W
        W_test_vectors = []
        if len(W_basis) > 0:
            for c in itertools.product([-1, 0, 1], repeat=len(W_basis)):
                w = sum((c[i]*W_basis[i] for i in range(len(W_basis))), Matrix.zeros(n, 1))
                W_test_vectors.append(w)
                if len(W_test_vectors) >= 27:
                    break
        else:
            W_test_vectors.append(Matrix.zeros(n, 1))
            
        # Test well-definedness: T(v + w) - T(v) \in W
        for v in V_test_vectors:
            for w in W_test_vectors:
                if not in_W(safe_T(v + w) - safe_T(v)):
                    Q_well_defined = False
                    break
            if not Q_well_defined:
                break
                
        # Test linearity: T(a*v1 + b*v2) - (a*T(v1) + b*T(v2)) \in W
        if Q_well_defined:
            for v1 in V_test_vectors:
                for v2 in V_test_vectors:
                    for a in [-1, 0, 1, 2]:
                        for b in [-1, 0, 1, 2]:
                            diff = safe_T(a*v1 + b*v2) - (a*safe_T(v1) + b*safe_T(v2))
                            if not in_W(diff):
                                Q_linear = False
                                break
                        if not Q_linear:
                            break
                    if not Q_linear:
                        break
                if not Q_linear:
                    break
                    
        Q_true = Q_well_defined and Q_linear
        
        # The conclusion is the equivalence P <-> Q.
        # The negation of the conclusion is that the equivalence fails (P != Q).
        neg_q = (P_true != Q_true)
        
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]