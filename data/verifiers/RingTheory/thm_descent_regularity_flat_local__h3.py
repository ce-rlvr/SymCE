import sympy

class RingHomomorphismWitness:
    """
    A mock object representing a ring homomorphism f: R -> S
    along with the relevant abstract algebraic properties.
    """
    def __init__(self, R_is_Noetherian_local, S_is_Noetherian_local, f_is_flat_local, R_is_regular_local):
        self.R_is_Noetherian_local = R_is_Noetherian_local
        self.S_is_Noetherian_local = S_is_Noetherian_local
        self.f_is_flat_local = f_is_flat_local
        self.R_is_regular_local = R_is_regular_local

# A valid counterexample: R = k[x]/(x^2), S = k[x]/(x^2), f = id
# R and S are Noetherian local rings, f is flat local, but R is not regular.
Counterexample = RingHomomorphismWitness(
    R_is_Noetherian_local=True,
    S_is_Noetherian_local=True,
    f_is_flat_local=True,
    R_is_regular_local=False
)

def conditions(witness) -> list[bool]:
    if isinstance(witness, str):
        witness = globals().get(witness, witness)
        
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('R_is_Noetherian_local', False) and witness.get('S_is_Noetherian_local', False))
            h2 = bool(witness.get('f_is_flat_local', False))
            neg_q = not bool(witness.get('R_is_regular_local', True))
        elif isinstance(witness, (list, tuple)) and len(witness) >= 4:
            h1 = bool(witness[0] and witness[1])
            h2 = bool(witness[2])
            neg_q = not bool(witness[3])
        else:
            h1 = bool(witness.R_is_Noetherian_local and witness.S_is_Noetherian_local)
            h2 = bool(witness.f_is_flat_local)
            neg_q = not bool(witness.R_is_regular_local)
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are Noetherian local rings",
    "H_2: f: R -> S is a flat local homomorphism",
    "¬Q: R is not a regular local ring"
]

N_HYP = 2
NEG_Q_INDEX = 2