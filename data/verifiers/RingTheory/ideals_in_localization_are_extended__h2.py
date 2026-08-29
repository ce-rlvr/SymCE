import sympy
from sympy import Rational, cancel, factor_list, div, simplify, sympify
from sympy.ntheory import primefactors
from sympy.abc import x

# Top-level setup for witness expressions
ZZ = sympy.S.Integers
QQ = sympy.S.Rationals

def conditions(witness):
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture:
    Hypotheses:
      - R is a commutative ring with identity
      - J is an ideal of the localization S^{-1}R
    Conclusion:
      - There exists an ideal I of R such that J = S^{-1}I
    (The missing hypothesis is that S must be a multiplicatively closed subset of R).
    """
    try:
        # Unpack witness. Expected format: tuple (R, S, J_gens) or dict/object with these attributes.
        if hasattr(witness, 'R'):
            R = witness.R
            S = witness.S
            J_gens = witness.J_gens
        elif isinstance(witness, dict):
            R = witness.get('R')
            S = witness.get('S')
            J_gens = witness.get('J_gens')
        else:
            R, S, J_gens = witness
    except Exception:
        return [False, False, False]

    # H_1: R is a commutative ring with identity
    try:
        h1 = False
        if R in ('Z', ZZ, 'Q', QQ):
            h1 = True
        elif hasattr(R, 'is_commutative') and R.is_commutative:
            h1 = True
        elif hasattr(R, 'domain') and hasattr(R, 'gens'):
            h1 = True
        elif isinstance(R, str) and ('[' in R or R.isalpha()):
            h1 = True
    except Exception:
        h1 = False

    # H_2: J is an ideal of the localization S^{-1}R
    # We verify that S is a valid subset and that the generators of J belong to S^{-1}R.
    try:
        h2 = False
        if isinstance(S, (list, tuple, set)) and len(S) > 0:
            # If R is Z, ensure S only contains integers
            if R in ('Z', ZZ) and not all(isinstance(s, (int, sympy.Integer)) for s in S):
                h2 = False
            else:
                h2 = True
                for g in J_gens:
                    in_loc = False
                    # Try evaluating as a rational number (for R = Z)
                    try:
                        if isinstance(g, (int, sympy.Integer)):
                            in_loc = True
                        else:
                            q = Rational(g)
                            den = q.q
                            if den == 1:
                                in_loc = True
                            else:
                                in_loc = True
                                for p in primefactors(den):
                                    if not any(isinstance(s, (int, sympy.Integer)) and s % p == 0 for s in S):
                                        in_loc = False
                                        break
                    except Exception:
                        pass
                    
                    # Try evaluating as a symbolic expression (for polynomial rings)
                    if not in_loc:
                        try:
                            num, den = cancel(g).as_numer_denom()
                            if den == 1:
                                in_loc = True
                            else:
                                coeff, factors = factor_list(den)
                                in_loc = True
                                # Check constant coefficient of the denominator
                                if abs(coeff) > 1:
                                    for p in primefactors(abs(int(coeff))):
                                        if not any(isinstance(s, (int, sympy.Integer)) and s % p == 0 for s in S):
                                            in_loc = False
                                            break
                                # Check polynomial factors of the denominator
                                if in_loc:
                                    for factor, power in factors:
                                        divides = False
                                        for s in S:
                                            try:
                                                q_div, r_div = div(s, factor)
                                                if r_div == 0:
                                                    divides = True
                                                    break
                                            except Exception:
                                                pass
                                        if not divides:
                                            in_loc = False
                                            break
                        except Exception:
                            pass
                    
                    if not in_loc:
                        h2 = False
                        break
    except Exception:
        h2 = False

    # ¬Q: There does NOT exist an ideal I of R such that J = S^{-1}I
    # If S is finite and not multiplicatively closed (contains a non-unit), 
    # S^{-1}I will have bounded denominators for any ideal I.
    # However, any non-zero ideal J of S^{-1}R will have unbounded denominators.
    # Thus, J != S^{-1}I for all I.
    try:
        neg_q = False
        if h1 and h2:
            has_nonzero_J = False
            for g in J_gens:
                try:
                    if simplify(g) != 0:
                        has_nonzero_J = True
                        break
                except Exception:
                    pass
            
            has_nonunit_S = False
            has_zero_in_S = False
            for s in S:
                try:
                    if simplify(s) == 0:
                        has_zero_in_S = True
                        break
                    if isinstance(s, (int, sympy.Integer)):
                        if abs(s) > 1:
                            has_nonunit_S = True
                    else:
                        if not sympify(s).is_constant():
                            has_nonunit_S = True
                except Exception:
                    pass
            
            # If 0 is in S, S^{-1}R is the zero ring, and J = S^{-1}I = {0} holds trivially.
            if has_zero_in_S:
                neg_q = False
            elif has_nonzero_J and has_nonunit_S:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: J is an ideal of the localization S^{-1}R",
    "¬Q: There does not exist an ideal I of R such that J = S^{-1}I"
]

N_HYP = 2
NEG_Q_INDEX = 2