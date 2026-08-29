import math

# Top-level setup
# No named bindings needed for Number Theory; integers are used directly.

CONDITION_LABELS = [
    "H_1: a and m are positive coprime integers",
    "H_2: n is the index of the final convergent such that p_n/q_n = a/m",
    "¬Q: The modular inverse of a modulo m is NOT congruent to (-1)^{n-1} q_{n-1} (mod m)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    a = None
    m = None
    cf = None
    p_seq = None
    q_seq = None
    n = None

    # Extract properties from the witness
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            m = witness.get('m')
            cf = witness.get('cf')
            p_seq = witness.get('p')
            q_seq = witness.get('q')
            n = witness.get('n')
        else:
            a = getattr(witness, 'a', None)
            m = getattr(witness, 'm', None)
            cf = getattr(witness, 'cf', None)
            p_seq = getattr(witness, 'p', None)
            q_seq = getattr(witness, 'q', None)
            n = getattr(witness, 'n', None)
            
        if a is None or m is None:
            if isinstance(witness, tuple):
                if len(witness) == 3:
                    a, m, cf = witness
                elif len(witness) == 4:
                    a, m, n, cf = witness
    except Exception:
        pass

    # Compute convergents if a continued fraction is provided
    try:
        if cf is not None:
            p_seq = {-2: 0, -1: 1}
            q_seq = {-2: 1, -1: 0}
            for i, c in enumerate(cf):
                p_seq[i] = c * p_seq[i-1] + p_seq[i-2]
                q_seq[i] = c * q_seq[i-1] + q_seq[i-2]
            if n is None:
                n = len(cf) - 1
    except Exception:
        pass

    # Normalize p_seq and q_seq to dictionaries if they are lists
    try:
        if isinstance(p_seq, (list, tuple)):
            p_seq = {i: p_seq[i] for i in range(len(p_seq))}
            if -1 not in p_seq: p_seq[-1] = 1
            if -2 not in p_seq: p_seq[-2] = 0
        if isinstance(q_seq, (list, tuple)):
            q_seq = {i: q_seq[i] for i in range(len(q_seq))}
            if -1 not in q_seq: q_seq[-1] = 0
            if -2 not in q_seq: q_seq[-2] = 1
    except Exception:
        pass

    # H_1: a and m are positive coprime integers
    try:
        h1 = isinstance(a, int) and isinstance(m, int) and a > 0 and m > 0 and math.gcd(a, m) == 1
    except Exception:
        h1 = False

    # H_2: n is the index of the final convergent such that p_n/q_n = a/m
    try:
        pn = p_seq[n]
        qn = q_seq[n]
        h2 = (qn != 0) and (pn * m == qn * a)
        if cf is not None:
            h2 = h2 and (n == len(cf) - 1) and all(isinstance(c, int) for c in cf)
        else:
            max_k = max([k for k in p_seq.keys() if k >= 0])
            h2 = h2 and (n == max_k)
    except Exception:
        h2 = False

    # ¬Q: The modular inverse of a modulo m is NOT congruent to (-1)^{n-1} q_{n-1} (mod m)
    try:
        if m == 1:
            inv_a = 0
        else:
            inv_a = pow(a, -1, m)
            
        q_n_minus_1 = q_seq[n-1]
        sign = -1 if (n - 1) % 2 != 0 else 1
        formula_val = sign * q_n_minus_1
        
        neg_q = (inv_a % m) != (formula_val % m)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]