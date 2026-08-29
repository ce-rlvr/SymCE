import math

# Top-level setup
# (No named bindings needed for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            k = witness.get('k')
            m = witness.get('m')
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                a, k, m = witness
            else:
                return [False, False]
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: a and k are integers such that a > 1 and k >= 1
    try:
        h1 = (type(a) is int and type(k) is int and a > 1 and k >= 1)
    except Exception:
        h1 = False

    # neg_Q: The modular inverse of a modulo m is NOT congruent to -\sum_{i=0}^{k-1} a^i \pmod m
    try:
        if type(m) is not int or m == 0:
            neg_q = True
        else:
            if math.gcd(a, m) != 1:
                neg_q = True
            else:
                inv_a = pow(a, -1, abs(m))
                geom_sum = sum(a**i for i in range(k))
                expected = (-geom_sum) % abs(m)
                neg_q = (inv_a % abs(m)) != expected
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a and k are integers such that a > 1 and k >= 1",
    "¬Q: The modular inverse of a modulo m is NOT congruent to -\\sum_{i=0}^{k-1} a^i \\pmod m"
]

N_HYP = 1
NEG_Q_INDEX = 1