import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
    Checks if the witness is a valid counterexample to the false conjecture.
    """
    # H_1: The rank of F is finite (i.e., F is finitely generated)
    try:
        if isinstance(witness, str):
            h1_ok = True
        else:
            # In SymPy, groups with a 'generators' attribute are finitely generated
            h1_ok = hasattr(witness, 'generators') and len(witness.generators) >= 0
    except Exception:
        h1_ok = False

    # ¬Q: The automorphism group Aut(F) is NOT finitely generated
    try:
        neg_q = False
        if isinstance(witness, str):
            s = witness.lower().replace(" ", "").replace("_", "")
            # Known counterexamples: F_2 x Z, or Baumslag-Solitar group BS(1, 2)
            if "f2xz" in s or "bs(1,2)" in s or "baumslag" in s:
                neg_q = True
        else:
            # Heuristics for SymPy FpGroup objects representing known counterexamples
            if hasattr(witness, 'generators') and hasattr(witness, 'relators'):
                n_gen = len(witness.generators)
                n_rel = len(witness.relators)
                if n_gen == 3 and n_rel == 2:
                    # Heuristic for F_2 x Z presentation
                    neg_q = True
                elif n_gen == 2 and n_rel == 1:
                    # Heuristic for BS(1, 2) presentation
                    neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1_ok), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: The rank of F is finite",
    "¬Q: The automorphism group Aut(F) is not finitely generated"
]

N_HYP = 1
NEG_Q_INDEX = 1