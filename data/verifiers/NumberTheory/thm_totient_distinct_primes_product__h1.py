import sympy
from sympy.ntheory import isprime, totient, factorint

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the conjecture:
    Hypotheses:
      - p_1, p_2, ..., p_k are distinct prime numbers
      - n = p_1 p_2 ... p_k
    Conclusion:
      - phi(n) = (p_1 - 1)(p_2 - 1) ... (p_k - 1)
    """
    try:
        if isinstance(witness, dict):
            if 'n' in witness and ('p_list' in witness or 'p' in witness or 'primes' in witness):
                n = witness['n']
                p_list = witness.get('p_list', witness.get('p', witness.get('primes')))
            else:
                if 'n' in witness:
                    n = witness['n']
                    p_list = list(factorint(n).keys())
                else:
                    p_list = witness.get('p_list', witness.get('p', witness.get('primes')))
                    n = 1
                    for p in p_list:
                        n *= p
        elif isinstance(witness, (int, sympy.Integer)):
            n = witness
            p_list = list(factorint(n).keys())
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 2 and isinstance(witness[1], (list, tuple, set, frozenset)):
                n, p_list = witness
            else:
                p_list = list(witness)
                n = 1
                for p in p_list:
                    n *= p
        else:
            return [False, False, False]
            
        p_list = list(p_list)
    except Exception:
        return [False, False, False]

    # H_1: p_1, p_2, ..., p_k are distinct prime numbers
    try:
        h1 = all(isprime(p) for p in p_list) and len(set(p_list)) == len(p_list)
    except Exception:
        h1 = False

    # H_2: n = p_1 p_2 ... p_k
    try:
        prod = 1
        for p in p_list:
            prod *= p
        h2 = (n == prod)
    except Exception:
        h2 = False

    # ¬Q: phi(n) != (p_1 - 1)(p_2 - 1) ... (p_k - 1)
    try:
        prod_phi = 1
        for p in p_list:
            prod_phi *= (p - 1)
        neg_q = (totient(n) != prod_phi)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p_1, p_2, ..., p_k are distinct prime numbers",
    "H_2: n = p_1 p_2 ... p_k",
    "¬Q: phi(n) != (p_1 - 1)(p_2 - 1) ... (p_k - 1)"
]

N_HYP = 2
NEG_Q_INDEX = 2