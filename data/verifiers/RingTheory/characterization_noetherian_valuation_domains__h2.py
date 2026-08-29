import sympy

class AbstractRing:
    """
    A mock class to represent abstract rings and their properties,
    since SymPy does not natively model arbitrary valuation domains.
    """
    def __init__(self, name, is_valuation_domain, is_field, is_dvr):
        self.name = name
        self.is_valuation_domain = is_valuation_domain
        self.is_field = is_field
        self.is_dvr = is_dvr
        
    def __str__(self):
        return self.name
        
    def __repr__(self):
        return self.name

# Top-level setup: named object bindings that the witness expression may reference.
# We provide several standard examples of rings with their properties.
Z = AbstractRing("Z", is_valuation_domain=False, is_field=False, is_dvr=False)
Q = AbstractRing("Q", is_valuation_domain=True, is_field=True, is_dvr=False)
Z_p = AbstractRing("Z_p", is_valuation_domain=True, is_field=False, is_dvr=True)
k_x_y = AbstractRing("k[[x,y]]", is_valuation_domain=False, is_field=False, is_dvr=False)

# Counterexamples: Valuation domains that are neither fields nor DVRs.
# Examples include valuation rings of rank > 1, or non-discrete rank 1 valuation rings.
ValuationRing_Rank2 = AbstractRing("ValuationRing_Rank2", is_valuation_domain=True, is_field=False, is_dvr=False)
PuiseuxSeriesRing = AbstractRing("PuiseuxSeriesRing", is_valuation_domain=True, is_field=False, is_dvr=False)
NonDiscreteValuationDomain = AbstractRing("NonDiscreteValuationDomain", is_valuation_domain=True, is_field=False, is_dvr=False)

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    Returns [H_1_ok, H_2_ok, neg_Q_ok].
    """
    # H_1: R is a valuation domain
    try:
        if hasattr(witness, 'is_valuation_domain'):
            h1 = bool(witness.is_valuation_domain)
        elif isinstance(witness, dict) and 'is_valuation_domain' in witness:
            h1 = bool(witness['is_valuation_domain'])
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: R is not a field
    try:
        if hasattr(witness, 'is_field'):
            h2 = not bool(witness.is_field)
        elif isinstance(witness, dict) and 'is_field' in witness:
            h2 = not bool(witness['is_field'])
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: R is not a discrete valuation ring (DVR)
    try:
        if hasattr(witness, 'is_dvr'):
            neg_q = not bool(witness.is_dvr)
        elif isinstance(witness, dict) and 'is_dvr' in witness:
            neg_q = not bool(witness['is_dvr'])
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a valuation domain",
    "H_2: R is not a field",
    "¬Q: R is not a discrete valuation ring (DVR)"
]

N_HYP = 2
NEG_Q_INDEX = 2