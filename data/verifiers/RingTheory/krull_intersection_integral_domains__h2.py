import sympy
from sympy import S

# Top-level setup: named object bindings that the witness expression may reference.
class ValuationRing:
    """
    Represents a valuation ring with a given value group.
    """
    def __init__(self, value_group):
        self.value_group = value_group
        
    def __repr__(self):
        return f"ValuationRing({self.value_group})"

class ValuationMaximalIdeal:
    """
    Represents the maximal ideal of a valuation ring.
    """
    def __init__(self, ring):
        self.ring = ring
        
    def __repr__(self):
        return f"ValuationMaximalIdeal({self.ring})"

class PuiseuxSeriesRing:
    """
    Represents the ring of Puiseux series over a field.
    """
    def __init__(self, field):
        self.field = field
        
    def __repr__(self):
        return f"PuiseuxSeriesRing({self.field})"

class PuiseuxSeriesMaximalIdeal:
    """
    Represents the maximal ideal of the Puiseux series ring (series with strictly positive valuation).
    """
    def __init__(self, ring):
        self.ring = ring
        
    def __repr__(self):
        return f"PuiseuxSeriesMaximalIdeal({self.ring})"

# Standard counterexamples for Krull's Intersection Theorem
# (Non-Noetherian integral domains where the intersection of I^n is not zero)
R_val_Q = ValuationRing(S.Rationals)
I_val_Q = ValuationMaximalIdeal(R_val_Q)

R_val_Z = ValuationRing(S.Integers)
I_val_Z = ValuationMaximalIdeal(R_val_Z)

R_puiseux = PuiseuxSeriesRing(S.Rationals)
I_puiseux = PuiseuxSeriesMaximalIdeal(R_puiseux)


def conditions(witness) -> list[bool]:
    try:
        R, I = witness
    except Exception:
        return [False, False, False, False]

    h1 = False
    try:
        r_name = R.__class__.__name__
        if r_name in ('ValuationRing', 'PuiseuxSeriesRing'):
            h1 = True
        elif hasattr(R, 'is_commutative'):
            h1 = bool(R.is_commutative)
        elif hasattr(R, 'is_CommutativeRing'):
            h1 = bool(R.is_CommutativeRing)
    except Exception:
        pass

    h2 = False
    try:
        r_name = R.__class__.__name__
        if r_name in ('ValuationRing', 'PuiseuxSeriesRing'):
            h2 = True
        elif hasattr(R, 'is_integral_domain'):
            h2 = bool(R.is_integral_domain)
        elif hasattr(R, 'is_IntegralDomain'):
            h2 = bool(R.is_IntegralDomain)
    except Exception:
        pass

    h3 = False
    try:
        r_name = R.__class__.__name__
        i_name = I.__class__.__name__
        if r_name == 'ValuationRing' and i_name == 'ValuationMaximalIdeal':
            h3 = (getattr(I, 'ring', None) == R)
        elif r_name == 'PuiseuxSeriesRing' and i_name == 'PuiseuxSeriesMaximalIdeal':
            h3 = (getattr(I, 'ring', None) == R)
        elif hasattr(I, 'is_proper'):
            h3 = bool(I.is_proper)
        else:
            try:
                h3 = not (1 in I)
            except Exception:
                pass
    except Exception:
        pass

    neg_q = False
    try:
        r_name = R.__class__.__name__
        i_name = I.__class__.__name__
        if r_name == 'ValuationRing' and i_name == 'ValuationMaximalIdeal' and getattr(I, 'ring', None) == R:
            vg = getattr(R, 'value_group', None)
            # If the value group is dense (like Rationals or Reals), the intersection of I^n is I != 0.
            if vg in (sympy.S.Rationals, sympy.S.Reals, getattr(sympy, 'QQ', None), getattr(sympy, 'RR', None)):
                neg_q = True
            else:
                neg_q = False
        elif r_name == 'PuiseuxSeriesRing' and i_name == 'PuiseuxSeriesMaximalIdeal' and getattr(I, 'ring', None) == R:
            # Puiseux series ring has value group Q, so intersection of I^n is I != 0.
            neg_q = True
        else:
            # For standard SymPy rings (which are Noetherian), the intersection is zero.
            neg_q = False
    except Exception:
        pass

    return [h1, h2, h3, neg_q]


CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is an integral domain",
    "H_3: I is a proper ideal of R",
    "¬Q: The intersection of I^n is not the zero ideal"
]

N_HYP = 3
NEG_Q_INDEX = 3