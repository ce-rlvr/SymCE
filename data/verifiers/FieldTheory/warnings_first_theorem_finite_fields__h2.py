import sympy
import itertools
from sympy.abc import x, y, z, t, u, v, w

CONDITION_LABELS = [
    "H_1: F_q is a finite field of characteristic p",
    "H_2: The sum of the total degrees is strictly less than n",
    "H_3: N is the number of common zeros of f_1, ..., f_k in F_q^n",
    "¬Q: N is not divisible by p"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, dict):
            p = witness['p']
            q = witness['q']
            n = witness['n']
            polys = witness['polys']
            vars = witness.get('vars', [])
        elif isinstance(witness, (tuple, list)):
            p = witness[0]
            q = witness[1]
            n = witness[2]
            polys = witness[3]
            vars = witness[4] if len(witness) > 4 else []
        else:
            p = witness.p
            q = witness.q
            n = witness.n
            polys = witness.polys
            vars = getattr(witness, 'vars', [])
    except Exception:
        return [False, False, False, False]

    # H1: F_q is a finite field of characteristic p
    try:
        h1 = False
        if sympy.isprime(p) and q >= p:
            temp = q
            while temp % p == 0:
                temp //= p
            if temp == 1:
                h1 = True
    except Exception:
        h1 = False

    # H2: The sum of the total degrees is strictly less than n
    try:
        h2 = False
        sum_deg = 0.0
        for f in polys:
            f_expr = sympy.S(f)
            if f_expr == 0:
                sum_deg += float('-inf')
            elif not vars:
                if f_expr.free_symbols:
                    raise ValueError("Not a constant")
                sum_deg += 0.0
            else:
                poly_obj = sympy.Poly(f_expr, *vars)
                deg = poly_obj.total_degree()
                if deg == sympy.S('-oo') or deg == float('-inf'):
                    sum_deg += float('-inf')
                else:
                    sum_deg += float(deg)
        if sum_deg < n:
            h2 = True
    except Exception:
        h2 = False

    # H3: N is the number of common zeros of f_1, ..., f_k in F_q^n
    # This is a definitional hypothesis satisfied by how we compute N below.
    h3 = True

    # ¬Q: N is not divisible by p
    try:
        neg_q = False
        if n == 0:
            all_zero = True
            for f in polys:
                val = sympy.S(f)
                if val.is_Rational:
                    if val.q % p == 0 or val.p % p != 0:
                        all_zero = False
                        break
                else:
                    all_zero = False
                    break
            N = 1 if all_zero else 0
            if N % p != 0:
                neg_q = True
        elif q == p:
            N = 0
            for pt in itertools.product(range(p), repeat=n):
                subs_dict = dict(zip(vars, pt))
                all_zero = True
                for f in polys:
                    val = sympy.S(f).subs(subs_dict)
                    if val.is_Rational:
                        if val.q % p == 0 or val.p % p != 0:
                            all_zero = False
                            break
                    else:
                        all_zero = False
                        break
                if all_zero:
                    N += 1
            if N % p != 0:
                neg_q = True
        else:
            # For q > p and n > 0, full finite field arithmetic is required.
            # A valid counterexample can be provided with n=0 or q=p.
            pass
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]