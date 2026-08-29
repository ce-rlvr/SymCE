import math

# Top-level setup
# (No special named objects required for this domain)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            a = witness['a']
            k = witness.get('k', None)
        elif isinstance(witness, (tuple, list)):
            a = witness[0]
            k = witness[1] if len(witness) > 1 else None
        else:
            a = witness
            k = None
    except Exception:
        a = None
        k = None

    # H1: a is an odd integer
    try:
        a_int = int(a)
        h1 = (a_int == a) and (a_int % 2 != 0)
    except Exception:
        h1 = False

    # neg_Q: The congruence x^2 \equiv a \pmod{2^k} has a solution if and only if a \equiv 1 \pmod 8
    try:
        a_int = int(a)
        if a_int != a:
            neg_q = False
        elif k is None:
            # If k is not provided, check if there exists any k that makes the conclusion fail.
            # We only need to check k=1 and k=2, because for k>=3, the iff holds.
            neg_q = False
            for test_k in [1, 2]:
                if test_k == 2:
                    has_sol = (a_int % 4 == 1)
                else:
                    has_sol = True
                if has_sol != (a_int % 8 == 1):
                    neg_q = True
                    break
        else:
            k_int = int(k)
            if k_int != k or k_int < 0:
                neg_q = False
            else:
                if k_int >= 3:
                    has_solution = (a_int % 8 == 1)
                elif k_int == 2:
                    has_solution = (a_int % 4 == 1)
                else:
                    has_solution = True
                    
                a_eq_1_mod_8 = (a_int % 8 == 1)
                neg_q = (has_solution != a_eq_1_mod_8)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a is an odd integer",
    "¬Q: The equivalence (x^2 ≡ a mod 2^k has a solution iff a ≡ 1 mod 8) fails"
]

N_HYP = 1
NEG_Q_INDEX = 1