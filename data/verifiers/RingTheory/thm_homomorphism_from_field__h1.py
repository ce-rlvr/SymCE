import itertools

Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8

def conditions(witness) -> list[bool]:
    try:
        F_mod, S_mod, f_map = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(S_mod, int) and S_mod >= 2
    except Exception:
        h1 = False

    try:
        h2 = True
        if not (isinstance(F_mod, int) and F_mod >= 2):
            h2 = False
        elif f_map[1 % F_mod] != 1 % S_mod:
            h2 = False
        else:
            for a, b in itertools.product(range(F_mod), repeat=2):
                if f_map[(a + b) % F_mod] != (f_map[a] + f_map[b]) % S_mod:
                    h2 = False
                    break
                if f_map[(a * b) % F_mod] != (f_map[a] * f_map[b]) % S_mod:
                    h2 = False
                    break
    except Exception:
        h2 = False

    try:
        neg_q = len(set(f_map[k] for k in range(F_mod))) < F_mod
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S is a non-trivial ring where 1_S != 0_S",
    "H_2: f: F -> S is a ring homomorphism",
    "¬Q: f is not an injective ring homomorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2