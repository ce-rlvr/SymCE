import sympy
import math

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the conjecture:
    "Cyclotomic Units of Prime Power Index"
    
    Witness is expected to be a tuple containing (p, k, a) or similar,
    where p is a prime, k >= 1, and a is an integer.
    """
    p, k, a = None, None, None
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            k = witness.get('k')
            a = witness.get('a')
        elif isinstance(witness, (tuple, list)):
            ints = []
            for x in witness:
                if isinstance(x, int):
                    ints.append(x)
                elif hasattr(x, 'is_integer') and x.is_integer:
                    ints.append(int(x))
            if len(ints) >= 3:
                p, k, a = ints[0], ints[1], ints[2]
            elif len(witness) >= 3:
                p, k, a = witness[0], witness[1], witness[2]
    except Exception:
        pass

    # Ensure types are standard Python ints if they are sympy Integers
    try:
        if hasattr(p, 'is_integer') and p.is_integer: p = int(p)
        if hasattr(k, 'is_integer') and k.is_integer: k = int(k)
        if hasattr(a, 'is_integer') and a.is_integer: a = int(a)
    except Exception:
        pass

    # H_1: p is a prime number
    try:
        h1_ok = bool(sympy.isprime(p))
    except Exception:
        h1_ok = False

    # H_2: k >= 1 is an integer
    try:
        h2_ok = bool(isinstance(k, int) and k >= 1)
    except Exception:
        h2_ok = False

    # H_3: \zeta_{p^k} is a primitive p^k-th root of unity
    # The existence of the primitive root is a mathematical fact for valid p and k.
    # We verify that 'a' is an integer, which is implicitly required for \zeta^a to be well-defined.
    try:
        h3_ok = bool(isinstance(a, int))
    except Exception:
        h3_ok = False

    # ¬Q: The element (\zeta^a - 1) / (\zeta - 1) is NOT a unit in Z[\zeta_{p^k}]
    # The element is a unit if and only if gcd(a, p) == 1.
    # Therefore, it is NOT a unit if and only if gcd(a, p) != 1.
    try:
        neg_q_ok = bool(math.gcd(int(a), int(p)) != 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: k >= 1 is an integer",
    "H_3: \\zeta_{p^k} is a primitive p^k-th root of unity",
    "¬Q: The element is not a unit in the ring of integers"
]

N_HYP = 3
NEG_Q_INDEX = 3