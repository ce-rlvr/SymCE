import sympy
import math
import itertools
import functools

x, y, z, w = sympy.symbols('x y z w')

def conditions(witness) -> list[bool]:
    """
    witness: tuple (f_expr, q, p)
    where f_expr is a sympy expression in x representing the polynomial,
    q is the size of the field, and p is the characteristic.
    """
    try:
        f_expr, q, p = witness
    except Exception:
        return [False, False]

    def check_h1():
        try:
            if not isinstance(q, int) or not isinstance(p, int):
                return False
            if not sympy.isprime(p):
                return False
            if q < p:
                return False
            temp = q
            while temp % p == 0:
                temp //= p
            return temp == 1
        except Exception:
            return False

    h1_ok = check_h1()

    def check_neg_q():
        try:
            k = int(round(math.log(q, p)))
            y_sym = sympy.Symbol('y')

            # Find an irreducible polynomial of degree k over GF(p)
            irred_poly = None
            for coeffs in itertools.product(range(p), repeat=k+1):
                if coeffs[0] == 0:
                    continue
                P = sympy.Poly(coeffs, y_sym, domain=sympy.GF(p))
                if P.is_irreducible:
                    irred_poly = P.as_expr()
                    break

            if irred_poly is None:
                return False

            # Evaluate f(c) for all c in F_q
            values = []
            for coeffs in itertools.product(range(p), repeat=k):
                c = sympy.Poly(coeffs, y_sym, domain=sympy.GF(p)).as_expr()
                val_expr = f_expr.subs(x, c)
                val_expr = sympy.expand(val_expr)
                rem = sympy.rem(val_expr, irred_poly, y_sym, domain=sympy.GF(p))
                rem_poly = sympy.Poly(rem, y_sym, domain=sympy.GF(p))
                cfs = rem_poly.all_coeffs()
                # Pad with leading zeros to length k
                cfs = tuple([0]*(k - len(cfs)) + cfs)
                values.append(cfs)

            # Check if f is a permutation polynomial
            unique_values = set(values)
            is_pp = (len(unique_values) == q)

            # Check if f has exactly one root
            zero_tuple = tuple([0]*k)
            num_roots = values.count(zero_tuple)
            exactly_one_root = (num_roots == 1)

            # Helper functions for F_q arithmetic
            def mul_values(v1, v2):
                p1 = sympy.Poly(v1, y_sym, domain=sympy.GF(p))
                p2 = sympy.Poly(v2, y_sym, domain=sympy.GF(p))
                prod = p1 * p2
                rem = sympy.rem(prod.as_expr(), irred_poly, y_sym, domain=sympy.GF(p))
                rem_poly = sympy.Poly(rem, y_sym, domain=sympy.GF(p))
                cfs = rem_poly.all_coeffs()
                return tuple([0]*(k - len(cfs)) + cfs)

            def power_value(v, t):
                res = tuple([0]*(k-1) + [1])
                base = v
                while t > 0:
                    if t % 2 == 1:
                        res = mul_values(res, base)
                    base = mul_values(base, base)
                    t //= 2
                return res

            # Check the degree condition
            # The degree of f(x)^t mod (x^q - x) is strictly less than q-1
            # iff the coefficient of x^{q-1} is 0.
            # The coefficient of x^{q-1} is exactly -sum_{c in F_q} f(c)^t.
            degree_condition = True
            for t in range(1, q - 1):
                if t % p == 0:
                    continue

                sum_val = tuple([0]*k)
                for v in values:
                    vt = power_value(v, t)
                    sum_val = tuple((a + b) % p for a, b in zip(sum_val, vt))

                if sum_val != zero_tuple:
                    degree_condition = False
                    break

            # The conjecture states: f is PP iff (exactly one root AND degree condition)
            equivalence = (is_pp == (exactly_one_root and degree_condition))
            
            # neg_Q is True if the equivalence fails
            return not equivalence
        except Exception:
            return False

    neg_q_ok = check_neg_q()

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F_q is a finite field of characteristic p with q elements",
    "¬Q: The equivalence fails (f is PP iff exactly one root and degree condition)"
]

N_HYP = 1
NEG_Q_INDEX = 1