import sympy as sp
from sympy import re
from sympy.ntheory import factorint

def dedekind_psi(n):
    """Compute the Dedekind psi function for an integer n."""
    if n < 1:
        return 0
    res = n
    for p in factorint(n):
        res *= (1 + 1/p)
    return int(res)

def conditions(witness):
    """
    Check the remaining hypotheses and the negated conclusion.
    The true theorem states that for the Dedekind psi function, the Dirichlet series
    equals zeta(s)zeta(s-1)/zeta(2s) for Re(s) > 2.
    If the conjecture drops the hypothesis that psi is the Dedekind psi function,
    the witness would be a tuple (psi_function, s).
    """
    # Unpack witness
    if isinstance(witness, tuple) and len(witness) == 2:
        psi, s = witness
    else:
        psi = dedekind_psi
        s = witness

    # H_1: Re(s) > 2
    try:
        h1_ok = bool(re(s) > 2)
    except Exception:
        h1_ok = False

    # neg_Q: The conclusion FAILS at the witness.
    # The conclusion is that the Dirichlet series of psi equals zeta(s)zeta(s-1)/zeta(2s).
    # Since Dirichlet series are equal iff their coefficients are equal, and the RHS
    # coefficients are exactly the Dedekind psi function, the conclusion holds iff
    # psi(n) == dedekind_psi(n) for all n >= 1.
    # We check the first few coefficients to verify if the conclusion fails.
    try:
        match = True
        for n in range(1, 50):
            if psi(n) != dedekind_psi(n):
                match = False
                break
        neg_q_ok = not match
    except Exception:
        # If evaluating psi(n) fails, it does not satisfy the conclusion's formula.
        neg_q_ok = True

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: Re(s) > 2",
    "¬Q: The Dirichlet series of psi does not equal zeta(s)zeta(s-1)/zeta(2s)"
]

N_HYP = 1
NEG_Q_INDEX = 1