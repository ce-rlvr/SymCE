import sympy
from sympy import Poly, factor_list, GF, discriminant, lcm
from sympy.abc import x
from sympy.ntheory import primerange

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    Returns [H_1_ok, neg_Q_ok].
    """
    
    def check_h1(expr):
        """
        H_1: Let E be the splitting field of f(x) over Q.
        This requires the witness to be a valid polynomial over Q.
        """
        try:
            f = Poly(expr)
            if len(f.gens) != 1:
                return False
            return all(c.is_Rational for c in f.coeffs())
        except Exception:
            return False

    def check_neg_q(expr):
        """
        neg_Q: The Galois group of f(x) over Q is NOT S_5, OR the degree of the extension is NOT 120.
        Returns True if the conclusion FAILS (i.e., it is not S_5 or degree is not 120).
        """
        try:
            f = Poly(expr)
            if len(f.gens) != 1:
                return True
            gen = f.gens[0]
            
            if not all(c.is_Rational for c in f.coeffs()):
                return True
                
            if f.degree() < 5:
                return True
                
            # Factor the polynomial over Q
            facs = factor_list(expr)
            non_linear = [fac for fac, mult in facs[1] if Poly(fac, gen).degree() > 1]
            
            # If there are multiple non-linear factors, the splitting field is a compositum
            # which is extremely unlikely to have degree exactly 120 and group S_5.
            if len(non_linear) != 1:
                return True
                
            g_expr = non_linear[0]
            g = Poly(g_expr, gen)
            
            if g.degree() != 5:
                return True
                
            # Convert to an integer polynomial to compute the discriminant safely
            coeffs = g.coeffs()
            common_denom = 1
            for c in coeffs:
                common_denom = lcm(common_denom, c.as_numer_denom()[1])
            g_int_expr = g_expr * common_denom
            disc = discriminant(g_int_expr, gen)
            
            if disc == 0:
                return True
                
            # Check for S_5 Galois group using Chebotarev's density theorem.
            # A transitive subgroup of S_5 containing a 2-cycle and a 3-cycle (or a 6-cycle) is S_5.
            # We look for a prime p where the polynomial factors into degrees [2, 3] or [1, 1, 1, 2].
            has_S5_cert = False
            for p in primerange(2, 500):
                if disc % p == 0:
                    continue
                try:
                    fp = Poly(g_int_expr, gen, domain=GF(p))
                    mod_facs = fp.factor_list()
                    degrees = sorted([fac.degree() for fac, mult in mod_facs[1] for _ in range(mult)])
                    if degrees == [2, 3] or degrees == [1, 1, 1, 2]:
                        has_S5_cert = True
                        break
                except Exception:
                    continue
                    
            # If we found a certificate, it IS S_5 and degree IS 120, so the conclusion HOLDS (neg_Q is False).
            # Otherwise, we assume it is not S_5, so the conclusion FAILS (neg_Q is True).
            return not has_S5_cert
        except Exception:
            return True

    h1_ok = check_h1(witness)
    neg_q_ok = check_neg_q(witness)
    
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial over Q",
    "¬Q: The Galois group of f(x) over Q is not S_5 or the splitting field degree is not 120"
]

N_HYP = 1
NEG_Q_INDEX = 1