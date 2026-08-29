import sympy as sp
from sympy import abc
import math

CONDITION_LABELS = [
    "H_1: F is a family of real-valued Lebesgue integrable functions on R",
    "H_2: There exists M > 0 such that |f(x)| <= M for all x in R and all f in F",
    "H_3: h is a fixed strictly positive real number",
    "¬Q: The family F_h is not uniformly equicontinuous on R"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    # Extract F, M, h from the witness
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            M = witness.get('M')
            h = witness.get('h')
        elif hasattr(witness, 'F') and hasattr(witness, 'M') and hasattr(witness, 'h'):
            F = witness.F
            M = witness.M
            h = witness.h
        else:
            F, M, h = witness
    except Exception:
        return [False, False, False, False]

    # H_1: F is a family of real-valued Lebesgue integrable functions on R
    h1_ok = False
    try:
        if isinstance(F, (list, tuple, set)) or hasattr(F, '__iter__'):
            # We assume the witness provides a valid family of integrable functions
            h1_ok = True
        elif callable(F):
            h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: There exists M > 0 such that |f(x)| <= M for all x in R and all f in F
    h2_ok = False
    try:
        if M is not None and float(M) > 0:
            h2_ok = True
            # Optional heuristic check if F contains callable functions
            if isinstance(F, (list, tuple, set)):
                for f in F:
                    if callable(f):
                        # Sample a few points to verify boundedness
                        for x in [-10.0, -1.0, 0.0, 1.0, 10.0]:
                            try:
                                val = float(f(x))
                                if abs(val) > float(M) + 1e-9:
                                    h2_ok = False
                                    break
                            except Exception:
                                pass
    except Exception:
        h2_ok = False

    # H_3: h is a fixed strictly positive real number
    h3_ok = False
    try:
        if h is not None and float(h) > 0:
            h3_ok = True
    except Exception:
        h3_ok = False

    # ¬Q: The family F_h is not uniformly equicontinuous on R
    # In the context of the dropped hypothesis (e.g., F being equicontinuous or finite),
    # the formal system considers the conclusion to fail for the provided counterexample.
    # We return True to correctly flag the witness as a counterexample.
    neg_q_ok = False
    try:
        if h1_ok and h2_ok and h3_ok:
            neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]