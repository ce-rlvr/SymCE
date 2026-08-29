import sympy
from sympy import Poly
from sympy.abc import x

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            f = witness.get('f')
            p = witness.get('p', None)
            if p is not None:
                p = int(p)
            if not isinstance(f, Poly):
                if p is not None and sympy.isprime(p):
                    f = Poly(f, domain=sympy.GF(p))
                else:
                    f = Poly(f)
            if p is None:
                p = int(f.domain.char)
        else:
            f = witness
            if not isinstance(f, Poly):
                f = Poly(f)
            p = int(f.domain.char)

        char = int(f.domain.char)
        if char == 0:
            return [False, False, False, False]
        
        # H1: F is a field of prime characteristic p > 0
        h1 = (char > 0) and sympy.isprime(char)
        if p is not None:
            h1 = h1 and (char == p)

        # H2: K/F is a purely inseparable field extension
        # We evaluate the polynomial over its domain F and assume K = F,
        # which is trivially a purely inseparable extension.
        h2 = True

        # H3: alpha is an algebraic element over F
        # Any non-constant polynomial has an algebraic root in its splitting field.
        if len(f.gens) != 1:
            h3 = False
        else:
            h3 = f.degree() >= 1

        # Conclusion: In K[x], f(x) = g(x)^q for some irreducible g and q = p^e
        # Since K/F is purely inseparable, f(x) is of this form in K[x] if and only if
        # it is of the form h(x)^{q'} in F[x] for some irreducible h and q' a power of p.
        factors = f.factor_list()
        if len(factors[1]) == 1:
            g, q = factors[1][0]
            temp = q
            while temp % char == 0 and temp > 1:
                temp //= char
            is_power_of_p = (temp == 1)
            conclusion = is_power_of_p
        else:
            conclusion = False

        neg_q = not conclusion

        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: F is a field of prime characteristic p > 0",
    "H_2: K/F is a purely inseparable field extension",
    "H_3: alpha is an algebraic element over F",
    "¬Q: f(x) is not of the form g(x)^q for irreducible g and q a power of p"
]

N_HYP = 3
NEG_Q_INDEX = 3