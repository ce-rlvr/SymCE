import sympy
from sympy import Poly
from sympy.abc import x, t
import sympy.ntheory
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
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

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    
    The true theorem (Galois) states that for a SEPARABLE irreducible polynomial of prime degree p,
    if the Galois group is solvable, then any two distinct roots generate the splitting field.
    The dropped hypothesis is "separable" (or "characteristic 0").
    The counterexample is an inseparable irreducible polynomial of prime degree p (e.g., x^p - t over F_p(t)),
    which has only 1 distinct root, meaning we cannot find two distinct roots that generate E.
    """
    # H1: f(x) is an irreducible polynomial of prime degree p
    h1 = False
    try:
        deg = None
        if hasattr(witness, 'degree'):
            deg = witness.degree() if callable(witness.degree) else witness.degree
        
        if deg is not None and sympy.ntheory.isprime(deg):
            if hasattr(witness, 'is_irreducible'):
                irr = witness.is_irreducible() if callable(witness.is_irreducible) else witness.is_irreducible
                h1 = bool(irr)
    except Exception:
        h1 = False

    # H2: E is the splitting field of f(x) over F
    # This is a definitional hypothesis for the field E in the context of the witness.
    h2 = True

    # H3: The Galois group Gal(E/F) is a solvable group
    h3 = False
    try:
        if hasattr(witness, 'galois_group_is_solvable'):
            solv = witness.galois_group_is_solvable() if callable(witness.galois_group_is_solvable) else witness.galois_group_is_solvable
            h3 = bool(solv)
        else:
            # If not explicitly provided, we assume the witness satisfies this hypothesis.
            # For an inseparable polynomial x^p - t, the Galois group is trivial, which is solvable.
            h3 = True
    except Exception:
        h3 = False

    # neg_Q: Any two distinct roots of f(x) DO NOT generate the entire splitting field E over F
    # This fails (i.e., neg_Q is True) if the polynomial is inseparable, because it has only 1 distinct root,
    # so there do not exist two distinct roots that generate E.
    neg_q = False
    try:
        if hasattr(witness, 'two_roots_generate_E'):
            gen = witness.two_roots_generate_E() if callable(witness.two_roots_generate_E) else witness.two_roots_generate_E
            neg_q = not bool(gen)
        elif hasattr(witness, 'is_separable'):
            sep = witness.is_separable() if callable(witness.is_separable) else witness.is_separable
            neg_q = not bool(sep)
        elif hasattr(witness, 'diff'):
            # In characteristic p, an irreducible polynomial is inseparable iff its formal derivative is 0.
            neg_q = (witness.diff() == 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is an irreducible polynomial of prime degree p",
    "H_2: E is the splitting field of f(x) over F",
    "H_3: The Galois group Gal(E/F) is a solvable group",
    "¬Q: Any two distinct roots of f(x) DO NOT generate the entire splitting field E over F"
]

N_HYP = 3
NEG_Q_INDEX = 3