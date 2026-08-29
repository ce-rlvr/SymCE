import sympy

def conditions(witness):
    try:
        p, q, a = witness
    except Exception:
        return [False, False, False]

    # H_1: a \in \mathbb{F}_q
    try:
        q_int = int(q)
        a_int = int(a)
        h1 = bool(sympy.ntheory.is_prime_power(q_int))
    except Exception:
        h1 = False

    # H_2: f(x) = x^p - x - a \in \mathbb{F}_q[x]
    try:
        p_int = int(p)
        h2 = (p_int >= 1)
    except Exception:
        h2 = False

    # Conclusion: f(x) is irreducible over \mathbb{F}_q iff Tr_{\mathbb{F}_q/\mathbb{F}_p}(a) \neq 0
    try:
        p_int = int(p)
        q_int = int(q)
        
        if not sympy.isprime(p_int):
            q_holds = False
        else:
            factors = sympy.ntheory.factorint(q_int)
            if len(factors) != 1:
                q_holds = False
            else:
                char = list(factors.keys())[0]
                if char == p_int:
                    q_holds = True
                else:
                    q_holds = False
    except Exception:
        q_holds = False

    neg_q = not q_holds

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a in F_q",
    "H_2: f(x) = x^p - x - a is a polynomial",
    "not Q: f(x) is irreducible iff Tr(a) != 0 fails"
]

N_HYP = 2
NEG_Q_INDEX = 2