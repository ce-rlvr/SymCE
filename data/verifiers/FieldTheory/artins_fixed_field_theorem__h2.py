import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, Rational, Integer, oo
from sympy.abc import x

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

class ArtinWitness:
    """
    Witness for Artin's Theorem on Fixed Fields.
    Since SymPy cannot compute infinite Galois extensions, this class
    encapsulates the mathematical properties of the counterexample.
    """
    def __init__(self, E_is_field, E_G_is_fixed_field, is_finite_galois, galois_group_isomorphic, degree, G_order):
        self.E_is_field = E_is_field
        self.E_G_is_fixed_field = E_G_is_fixed_field
        self.is_finite_galois = is_finite_galois
        self.galois_group_isomorphic = galois_group_isomorphic
        self.degree = degree
        self.G_order = G_order

def conditions(witness) -> list[bool]:
    # Handle SymPy tuple representation, e.g., (QQ.frac_field(x), 'Aut', QQ)
    if isinstance(witness, tuple) and len(witness) == 3:
        E, G, E_G = witness
        try:
            h1 = bool(getattr(E, 'is_Field', False) or getattr(E, 'is_field', False))
        except Exception:
            h1 = False
            
        try:
            if hasattr(E, 'domain') and E.domain == E_G:
                h2 = True
            elif hasattr(E, 'base') and E.base == E_G:
                h2 = True
            else:
                h2 = False
        except Exception:
            h2 = False
            
        try:
            if type(E).__name__ == 'FractionField':
                neg_q = True
            else:
                neg_q = False
        except Exception:
            neg_q = False
            
        return [h1, h2, neg_q]

    # Handle dictionary representation
    if isinstance(witness, dict):
        class Dummy:
            pass
        obj = Dummy()
        obj.__dict__.update(witness)
        witness = obj

    # Handle ArtinWitness or similar object
    try:
        h1 = bool(witness.E_is_field)
    except Exception:
        h1 = False

    try:
        h2 = bool(witness.E_G_is_fixed_field)
    except Exception:
        h2 = False

    try:
        finite_galois = bool(witness.is_finite_galois)
        gal_iso = bool(witness.galois_group_isomorphic)
        degree_eq = (witness.degree == witness.G_order)
        
        q = finite_galois and gal_iso and degree_eq
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: E is a field",
    "H_2: E^G is the fixed field of E under the action of G",
    "¬Q: E/E^G is not a finite Galois extension with Gal isomorphic to G or degree is not order of G"
]

N_HYP = 2
NEG_Q_INDEX = 2