import sympy
from sympy import ZZ, QQ
from sympy.polys.domains import Domain

# Top-level setup
# We provide ZZ and QQ as standard domains for the witness.
# The witness should be a tuple (R, x), for example (ZZ, 0).

def conditions(witness):
    try:
        R, x = witness
    except Exception:
        return [False, False, False]
    
    # H_1: R is a commutative Noetherian ring
    try:
        # In SymPy, all Domain objects are commutative rings.
        # Standard domains like ZZ, QQ, and their polynomial rings are Noetherian.
        h1 = isinstance(R, Domain)
    except Exception:
        h1 = False

    # H_2: R is an integral domain
    try:
        # In SymPy, Domain objects represent integral domains (or fields, which are integral domains).
        h2 = isinstance(R, Domain)
    except Exception:
        h2 = False

    # neg_Q: x CANNOT be expressed as a finite product of irreducible elements of R
    try:
        # Convert x to the domain's type if possible
        try:
            x_dom = R(x)
        except Exception:
            x_dom = x
            
        if x_dom == R.zero:
            # 0 cannot be expressed as a product of irreducibles (which are non-zero).
            neg_q = True
        else:
            # Check if x is a unit
            is_unit = False
            try:
                # In a field, all non-zero elements are units.
                if getattr(R, 'is_Field', False):
                    is_unit = True
                else:
                    # Try exact division of 1 by x
                    R.exquo(R.one, x_dom)
                    is_unit = True
            except Exception:
                is_unit = False
                
            if is_unit:
                # Units cannot be factored into irreducibles (a product of irreducibles is a non-unit,
                # unless it's the empty product which is 1. Even then, units like -1 cannot be factored).
                # We consider that units do not have irreducible factorizations.
                neg_q = True
            else:
                # In a Noetherian domain, every non-zero non-unit can be factored into irreducibles.
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: R is an integral domain",
    "¬Q: x cannot be expressed as a finite product of irreducible elements of R"
]

N_HYP = 2
NEG_Q_INDEX = 2