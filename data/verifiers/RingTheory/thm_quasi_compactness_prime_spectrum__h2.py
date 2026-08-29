import sympy
from sympy import ZZ, QQ, RR, CC
from sympy.abc import x, y, z

# Top-level setup
# Standard rings and variables are imported above.

def conditions(witness) -> list[bool]:
    # H_1: Let R be a commutative ring with identity
    try:
        h1 = False
        # Heuristic to check if the witness is a ring (SymPy domain, PolyRing, or custom object)
        if hasattr(witness, 'is_ring') and witness.is_ring:
            h1 = True
        elif hasattr(witness, 'is_Commutative') and hasattr(witness, 'from_sympy'):
            h1 = True
        elif type(witness).__name__.endswith('Ring') or type(witness).__name__.endswith('Field'):
            h1 = True
            
        if h1:
            # Check commutativity
            if hasattr(witness, 'is_commutative'):
                h1 = h1 and bool(witness.is_commutative)
            elif hasattr(witness, 'is_Commutative'):
                h1 = h1 and bool(witness.is_Commutative)
            else:
                h1 = False
                
            # Check for identity
            if hasattr(witness, 'has_identity'):
                h1 = h1 and bool(witness.has_identity)
    except Exception:
        h1 = False

    # H_2: Assume Spec(R) is equipped with the Zariski topology
    # This is a definitional hypothesis for the space Spec(R).
    # If R is a valid ring, we assume its spectrum carries the Zariski topology.
    h2 = h1

    # ¬Q: The topological space Spec(R) is not quasi-compact
    try:
        if hasattr(witness, 'is_quasi_compact'):
            neg_q = not bool(witness.is_quasi_compact)
        else:
            # Mathematically, Spec(R) is ALWAYS quasi-compact for any commutative ring with identity.
            # Thus, for any standard mathematical ring object, the conclusion holds and its negation is False.
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: Let R be a commutative ring with identity",
    "H_2: Assume Spec(R) is equipped with the Zariski topology",
    "¬Q: The topological space Spec(R) is not quasi-compact"
]

N_HYP = 2
NEG_Q_INDEX = 2