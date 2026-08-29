import sympy
from sympy.ntheory import factorint

# Top-level setup
# Witnesses are expected to be of the form (n, m, f)
# where R = Z/nZ, S = Z/mZ, and f is a mapping from R to S.
# n and m are integers >= 1.

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            n, m, f = witness
        elif isinstance(witness, dict):
            n = witness.get('n', witness.get('R'))
            m = witness.get('m', witness.get('S'))
            f = witness.get('f')
        else:
            n = getattr(witness, 'n', getattr(witness, 'R', None))
            m = getattr(witness, 'm', getattr(witness, 'S', None))
            f = getattr(witness, 'f', None)
            
        n = int(n)
        m = int(m)
    except Exception:
        return [False, False, False]

    # H_1: R and S are commutative rings
    # Z/nZ and Z/mZ are commutative rings for any integers n, m >= 1
    try:
        h1 = (n >= 1) and (m >= 1)
    except Exception:
        h1 = False

    # H_2: S is a reduced ring
    # Z/mZ is reduced iff m is square-free (or m=1, which is the zero ring)
    try:
        if m == 1:
            h2 = True
        else:
            factors = factorint(m)
            h2 = all(v == 1 for v in factors.values())
    except Exception:
        h2 = False

    # ¬Q: The nilradical of R is NOT contained in the kernel of f
    # We must find an element x in the nilradical of Z/nZ such that f(x) != 0 mod m.
    try:
        rad_n = 1
        if n > 1:
            for p in factorint(n).keys():
                rad_n *= p
        
        if isinstance(f, list) and len(f) > 0 and isinstance(f[0], (tuple, list)) and len(f[0]) == 2:
            try:
                f = dict(f)
            except Exception:
                pass

        neg_q = False
        # The nilradical of Z/nZ consists exactly of the multiples of rad_n
        for i, x in enumerate(range(0, n, rad_n)):
            if i > 1000:  # Safety limit to prevent TLE
                break
            
            val = None
            if callable(f):
                try:
                    val = f(x)
                except Exception:
                    pass
            elif hasattr(f, 'subs') and hasattr(f, 'free_symbols'):
                try:
                    syms = list(f.free_symbols)
                    if len(syms) == 1:
                        val = f.subs(syms[0], x)
                    elif len(syms) == 0:
                        val = f
                except Exception:
                    pass
            elif isinstance(f, dict):
                val = f.get(x, f.get(str(x)))
            else:
                try:
                    val = f[x]
                except Exception:
                    pass
            
            if val is not None:
                try:
                    val = int(val)
                    if (val % m) != 0:
                        neg_q = True
                        break
                except Exception:
                    pass
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings",
    "H_2: S is a reduced ring",
    "¬Q: The nilradical of R is not contained in the kernel of f"
]

N_HYP = 2
NEG_Q_INDEX = 2