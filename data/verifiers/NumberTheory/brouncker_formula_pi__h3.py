import math

# Top-level setup
# (No specific named bindings required for this Number Theory domain)

def get_a0_b_a(witness):
    if isinstance(witness, dict):
        return witness.get('a0'), witness.get('b'), witness.get('a')
    elif isinstance(witness, (list, tuple)) and len(witness) == 3:
        return witness[0], witness[1], witness[2]
    else:
        return getattr(witness, 'a0', None), getattr(witness, 'b', None), getattr(witness, 'a', None)

def get_term(seq, n):
    if callable(seq):
        return seq(n)
    elif isinstance(seq, (list, tuple, dict)):
        return seq[n]
    elif hasattr(seq, '__getitem__'):
        return seq[n]
    else:
        raise TypeError("Sequence must be callable or subscriptable")

def eval_gcf_backwards(a0, b, a, N):
    val = 0.0
    for n in range(N, 0, -1):
        num = float(get_term(b, n))
        den = float(get_term(a, n))
        if den + val == 0:
            return None
        val = num / (den + val)
    return float(a0) + val

def conditions(witness) -> list[bool]:
    try:
        a0, b, a = get_a0_b_a(witness)
    except Exception:
        return [False, False, False]
        
    # H1: a0 == 1
    try:
        h1 = (a0 == 1)
    except Exception:
        h1 = False
        
    # H2: b_n = (2n-1)^2 for all n >= 1
    try:
        h2 = True
        for n in range(1, 100):
            if get_term(b, n) != (2*n - 1)**2:
                h2 = False
                break
    except Exception:
        h2 = False
        
    # neg_Q: does not converge to 4/pi
    try:
        v1 = eval_gcf_backwards(a0, b, a, 2000)
        v2 = eval_gcf_backwards(a0, b, a, 2001)
        if v1 is None or v2 is None:
            neg_q = True
        elif math.isnan(v1) or math.isnan(v2):
            neg_q = True
        else:
            target = 4.0 / math.pi
            # If both convergents are within 0.02 of 4/pi, we consider it converging to 4/pi.
            # (Brouncker's formula error at N=2000 is ~0.0005, well within 0.02)
            if abs(v1 - target) < 0.02 and abs(v2 - target) < 0.02:
                neg_q = False
            else:
                neg_q = True
    except Exception:
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A generalized continued fraction is defined with integer part a_0 = 1",
    "H_2: The partial numerators are b_n = (2n-1)^2 for all integers n >= 1",
    "¬Q: The generalized continued fraction does not converge to 4/pi"
]

N_HYP = 2
NEG_Q_INDEX = 2