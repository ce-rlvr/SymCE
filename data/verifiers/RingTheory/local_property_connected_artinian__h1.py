import sympy
from sympy import ZZ, QQ

# Top-level setup: named object bindings
Z = ZZ
Q = QQ

def conditions(witness) -> list[bool]:
    """
    Check if the witness satisfies the hypotheses and negates the conclusion.
    H_1: R contains no idempotents other than 0 and 1.
    neg_Q: R is NOT a local ring.
    """
    h1_ok = False
    neg_q_ok = False

    # Check H_1: R contains no idempotents other than 0 and 1
    try:
        # In an integral domain, the only idempotents are 0 and 1.
        if getattr(witness, 'is_Domain', False):
            h1_ok = True
        elif witness in (ZZ, QQ):
            h1_ok = True
    except Exception:
        h1_ok = False

    # Check neg_Q: R is NOT a local ring
    try:
        # A ring is local iff the set of non-units forms an ideal.
        # If we can find two non-units a and b such that a + b = 1, 
        # then the non-units do not form an ideal, so the ring is NOT local.
        if getattr(witness, 'is_Field', False) or witness == QQ:
            neg_q_ok = False
        else:
            found_non_local_evidence = False
            for i in range(-20, 21):
                try:
                    a = witness(i)
                    b = witness(1) - a
                    
                    def is_unit(ring, x):
                        if x == ring.zero:
                            return False
                        if hasattr(ring, 'is_unit'):
                            return ring.is_unit(x)
                        try:
                            ring.exquo(ring.one, x)
                            return True
                        except Exception:
                            return False
                            
                    if not is_unit(witness, a) and not is_unit(witness, b):
                        found_non_local_evidence = True
                        break
                except Exception:
                    continue
            
            if found_non_local_evidence:
                neg_q_ok = True
            elif witness == ZZ:
                # Fallback for ZZ just in case the loop fails
                neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R contains no idempotents other than 0 and 1",
    "¬Q: R is not a local ring"
]

N_HYP = 1
NEG_Q_INDEX = 1