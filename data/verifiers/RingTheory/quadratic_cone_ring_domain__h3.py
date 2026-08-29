import sympy
from sympy import symbols, Poly, GF, QQ, ZZ

# Top-level setup: named object bindings
x, y, z = symbols('x y z')

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    F = None
    gens = {x, y, z}
    
    # Extract the field F and the generators from the witness
    try:
        items_to_check = []
        if isinstance(witness, (tuple, list)):
            items_to_check = list(witness)
        elif isinstance(witness, dict):
            items_to_check = list(witness.values())
        else:
            items_to_check = [witness]
            
        for item in items_to_check:
            if hasattr(item, 'is_Field') and item.is_Field:
                F = item
            elif hasattr(item, 'domain') and item.domain.is_Field:
                F = item.domain
                if hasattr(item, 'gens'):
                    gens = set(item.gens)
            elif isinstance(item, (int, sympy.Integer)):
                try:
                    F = GF(int(item))
                except Exception:
                    pass
    except Exception:
        pass

    # H_1: Let F be a field.
    try:
        h1 = F is not None and F.is_Field
    except Exception:
        h1 = False

    # H_2: Let R be the polynomial ring in three variables over F.
    try:
        h2 = h1 and gens == {x, y, z}
    except Exception:
        h2 = False

    # not Q: The factor ring R/I is NOT an integral domain.
    # For the Quadratic Cone Ring Domain Theorem, I = <x^2 + y^2 - z^2>.
    # R/I is an integral domain iff x^2 + y^2 - z^2 is irreducible over F.
    try:
        if h1:
            p = Poly(x**2 + y**2 - z**2, x, y, z, domain=F)
            try:
                _, factors = p.factor_list()
                neg_q = len(factors) > 1 or (len(factors) == 1 and factors[0][1] > 1)
            except Exception:
                neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: R is the polynomial ring in three variables over F",
    "not Q: The factor ring R/I is not an integral domain"
]

N_HYP = 2
NEG_Q_INDEX = 2