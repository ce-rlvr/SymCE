import math

# Top-level setup
# (No specific named objects required for this domain)

def conditions(witness) -> list[bool]:
    try:
        witness = list(witness)
    except Exception:
        return [False, False, False]

    try:
        h1 = True
        if not witness:
            h1 = False
        for item in witness:
            if len(item) != 3:
                h1 = False
                break
            c, a, m = item
            if not (isinstance(c, int) and isinstance(m, int)):
                h1 = False
                break
            if m == 0:
                h1 = False
                break
            if math.gcd(c, m) != 1:
                h1 = False
                break
    except Exception:
        h1 = False

    try:
        h2 = True
        if not witness:
            h2 = False
        for item in witness:
            if len(item) != 3:
                h2 = False
                break
            c, a, m = item
            if not isinstance(a, int):
                h2 = False
                break
    except Exception:
        h2 = False

    try:
        M = 1
        congruences = []
        for item in witness:
            c, a, m = item
            m_abs = abs(m)
            M *= m_abs
            if m_abs > 1:
                c_inv = pow(c % m_abs, -1, m_abs)
                b = (a * c_inv) % m_abs
                congruences.append((b, m_abs))
        
        if not congruences:
            # If all moduli are 1, the system trivially has a unique solution modulo 1
            neg_q = False
        else:
            curr_b, curr_m = congruences[0]
            possible = True
            for b, m in congruences[1:]:
                g = math.gcd(curr_m, m)
                if curr_b % g != b % g:
                    possible = False
                    break
                m1_g = curr_m // g
                m2_g = m // g
                if m2_g == 1:
                    u = 0
                else:
                    u = pow(m1_g % m2_g, -1, m2_g)
                lcm = curr_m * m2_g
                curr_b = (curr_b + curr_m * u * ((b - curr_b) // g)) % lcm
                curr_m = lcm
            
            if not possible:
                # No solution exists
                neg_q = True
            else:
                # Solution exists and is unique modulo curr_m (the LCM of all moduli).
                # It is unique modulo M (the product of all moduli) if and only if M == curr_m.
                neg_q = (M != curr_m)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: c_i and m_i are integers with gcd(c_i, m_i) = 1 for all i",
    "H_2: a_i are arbitrary integers",
    "¬Q: The system does not have a unique solution modulo m_1 * ... * m_k"
]

N_HYP = 2
NEG_Q_INDEX = 2