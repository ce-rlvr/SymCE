import sympy
from sympy.ntheory import isprime, is_primitive_root, n_order, totient

# Top-level setup
# (No specific named objects required for this number theory problem)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            p = witness['p']
            g = witness['g']
            k = witness['k']
        else:
            p, g, k = witness
    except Exception:
        return [False, False, False, False, False]

    # H1: p is an odd prime number
    try:
        if not sympy.sympify(p).is_integer:
            h1 = False
        else:
            p_val = int(p)
            h1 = bool(isprime(p_val) and p_val % 2 != 0)
    except Exception:
        h1 = False

    # H2: g is an integer
    try:
        h2 = bool(sympy.sympify(g).is_integer)
    except Exception:
        h2 = False

    # H3: g is a primitive root modulo p
    try:
        h3 = bool(is_primitive_root(int(g), int(p)))
    except Exception:
        h3 = False

    # H4: g^{p-1} \not\equiv 1 \pmod{p^2}
    try:
        h4 = bool(pow(int(g), int(p) - 1, int(p)**2) != 1)
    except Exception:
        h4 = False

    # neg_Q: The multiplicative order of g modulo p^k is NOT \phi(p^k)
    try:
        modulus = sympy.sympify(p)**sympy.sympify(k)
        if not modulus.is_integer or modulus <= 0:
            neg_q = True
        elif modulus == 1:
            # For modulus 1, the order is 1 and phi(1) is 1.
            neg_q = False
        else:
            mod_int = int(modulus)
            expected = totient(mod_int)
            try:
                actual = n_order(int(g), mod_int)
                neg_q = bool(actual != expected)
            except Exception:
                # If n_order raises an exception (e.g., g and p^k not coprime), 
                # the order is undefined, so it is not equal to phi(p^k).
                neg_q = True
    except Exception:
        neg_q = True

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: p is an odd prime number",
    "H_2: g is an integer",
    "H_3: g is a primitive root modulo p",
    "H_4: g^{p-1} \\not\\equiv 1 \\pmod{p^2}",
    "¬Q: The multiplicative order of g modulo p^k is not \\phi(p^k)"
]

N_HYP = 4
NEG_Q_INDEX = 4