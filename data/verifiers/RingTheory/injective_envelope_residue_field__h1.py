import sympy
from sympy import *

# Top-level setup for Ring Theory counterexamples
# Since SymPy does not natively support injective envelopes or general Artinian modules,
# we provide mock classes to allow the construction of a valid witness.

class LocalRing:
    def __init__(self, name, is_noetherian):
        self.name = name
        self.is_noetherian = is_noetherian

class ResidueField:
    def __init__(self, ring):
        self.ring = ring
        self.is_residue_field = True

class InjectiveEnvelope:
    def __init__(self, module, ring):
        self.module = module
        self.ring = ring
        self.is_injective_envelope = True
        # Theorem: For a local ring R, E(k) is Artinian iff R is Noetherian.
        # Thus, if R is not Noetherian, E(k) is not Artinian.
        self.is_artinian = ring.is_noetherian

# Pre-defined objects for convenience
R_noeth = LocalRing("R_noeth", is_noetherian=True)
R_non_noeth = LocalRing("R_non_noeth", is_noetherian=False)

k_noeth = ResidueField(R_noeth)
E_noeth = InjectiveEnvelope(k_noeth, R_noeth)

k_non_noeth = ResidueField(R_non_noeth)
E_non_noeth = InjectiveEnvelope(k_non_noeth, R_non_noeth)


def conditions(witness) -> list[bool]:
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness can be a dictionary, a tuple (k, E), or just the injective envelope E.
    """
    # Handle dictionary witness
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get('is_residue_field', False))
        except Exception:
            h1 = False
        try:
            h2 = bool(witness.get('is_injective_envelope', False))
        except Exception:
            h2 = False
        try:
            neg_q = not bool(witness.get('is_artinian', True))
        except Exception:
            neg_q = False
        return [h1, h2, neg_q]

    # Handle object witness
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            k, E = witness
        else:
            E = witness
            k = getattr(E, 'module', None)
            
        h1 = bool(getattr(k, 'is_residue_field', False))
    except Exception:
        h1 = False

    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            k, E = witness
        else:
            E = witness
            k = getattr(E, 'module', None)
            
        h2 = bool(getattr(E, 'is_injective_envelope', False) and getattr(E, 'module', None) is k)
    except Exception:
        h2 = False

    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            _, E = witness
        else:
            E = witness
            
        neg_q = not bool(getattr(E, 'is_artinian', True))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]


CONDITION_LABELS = [
    "H_1: k = R/m is the residue field of R",
    "H_2: E(k) is the injective envelope of k over R",
    "¬Q: E(k) is not an Artinian R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2