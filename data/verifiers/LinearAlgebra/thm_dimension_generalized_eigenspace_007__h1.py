import sympy
from sympy import eye, zeros, MatrixBase

# Top-level setup for Linear Algebra
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture:
    Hypotheses:
      - T: V -> V is a linear operator
      - The characteristic polynomial of T splits completely over F
      - lambda is an eigenvalue of T with algebraic multiplicity m
    Conclusion:
      - The dimension of the generalized eigenspace corresponding to lambda is equal to m.
    """
    # Extract T, lam, m from the witness
    try:
        if isinstance(witness, dict):
            T = witness['T']
            lam = witness.get('lam', witness.get('lambda'))
            m = witness['m']
        elif isinstance(witness, tuple):
            T = witness[0]
            lam = witness[1]
            m = witness[2]
        else:
            T = getattr(witness, 'T', witness)
            lam = getattr(witness, 'lam', getattr(witness, 'lambda', None))
            m = getattr(witness, 'm', None)
    except Exception:
        return [False, False, False, False]

    # H_1: T: V -> V is a linear operator
    try:
        if hasattr(T, 'is_linear_operator'):
            h1 = T.is_linear_operator()
        elif hasattr(witness, 'is_linear_operator'):
            h1 = witness.is_linear_operator()
        else:
            h1 = isinstance(T, MatrixBase) and T.is_square
    except Exception:
        h1 = False

    # H_2: The characteristic polynomial of T splits completely over F
    try:
        if hasattr(T, 'charpoly_splits_completely'):
            h2 = T.charpoly_splits_completely()
        elif hasattr(witness, 'charpoly_splits_completely'):
            h2 = witness.charpoly_splits_completely()
        else:
            evs = T.eigenvals()
            h2 = sum(evs.values()) == T.shape[0]
    except Exception:
        h2 = False

    # H_3: lambda is an eigenvalue of T with algebraic multiplicity m
    try:
        if hasattr(T, 'algebraic_multiplicity'):
            h3 = T.algebraic_multiplicity(lam) == m
        elif hasattr(witness, 'algebraic_multiplicity'):
            h3 = witness.algebraic_multiplicity(lam) == m
        else:
            evs = T.eigenvals()
            h3 = (lam in evs) and (evs[lam] == m)
    except Exception:
        h3 = False

    # ¬Q: The dimension of the generalized eigenspace corresponding to lambda is NOT equal to m
    try:
        if hasattr(T, 'generalized_eigenspace_dim'):
            dim = T.generalized_eigenspace_dim(lam)
        elif hasattr(witness, 'generalized_eigenspace_dim'):
            dim = witness.generalized_eigenspace_dim(lam)
        else:
            n = T.shape[0]
            A = T - lam * eye(n)
            # The generalized eigenspace is the nullspace of (T - lambda*I)^n
            dim = n - (A**n).rank()
        neg_q = dim != m
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: T is a linear operator",
    "H_2: The characteristic polynomial of T splits completely over F",
    "H_3: lambda is an eigenvalue of T with algebraic multiplicity m",
    "¬Q: The dimension of the generalized eigenspace corresponding to lambda is not equal to m"
]

N_HYP = 3
NEG_Q_INDEX = 3