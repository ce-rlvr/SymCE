import sympy
from sympy import S, ProductSet, FiniteSet

# Top-level setup: named object bindings that the witness expression may reference.
Q = S.Rationals
R = S.Reals
C = S.Complexes
Z = S.Integers

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Let V be equipped with a topology such that vector addition and scalar multiplication are continuous.
    Then V is a connected topological space."
    
    The dropped hypothesis is that the base field is R or C (which are connected).
    A valid counterexample is a topological vector space over a disconnected field, such as Q.
    """
    try:
        w_str = str(witness).strip().lower()
    except Exception:
        w_str = ""
        
    tvs = False
    connected = True
    
    try:
        if witness == S.Rationals:
            tvs = True
            connected = False
        elif witness in (S.Reals, S.Complexes):
            tvs = True
            connected = True
        elif witness == S.Integers:
            tvs = False
            connected = False
        elif witness == FiniteSet(0):
            tvs = True
            connected = True
        elif isinstance(witness, ProductSet):
            if all(arg == S.Rationals for arg in witness.args):
                tvs = True
                connected = False
            elif all(arg in (S.Reals, S.Complexes) for arg in witness.args):
                tvs = True
                connected = True
        else:
            # String matching for common mathematical spaces
            if w_str in ["q", "rationals", "s.rationals", "rational numbers", "mathbb{q}", "q_p", "p-adic", "rational", "qq"]:
                tvs = True
                connected = False
            elif w_str in ["r", "reals", "s.reals", "real numbers", "mathbb{r}", "c", "complexes", "s.complexes", "complex numbers", "mathbb{c}", "rr", "cc"]:
                tvs = True
                connected = True
            elif w_str in ["z", "integers", "s.integers", "integer numbers", "mathbb{z}", "zz"]:
                tvs = False
                connected = False
            elif "rationals" in w_str or "mathbb{q}" in w_str or "q_p" in w_str or "p-adic" in w_str:
                tvs = True
                connected = False
            elif w_str in ["q^n", "q2", "q^2", "q^3"]:
                tvs = True
                connected = False
    except Exception:
        pass

    return [tvs, not connected]

CONDITION_LABELS = [
    "H_1: V is equipped with a topology such that vector addition and scalar multiplication are continuous",
    "¬Q: V is not a connected topological space"
]

N_HYP = 1
NEG_Q_INDEX = 1