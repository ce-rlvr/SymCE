import sympy
import math

def _get_val(witness):
    if isinstance(witness, dict):
        if 'sigma_0' in witness:
            return float(witness['sigma_0'])
        elif 'sigma0' in witness:
            return float(witness['sigma0'])
        else:
            if len(witness) == 1:
                return float(list(witness.values())[0])
            raise ValueError("Missing sigma_0 in dictionary witness")
    return float(witness)

def conditions(witness):
    try:
        # H_1: F is the family of normal probability density functions
        # This is a definitional hypothesis, we just verify the witness is a valid numeric sigma_0
        sigma_0 = _get_val(witness)
        h1_ok = True
    except Exception:
        h1_ok = False

    try:
        # H_2: The parameters satisfy mu in R and sigma >= sigma_0
        # Again, this sets the context for the parameter sigma_0
        sigma_0 = _get_val(witness)
        h2_ok = True
    except Exception:
        h2_ok = False

    try:
        # ¬Q: The family F is NOT uniformly equicontinuous
        # The maximum derivative of the normal PDF is proportional to 1/sigma^2.
        # For the family to be uniformly equicontinuous, the derivative must be uniformly bounded,
        # which requires sigma to be bounded away from 0.
        # If sigma_0 <= 0, then sigma can be arbitrarily close to 0 (since sigma > 0 is required for a valid PDF).
        # In this case, the family is not uniformly equicontinuous.
        sigma_0 = _get_val(witness)
        neg_q_ok = bool(sigma_0 <= 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is the family of normal probability density functions",
    "H_2: The parameters satisfy mu in R and sigma >= sigma_0",
    "¬Q: The family F is not uniformly equicontinuous"
]

N_HYP = 2
NEG_Q_INDEX = 2