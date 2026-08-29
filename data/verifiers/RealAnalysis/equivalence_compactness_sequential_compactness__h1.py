import sympy
import math
import itertools
import functools

# Top-level setup
omega_1 = "omega_1"
beta_N = "beta N"

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, str):
            w_lower = witness.lower().strip()
            if w_lower in [
                "beta n", 
                "stone-cech compactification of n", 
                "[0,1]^[0,1]", 
                "uncountable product of [0,1]",
                "i^i",
                "2^r",
                "2^c",
                "novak space",
                "extended long line"
            ]:
                compact = True
                seq_compact = False
            elif w_lower in [
                "omega_1", 
                "[0, omega_1)", 
                "first uncountable ordinal",
                "long line",
                "closed long ray"
            ]:
                compact = False
                seq_compact = True
            elif w_lower in ["[0,1]", "s1", "sphere", "compact metric space"]:
                compact = True
                seq_compact = True
            elif w_lower in ["r", "r^n", "real line"]:
                compact = False
                seq_compact = False
            else:
                return [False]
        elif isinstance(witness, dict):
            if "compact" in witness and "sequentially_compact" in witness:
                compact = bool(witness["compact"])
                seq_compact = bool(witness["sequentially_compact"])
            else:
                return [False]
        elif hasattr(witness, "compact") and hasattr(witness, "sequentially_compact"):
            compact = bool(witness.compact)
            seq_compact = bool(witness.sequentially_compact)
        elif isinstance(witness, (list, tuple)) and len(witness) == 2:
            compact = bool(witness[0])
            seq_compact = bool(witness[1])
        else:
            return [False]
            
        neg_q = (compact != seq_compact)
        
        return [neg_q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: X is sequentially compact if and only if every open cover of X has a finite subcover (fails)"
]

N_HYP = 0
NEG_Q_INDEX = 0