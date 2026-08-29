import math

# Top-level setup
# No special objects needed for this Number Theory conjecture.

def conditions(witness):
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness should provide:
      - m: a list or tuple of positive integers (m_1, ..., m_k)
      - x: an integer
      - M: an integer representing the upper bound for x
    """
    m, x, M = None, None, None
    try:
        if isinstance(witness, dict):
            m = witness.get('m')
            x = witness.get('x')
            M = witness.get('M')
        elif isinstance(witness, tuple):
            if len(witness) >= 3:
                m, x, M = witness[:3]
            elif len(witness) == 2:
                m, x = witness
        else:
            m = getattr(witness, 'm', None)
            x = getattr(witness, 'x', None)
            M = getattr(witness, 'M', None)
    except Exception:
        pass

    # H_1: m_1, m_2, ..., m_k are pairwise coprime positive integers
    h1 = False
    try:
        if isinstance(m, (list, tuple)) and all(isinstance(mi, int) and not isinstance(mi, bool) and mi > 0 for mi in m):
            h1 = True
            for i in range(len(m)):
                for j in range(i + 1, len(m)):
                    if math.gcd(m[i], m[j]) != 1:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H_2: x is an integer such that 0 <= x < M
    h2 = False
    try:
        if isinstance(x, int) and not isinstance(x, bool) and isinstance(M, (int, float)):
            if 0 <= x < M:
                h2 = True
    except Exception:
        h2 = False

    # ¬Q: The mixed-radix representation of x does not exist or is not unique
    # The conclusion states that x can be uniquely represented as:
    # x = a_1 + a_2 m_1 + a_3 m_1 m_2 + ... + a_k m_1 m_2 ... m_{k-1}
    # with 0 <= a_i < m_i.
    # We compute the unique candidate sequence using the division algorithm.
    # If the candidate sequence does not sum to x, then no valid sequence exists.
    neg_q = False
    try:
        if isinstance(m, (list, tuple)) and isinstance(x, int) and not isinstance(x, bool) and all(isinstance(mi, int) and mi > 0 for mi in m):
            candidate_a = []
            curr_x = x
            for mi in m:
                ai = curr_x % mi
                candidate_a.append(ai)
                curr_x = (curr_x - ai) // mi
            
            total = 0
            prod = 1
            for ai, mi in zip(candidate_a, m):
                total += ai * prod
                prod *= mi
            
            # If total != x, the representation fails to exist.
            neg_q = (total != x)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: m_1, m_2, ..., m_k are pairwise coprime positive integers",
    "H_2: x is an integer such that 0 <= x < M",
    "¬Q: The mixed-radix representation of x does not exist or is not unique"
]

N_HYP = 2
NEG_Q_INDEX = 2