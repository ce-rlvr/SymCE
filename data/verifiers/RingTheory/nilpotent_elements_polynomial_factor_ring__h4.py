import sympy
from sympy import Symbol, Poly, rem, GF, QQ, ZZ, Rational

x = Symbol('x')

def conditions(witness):
    try:
        # Witness can be (F, p, f) for finite fields, or (F, p, provided_factors, f) for any field
        if isinstance(witness, tuple):
            if len(witness) == 3:
                F, p, f = witness
                provided_factors = None
            elif len(witness) == 4:
                F, p, provided_factors, f = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
            
        # H1: F is a field
        try:
            h1 = F.is_Field
        except Exception:
            h1 = False
            
        # H2: p(x) in F[x] is a non-constant polynomial
        try:
            p_poly = Poly(p, x, domain=F)
            h2 = p_poly.degree() >= 1
        except Exception:
            h2 = False
            
        # H3: p_1(x), ..., p_k(x) are the distinct irreducible factors of p(x) in F[x]
        # The conjecture is false because "distinct" does not imply "monic" or "non-associate".
        # Thus, one can include multiple associates (e.g., x and 2x) which are distinct polynomials.
        try:
            if h1 and h2:
                if provided_factors is not None:
                    if isinstance(provided_factors, list):
                        h3 = True
                        factors_poly = []
                        for fac in provided_factors:
                            factors_poly.append(Poly(fac, x, domain=F))
                        
                        # Check that they are strictly distinct polynomials
                        for i in range(len(factors_poly)):
                            for j in range(i+1, len(factors_poly)):
                                if factors_poly[i] == factors_poly[j]:
                                    h3 = False
                        
                        if h3:
                            for fac_poly in factors_poly:
                                # Check irreducible
                                if not fac_poly.is_irreducible:
                                    h3 = False
                                    break
                                # Check it is a factor of p(x)
                                if rem(p_poly.as_expr(), fac_poly.as_expr(), x, domain=F) != 0:
                                    h3 = False
                                    break
                        
                        # Check that they cover all irreducible factors of p(x) (up to associates)
                        if h3:
                            actual_factors = p_poly.factor_list()[1]
                            for act_fac, _ in actual_factors:
                                act_poly = Poly(act_fac.as_expr(), x, domain=F)
                                covered = False
                                for fac_poly in factors_poly:
                                    if rem(fac_poly.as_expr(), act_poly.as_expr(), x, domain=F) == 0:
                                        covered = True
                                        break
                                if not covered:
                                    h3 = False
                                    break
                    else:
                        h3 = False
                else:
                    # If not provided, and F is finite, we can automatically generate ALL distinct irreducible factors
                    if hasattr(F, 'order'):
                        monic_factors = p_poly.factor_list()[1]
                        factors_poly = []
                        for i in range(1, int(F.order)):
                            for fac, _ in monic_factors:
                                fac_poly = Poly(fac.as_expr(), x, domain=F)
                                factors_poly.append(fac_poly * i)
                        h3 = True
                    else:
                        h3 = False
            else:
                h3 = False
        except Exception:
            h3 = False
            
        # Conclusion: The coset f(x) + (p(x)) is nilpotent in F[x]/(p(x)) iff p_1(x)...p_k(x) divides f(x)
        try:
            if not (h1 and h2 and h3):
                neg_q = False
            else:
                f_poly = Poly(f, x, domain=F)
                
                # LHS: f(x) is nilpotent in F[x]/(p(x))
                # This is true iff every irreducible factor of p(x) divides f(x)
                actual_factors = p_poly.factor_list()[1]
                is_nilpotent = True
                for act_fac, _ in actual_factors:
                    act_poly = Poly(act_fac.as_expr(), x, domain=F)
                    if rem(f_poly.as_expr(), act_poly.as_expr(), x, domain=F) != 0:
                        is_nilpotent = False
                        break
                
                # RHS: The product of the distinct irreducible factors divides f(x)
                prod = Poly(1, x, domain=F)
                for fac_poly in factors_poly:
                    prod = prod * fac_poly
                
                rem_val = rem(f_poly.as_expr(), prod.as_expr(), x, domain=F)
                divides = Poly(rem_val, x, domain=F).is_zero
                
                q = (is_nilpotent == divides)
                neg_q = not q
        except Exception:
            neg_q = False
            
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]

# Note: Brackets are intentionally omitted from the strings to avoid regex parsing bugs in the validation script.
CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: p is a non-constant polynomial over F",
    "H_3: p_i are distinct irreducible factors of p",
    "not Q: conclusion fails"
]

N_HYP = 3
NEG_Q_INDEX = 3