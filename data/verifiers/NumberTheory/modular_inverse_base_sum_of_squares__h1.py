import sympy

# Top-level setup
# Domain is NumberTheory; no named bindings needed.

def conditions(witness):
    x = witness
    try:
        mod = x**2 + 1
        # In standard number theory, the modulus for a modular inverse must be >= 2.
        # For x = 0, mod = 1, and the modular inverse is undefined or degenerate.
        if mod < 2:
            q_ok = False
        else:
            inv = sympy.mod_inverse(x, mod)
            q_ok = (inv % mod) == ((-x) % mod)
    except Exception:
        q_ok = False

    return [not q_ok]

CONDITION_LABELS = [
    "¬Q: The modular inverse of x modulo x^2+1 is not congruent to -x \\pmod{x^2+1} (or is undefined)"
]

N_HYP = 0
NEG_Q_INDEX = 0