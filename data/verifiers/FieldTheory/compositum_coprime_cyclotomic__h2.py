import math
import sympy

# Top-level setup
# (No specific named objects required for this number theory/field theory conjecture)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness['n']
            m = witness['m']
        else:
            n = witness[0]
            m = witness[1]
        
        n_int = int(n)
        m_int = int(m)
        # H_1: n and m are positive integers
        h1 = (n_int == n) and (m_int == m) and (n_int > 0) and (m_int > 0)
        n = n_int
        m = m_int
    except Exception:
        h1 = False

    # H_2 and H_3: The existence of primitive roots of unity is guaranteed for any positive integers n, m.
    # The fields ℚ(ζ_n) and ℚ(ζ_m) are well-defined.
    h2 = h1
    h3 = h1

    try:
        if not h1:
            neg_q = False
        else:
            lcm_nm = (n * m) // math.gcd(n, m)
            
            # The cyclotomic field ℚ(ζ_k) contains exactly the rad(k)-th roots of unity,
            # where rad(k) = 2k if k is odd, and k if k is even.
            # Two cyclotomic fields ℚ(ζ_a) and ℚ(ζ_b) are equal iff rad(a) == rad(b).
            def rad(k):
                return 2 * k if k % 2 == 1 else k
                
            # The compositum ℚ(ζ_n)ℚ(ζ_m) is ℚ(ζ_{lcm(n, m)}).
            # The conclusion is ℚ(ζ_{lcm(n, m)}) == ℚ(ζ_{nm}).
            # So the negated conclusion is that they are not equal.
            neg_q = rad(lcm_nm) != rad(n * m)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n and m are positive integers",
    "H_2: ζ_n is a primitive n-th root of unity",
    "H_3: ζ_m is a primitive m-th root of unity",
    "¬Q: ℚ(ζ_n)ℚ(ζ_m) != ℚ(ζ_{nm})"
]

N_HYP = 3
NEG_Q_INDEX = 3