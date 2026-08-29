import sympy
from sympy.ntheory import totient, divisors, divisor_sigma
from sympy import Function

N_HYP = 0
NEG_Q_INDEX = 0
CONDITION_LABELS = ["¬Q: phi * tau != sigma"]

def conditions(witness):
    try:
        # If witness is a tuple (n, tau) or (tau, n)
        if isinstance(witness, tuple) and len(witness) == 2:
            a, b = witness
            if callable(a) and isinstance(b, int):
                tau_func, n = a, b
                conv = sum(totient(d) * tau_func(n // d) for d in divisors(n))
                neg_q = bool(conv != divisor_sigma(n))
                return [neg_q]
            elif callable(b) and isinstance(a, int):
                n, tau_func = a, b
                conv = sum(totient(d) * tau_func(n // d) for d in divisors(n))
                neg_q = bool(conv != divisor_sigma(n))
                return [neg_q]

        # If witness is a callable (like a function or sympy.Function)
        if callable(witness):
            tau_func = witness
            neg_q = False
            for n in range(1, 50):
                conv = sum(totient(d) * tau_func(n // d) for d in divisors(n))
                if conv != divisor_sigma(n):
                    neg_q = True
                    break
            return [neg_q]

        # If witness is a dict mapping n -> tau(n)
        if isinstance(witness, dict):
            neg_q = False
            for n in witness:
                if n < 1: 
                    continue
                conv = sum(totient(d) * witness[n // d] for d in divisors(n))
                if conv != divisor_sigma(n):
                    neg_q = True
                    break
            return [neg_q]

        # If witness is a list/tuple of values, assuming 0-indexed (tau(k) = witness[k])
        if isinstance(witness, (list, tuple)):
            neg_q = False
            for n in range(1, len(witness)):
                conv = sum(totient(d) * witness[n // d] for d in divisors(n))
                if conv != divisor_sigma(n):
                    neg_q = True
                    break
            return [neg_q]

        # Otherwise, assume witness is n, and tau is an uninterpreted function
        n = int(witness)
        tau_sym = Function('tau')
        conv = sum(totient(d) * tau_sym(n // d) for d in divisors(n))
        neg_q = bool(conv != divisor_sigma(n))
        return [neg_q]

    except Exception:
        return [False]