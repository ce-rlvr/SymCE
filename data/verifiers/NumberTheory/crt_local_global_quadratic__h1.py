import sympy
import math

# Top-level setup
# No named bindings needed for Number Theory; use integers directly.

def conditions(witness):
    """
    Given a witness (a, m, n), checks if it satisfies the remaining hypotheses
    and falsifies the conclusion of the conjecture.
    """
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            m = witness.get('m')
            n = witness.get('n')
        else:
            a, m, n = witness
    except Exception:
        return [False, False]

    # H_1: a is an integer
    try:
        h1 = isinstance(a, (int, sympy.Integer))
    except Exception:
        h1 = False

    # ¬Q: The conclusion fails
    try:
        a_int = int(a)
        m_int = int(m)
        n_int = int(n)
        
        def is_solvable(val, mod):
            if mod == 0:
                if val < 0: 
                    return False
                r = int(math.isqrt(val))
                return r * r == val
            
            mod = abs(mod)
            if mod > 1000000:
                raise ValueError("Modulus too large to check efficiently")
                
            for x in range(mod):
                if (x * x - val) % mod == 0:
                    return True
            return False

        sol_m = is_solvable(a_int, m_int)
        sol_n = is_solvable(a_int, n_int)
        sol_mn = is_solvable(a_int, m_int * n_int)

        # The conclusion states: sol_mn <==> (sol_m and sol_n)
        # The negation is that this equivalence does not hold.
        neg_q = sol_mn != (sol_m and sol_n)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a is an integer",
    "¬Q: Solvability modulo mn is not equivalent to solvability modulo m and modulo n"
]

N_HYP = 1
NEG_Q_INDEX = 1