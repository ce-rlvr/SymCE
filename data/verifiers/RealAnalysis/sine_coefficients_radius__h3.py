import sympy as sp

# Top-level setup
# No special named groups or matrices are needed for this real analysis theorem.

def conditions(witness) -> list[bool]:
    """
    Evaluates the remaining hypotheses and the negated conclusion for the given witness.
    
    Conjecture: If \theta is a real number and \theta is not an integer multiple of \pi,
    then the radius of convergence of the power series (with sine sequence coefficients) is exactly 1.
    
    Since for a_n = \sin(n\theta), the radius of convergence R = 1 for all real \theta \notin \pi\mathbb{Z},
    the only way the conclusion R=1 can fail for a real number under these hypotheses is if the sequence 
    was actually a_n = \sin(n \pi \theta) and the dropped hypothesis was \theta \notin \mathbb{Z}, 
    or if the witness is evaluated in a complex context where R = e^{-|Im(\theta)|} != 1.
    We check if R != 1 by checking if \sin(n\theta) evaluates to 0 (yielding R=\infty) 
    or if the witness has a non-zero imaginary part (yielding R < 1).
    """
    # H1: \theta is a real number
    try:
        h1_ok = bool(witness.is_real)
    except Exception:
        h1_ok = False

    # H2: \theta is not an integer multiple of \pi
    try:
        val = witness / sp.pi
        h2_ok = not bool(val.is_integer)
    except Exception:
        h2_ok = False

    # neg_Q: The radius of convergence is NOT exactly 1.
    # For a_n = \sin(n\theta), R = e^{-|Im(\theta)|}. If \theta is real, R = 1 unless \sin(n\theta) = 0 for all n.
    # If the sequence intended was \sin(n \pi \theta), then R = \infty when \theta is an integer.
    # We return True if the witness makes the radius of convergence differ from 1.
    try:
        # Check if it's a complex number with non-zero imaginary part (R < 1)
        if not witness.is_real:
            neg_q_ok = True
        # Check if it's an integer (in case the sequence is \sin(n \pi \theta), R = \infty)
        elif witness.is_integer:
            neg_q_ok = True
        # Check if it's a multiple of pi (though H2 excludes this, if evaluated independently, R = \infty)
        elif (witness / sp.pi).is_integer:
            neg_q_ok = True
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: \\theta is a real number",
    "H_2: \\theta is not an integer multiple of \\pi",
    "¬Q: The radius of convergence of the power series is not exactly 1"
]

N_HYP = 2
NEG_Q_INDEX = 2