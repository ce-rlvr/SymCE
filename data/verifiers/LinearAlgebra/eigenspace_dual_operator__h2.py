import sympy as sp

# Top-level setup for potential witness expressions
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    """
    Given a witness, checks if it satisfies the remaining hypotheses and falsifies the conclusion.
    The witness should be a tuple (T, lambda_) where T is a sympy Matrix and lambda_ is a scalar,
    or a dictionary {'T': T, 'lambda': lambda_}.
    """
    try:
        if isinstance(witness, dict):
            T = witness.get('T')
            lambda_ = witness.get('lambda')
        else:
            T, lambda_ = witness
            
        if not isinstance(T, sp.Matrix):
            return [False, False, False]
        n = T.shape[0]
        if T.shape != (n, n):
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: V is a finite-dimensional vector space over a field F
    # Implicitly true since T is a finite square matrix.
    h1_ok = True

    # H_2: lambda is an eigenvalue of T
    try:
        I = sp.eye(n)
        char_matrix = T - lambda_ * I
        h2_ok = sp.simplify(char_matrix.det()) == 0
    except Exception:
        h2_ok = False

    # ¬Q: E_lambda(T*) != Annihilator(Im(T - lambda I_V))
    try:
        # The false conjecture arises from confusing the dual operator with the adjoint operator.
        # We interpret V* as the space of row vectors and T* as the adjoint (conjugate transpose).
        # The action of T* on a row vector f is given by right multiplication: f * T*.
        
        # E_lambda(T*) = {f | f * T* = lambda * f}
        # This is the left nullspace of (T.H - lambda * I), 
        # which is the right nullspace of (T.H - lambda * I).T
        E_lambda_matrix = (T.H - lambda_ * I).transpose()
        
        # Annihilator of Im(T - lambda I) = {f | f * (T - lambda I) = 0}
        # This is the left nullspace of (T - lambda * I),
        # which is the right nullspace of (T - lambda * I).T
        Annihilator_matrix = (T - lambda_ * I).transpose()
        
        ns_E = E_lambda_matrix.nullspace()
        ns_A = Annihilator_matrix.nullspace()
        
        if len(ns_E) != len(ns_A):
            spaces_equal = False
        elif len(ns_E) == 0:
            spaces_equal = True
        else:
            M_E = sp.Matrix.hstack(*ns_E)
            M_A = sp.Matrix.hstack(*ns_A)
            M_both = sp.Matrix.hstack(M_E, M_A)
            # The spaces are equal if the rank of the combined basis equals the rank of one basis
            spaces_equal = (M_both.rank() == M_E.rank())
            
        neg_q_ok = not spaces_equal
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: lambda is an eigenvalue of T",
    "¬Q: E_lambda(T*) is not equal to the annihilator of Im(T - lambda I_V)"
]

N_HYP = 2
NEG_Q_INDEX = 2