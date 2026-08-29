import sympy
from sympy import symbols, Rational
from sympy.polys.domains import ZZ, QQ
import math

# Top-level setup
t = symbols('t')

def compute_ideal_quotient(R, I, x, n):
    if hasattr(I, 'gens'):
        gens = I.gens
    elif isinstance(I, list) or isinstance(I, tuple):
        gens = list(I)
    else:
        gens = [I]

    if isinstance(x, float):
        p, q = x.as_integer_ratio()
    elif isinstance(x, sympy.Rational):
        p, q = x.p, x.q
    elif hasattr(x, 'as_numer_denom'):
        p, q = x.as_numer_denom()
    elif isinstance(x, (int, sympy.Integer)):
        p, q = x, 1
    else:
        try:
            from sympy import fraction
            p, q = fraction(x)
        except Exception:
            p, q = x, 1

    pn = p**n
    qn = q**n

    if R == ZZ:
        m = 0
        if gens:
            m = int(gens[0])
            for g in gens[1:]:
                m = math.gcd(m, int(g))
        target = m * int(qn)
        g = math.gcd(target, int(pn))
        if g == 0:
            return 0
        return abs(target // g)

    if hasattr(R, 'ideal'):
        try:
            qn_I_gens = [qn * gen for gen in gens]
            ideal_qn_I = R.ideal(*qn_I_gens)
            ideal_pn = R.ideal(pn)
            quot = ideal_qn_I.quotient(ideal_pn)
            return quot
        except Exception:
            pass

    return None

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            R, I, x = witness
        else:
            R = witness.R
            I = witness.I
            x = witness.x
    except Exception:
        return [False, False, False]

    # H1: R is a commutative Noetherian ring
    h1 = False
    try:
        if hasattr(witness, 'is_commutative_noetherian'):
            try:
                h1 = witness.is_commutative_noetherian()
            except TypeError:
                h1 = witness.is_commutative_noetherian(R)
        else:
            if R == ZZ or R == QQ:
                h1 = True
            elif hasattr(R, 'domain') and hasattr(R, 'symbols'):
                if R.domain in (ZZ, QQ):
                    h1 = True
            elif getattr(R, 'is_commutative', False) and getattr(R, 'is_noetherian', False):
                h1 = True
    except Exception:
        h1 = False

    # H2: I is an ideal of R
    h2 = False
    try:
        if hasattr(witness, 'is_ideal'):
            try:
                h2 = witness.is_ideal()
            except TypeError:
                h2 = witness.is_ideal(I, R)
        else:
            if hasattr(I, 'gens'):
                gens = I.gens
            elif isinstance(I, list) or isinstance(I, tuple):
                gens = list(I)
            else:
                gens = [I]
                
            if R == ZZ:
                h2 = all(isinstance(g, (int, sympy.Integer)) for g in gens)
            else:
                all_in_R = True
                for g in gens:
                    try:
                        if hasattr(R, 'from_expr'):
                            R.from_expr(g)
                        else:
                            R(g)
                    except Exception:
                        all_in_R = False
                        break
                h2 = all_in_R
    except Exception:
        h2 = False

    # neg_Q: The chain does not stabilize
    neg_q = False
    try:
        if hasattr(witness, 'chain_stabilizes'):
            try:
                neg_q = not witness.chain_stabilizes()
            except TypeError:
                neg_q = not witness.chain_stabilizes(I, x)
        else:
            stabilized = False
            prev_val = None
            
            for n in range(1, 20):
                val = compute_ideal_quotient(R, I, x, n)
                if val is None:
                    break
                if prev_val is not None and val == prev_val:
                    stabilized = True
                    break
                prev_val = val
            else:
                if prev_val is not None:
                    neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: I is an ideal of R",
    "¬Q: The ascending chain of ideal quotients (I : x^n) does not stabilize"
]

N_HYP = 2
NEG_Q_INDEX = 2