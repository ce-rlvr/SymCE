import sympy

Z_omega = "Z[omega]"

def conditions(witness) -> list[bool]:
    try:
        h1_ok = bool(witness == "Z[omega]")
    except Exception:
        h1_ok = False

    try:
        if witness == "Z[omega]":
            is_euclidean = True
        else:
            is_euclidean = False
        neg_q_ok = not is_euclidean
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = ["H_1: R is the ring of Eisenstein integers", "¬Q: R is not a Euclidean domain"]
N_HYP = 1
NEG_Q_INDEX = 1