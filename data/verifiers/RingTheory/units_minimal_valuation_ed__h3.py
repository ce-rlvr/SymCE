import sympy
from sympy import ZZ, QQ
from sympy.abc import x

# Top-level setup for Ring Theory
# We define standard rings and symbols that a witness might use.
# (Group theory and linear algebra bindings are omitted as they are not relevant to this domain)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    Hypotheses:
      H_1: R is a Euclidean domain
      H_2: v is a Euclidean valuation on R such that v(a) <= v(ab) for all non-zero a, b in R
    Conclusion:
      Q: u is a unit in R if and only if v(u) = v(1)
    """
    try:
        R = witness.R
        v = witness.v
        u = witness.u
    except Exception:
        return [False, False, False]

    # H_1: R is a Euclidean domain
    try:
        h1 = False
        # We accept ZZ, any Field (since fields are Euclidean domains), or Polynomial Rings over Fields
        if hasattr(R, 'is_Field') and R.is_Field:
            h1 = True
        elif R == ZZ:
            h1 = True
        elif hasattr(R, 'is_PolynomialRing') and R.is_PolynomialRing and R.domain.is_Field:
            h1 = True
    except Exception:
        h1 = False

    # H_2: v is a Euclidean valuation on R such that v(a) <= v(ab) for all non-zero a, b
    try:
        h2 = True
        if R == ZZ:
            sample = [ZZ(i) for i in range(-10, 11)]
            def get_div(a, b):
                q_approx = int(a) // int(b)
                divs = []
                # Check a small neighborhood around the standard quotient to allow flexible remainders
                for dq in [-2, -1, 0, 1, 2]:
                    q = ZZ(q_approx + dq)
                    r = a - q * b
                    divs.append((q, r))
                return divs
            def is_unit(val):
                return abs(val) == 1
            zero = ZZ(0)
            one = ZZ(1)
        elif hasattr(R, 'is_Field') and R.is_Field:
            sample = [R(i) for i in range(-5, 6)]
            def get_div(a, b):
                return [(a / b, R(0))]
            def is_unit(val):
                return val != R(0)
            zero = R(0)
            one = R(1)
        elif hasattr(R, 'is_PolynomialRing') and R.is_PolynomialRing and R.domain.is_Field:
            gen = R.gens[0]
            sample = [R(0), R(1), R(-1), gen, gen + 1, gen - 1, gen**2, gen**2 + 1]
            def get_div(a, b):
                return [divmod(a, b)]
            def is_unit(val):
                return val != R(0) and val.degree() == 0
            zero = R(0)
            one = R(1)
        else:
            h2 = False
            sample = []

        if h2:
            for a in sample:
                for b in sample:
                    if b != zero:
                        # Check Euclidean division condition: a = qb + r with r = 0 or v(r) < v(b)
                        divs = get_div(a, b)
                        valid_div = False
                        for q, r in divs:
                            if r == zero:
                                valid_div = True
                                break
                            else:
                                try:
                                    if v(r) < v(b):
                                        valid_div = True
                                        break
                                except Exception:
                                    pass
                        if not valid_div:
                            h2 = False
                            break
                        
                        # Check monotonicity condition: v(a) <= v(ab) for non-zero a, b
                        if a != zero:
                            try:
                                if not (v(a) <= v(a * b)):
                                    h2 = False
                                    break
                            except Exception:
                                h2 = False
                                break
                if not h2:
                    break
    except Exception:
        h2 = False

    # ¬Q: The conclusion "u is a unit iff v(u) = v(1)" must FAIL at the witness
    try:
        is_u_unit = is_unit(u)
        v_u = v(u)
        v_1 = v(one)
        q_holds = (is_u_unit == (v_u == v_1))
        neg_q = not q_holds
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "H_2: v is a Euclidean valuation on R such that v(a) <= v(ab) for all non-zero a, b in R",
    "¬Q: The equivalence (u is a unit iff v(u) = v(1)) fails at the witness"
]

N_HYP = 2
NEG_Q_INDEX = 2