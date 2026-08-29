import sympy
from sympy import ZZ, QQ, RR, CC
from sympy.polys.domains import Domain
from sympy.abc import x, y, z

# Top-level setup
# (No specific named bindings needed for this domain beyond standard sympy domains)

def conditions(witness):
    """
    Given a witness (which may be a ring R or a tuple (R, I)),
    check if it satisfies the remaining hypotheses and falsifies the conclusion.
    """
    try:
        if isinstance(witness, tuple):
            R = witness[0]
        else:
            R = witness
            
        # H_1: R is a commutative Noetherian ring
        h1_ok = False
        if isinstance(R, Domain):
            # In sympy, standard domains (ZZ, QQ, etc.) and polynomial rings 
            # over them with finitely many generators are commutative Noetherian rings.
            if hasattr(R, 'gens') and len(R.gens) > 100:
                h1_ok = False
            else:
                h1_ok = True
        elif R in [ZZ, QQ, RR, CC]:
            h1_ok = True
            
        # neg_Q: The I-adic completion of R is not a Noetherian ring
        # Mathematically, the I-adic completion of a commutative Noetherian ring is ALWAYS Noetherian.
        # Therefore, if R is a commutative Noetherian ring, the conclusion holds, so neg_Q is False.
        # If R is not Noetherian, its completion (e.g., with I=(0)) is not Noetherian, so neg_Q is True.
        neg_q_ok = not h1_ok
        
        return [bool(h1_ok), bool(neg_q_ok)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "¬Q: The I-adic completion of R is not a Noetherian ring"
]

N_HYP = 1
NEG_Q_INDEX = 1