import math
import itertools

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (m_list, a_list, x)
    """
    try:
        m_list, a_list, x = witness
    except Exception:
        return [False, False, False]
        
    # H_1: m_1, ..., m_k are pairwise coprime positive integers
    try:
        h1 = True
        if not isinstance(m_list, (list, tuple)) or len(m_list) == 0:
            h1 = False
        else:
            for m in m_list:
                if not isinstance(m, int) or isinstance(m, bool) or m <= 0:
                    h1 = False
                    break
            if h1:
                for m1, m2 in itertools.combinations(m_list, 2):
                    if math.gcd(m1, m2) != 1:
                        h1 = False
                        break
    except Exception:
        h1 = False

    # H_2: x is an integer satisfying x ≡ a_i (mod m_i) for all 1 <= i <= k
    try:
        h2 = True
        if not isinstance(a_list, (list, tuple)) or len(a_list) != len(m_list):
            h2 = False
        elif not isinstance(x, int) or isinstance(x, bool):
            h2 = False
        else:
            for a, m in zip(a_list, m_list):
                if not isinstance(a, int) or isinstance(a, bool):
                    h2 = False
                    break
                if (x - a) % m != 0:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # ¬Q: The integer x is NOT coprime to the product M = m_1 * m_2 * ... * m_k
    try:
        M = math.prod(m_list)
        neg_q = math.gcd(x, M) > 1
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: m_1, ..., m_k are pairwise coprime positive integers",
    "H_2: x is an integer satisfying x ≡ a_i (mod m_i) for all 1 <= i <= k",
    "¬Q: x is not coprime to the product M = m_1 m_2 ... m_k"
]

N_HYP = 2
NEG_Q_INDEX = 2