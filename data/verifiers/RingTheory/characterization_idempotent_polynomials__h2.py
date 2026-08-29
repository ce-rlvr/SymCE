import sympy
from sympy import Poly

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a counterexample to the false conjecture:
    "f^2 = f if and only if f is a constant polynomial whose single coefficient is an idempotent element in R"
    where R is a commutative ring.
    
    The witness should be a polynomial (e.g., a sympy.Poly object).
    """
    try:
        # H1: R is a commutative ring.
        # In SymPy, the domain of a Poly is always a commutative ring.
        # We just verify the witness is a polynomial.
        h1_ok = isinstance(witness, Poly)
    except Exception:
        h1_ok = False

    try:
        # Evaluate the conclusion:
        # P: f^2 = f
        # Q: f is a constant polynomial whose single coefficient is an idempotent element in R
        
        # Check P: f^2 == f
        f_sq = witness * witness
        P = (f_sq == witness)
        
        # Check Q: f is constant AND its coefficient is idempotent
        is_constant = witness.is_constant()
        if is_constant:
            # Get the constant term
            c = witness.coeff_monomial(1)
            # Check if c is idempotent in the domain
            c_is_idempotent = (c * c == c)
            Q = c_is_idempotent
        else:
            Q = False
            
        # The conclusion is P <-> Q.
        # The negation of the conclusion is True if P != Q.
        neg_q_ok = (P != Q)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: It is NOT the case that (f^2 = f iff f is a constant polynomial whose single coefficient is an idempotent element in R)"
]

N_HYP = 1
NEG_Q_INDEX = 1