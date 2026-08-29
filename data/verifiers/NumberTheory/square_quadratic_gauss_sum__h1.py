import sympy as sp
from sympy import I, pi, exp
from sympy.ntheory import jacobi_symbol

try:
    from sympy.ntheory import kronecker_symbol
except ImportError:
    kronecker_symbol = None

# Top-level setup for Number Theory (no named bindings needed)

CONDITION_LABELS = [
    "H_1: g = sum_{t=1}^{p-1} (t/p) e^{2 pi i t / p}",
    "¬Q: g^2 != (-1)^{(p-1)/2} p"
]

N_HYP = 1
NEG_Q_INDEX = 1

def get_symbol(t, p):
    try:
        return jacobi_symbol(t, p)
    except ValueError:
        if kronecker_symbol is not None:
            return kronecker_symbol(t, p)
        if p == 2:
            return 1 if t % 2 != 0 else 0
        raise

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            p, g = witness
            p = int(p)
        else:
            p = int(witness)
            g = sum(get_symbol(t, p) * exp(2 * pi * I * t / p) for t in range(1, p))
    except Exception:
        return [False, False]
        
    try:
        expected_g = sum(get_symbol(t, p) * exp(2 * pi * I * t / p) for t in range(1, p))
        diff = sp.simplify(sp.expand(g - expected_g))
        if diff == 0:
            h1 = True
        else:
            try:
                h1 = abs(complex(diff.evalf(chop=True))) < 1e-9
            except Exception:
                h1 = False
    except Exception:
        h1 = False
        
    try:
        expected_g2 = ((-1)**sp.Rational(p-1, 2)) * p
        diff2 = sp.simplify(sp.expand(g**2 - expected_g2))
        if diff2 == 0:
            neg_q = False
        else:
            try:
                neg_q = abs(complex(diff2.evalf(chop=True))) > 1e-9
            except Exception:
                neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, neg_q]