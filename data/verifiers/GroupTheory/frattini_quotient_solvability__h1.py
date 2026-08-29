import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Check if the witness is a counterexample to the false conjecture:
    "If G/Phi(G) is solvable, then G is solvable."
    (This is true for finite groups, so the counterexample must be an infinite group).
    """
    h1 = False
    try:
        if isinstance(witness, dict):
            if 'frattini_quotient_is_solvable' in witness:
                h1 = bool(witness['frattini_quotient_is_solvable'])
            elif 'G_mod_Phi_is_solvable' in witness:
                h1 = bool(witness['G_mod_Phi_is_solvable'])
            elif 'is_solvable' in witness:
                h1 = bool(witness['is_solvable'])
        elif hasattr(witness, 'frattini_quotient_is_solvable'):
            val = witness.frattini_quotient_is_solvable
            h1 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'is_frattini_quotient_solvable'):
            val = witness.is_frattini_quotient_solvable
            h1 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'G_mod_Phi_is_solvable'):
            val = witness.G_mod_Phi_is_solvable
            h1 = bool(val() if callable(val) else val)
        elif isinstance(witness, tuple) and len(witness) == 2:
            G = witness[0]
            if hasattr(G, 'is_solvable'):
                val = G.is_solvable
                h1 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'is_solvable'):
            # For finite groups, G/Phi(G) is solvable iff G is solvable.
            # Since no finite group can be a counterexample, this fallback is mathematically safe.
            val = witness.is_solvable
            h1 = bool(val() if callable(val) else val)
    except Exception:
        pass

    neg_q = False
    try:
        if isinstance(witness, dict):
            if 'is_solvable' in witness:
                neg_q = not bool(witness['is_solvable'])
        else:
            if isinstance(witness, tuple) and len(witness) == 2:
                G = witness[0]
            else:
                G = witness
                
            if hasattr(G, 'is_solvable'):
                val = G.is_solvable
                is_solv = bool(val() if callable(val) else val)
                neg_q = not is_solv
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G/Phi(G) is solvable",
    "¬Q: G is not solvable"
]

N_HYP = 1
NEG_Q_INDEX = 1