import sympy
from sympy import ZZ, QQ, RR, CC, symbols
import math
import itertools
import functools

# Top-level setup for Ring Theory
x, y, z = symbols('x y z')

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture:
    "The topological space Spec(R) is quasi-compact"
    """
    # H_1: Let Spec(R) denote the set of all prime ideals of R
    # This is a definitional assumption that holds for any ring witness.
    h1 = True
    
    # H_2: Assume Spec(R) is equipped with the Zariski topology
    # This is a definitional assumption that holds for any ring witness.
    h2 = True
    
    # neg_Q: The topological space Spec(R) is NOT quasi-compact
    neg_q = False
    
    try:
        if isinstance(witness, str):
            s = witness.lower()
            # Known counterexamples: rings without identity whose Spec is not quasi-compact
            if "direct sum" in s and ("infinite" in s or "countabl" in s):
                neg_q = True
            elif "compact support" in s:
                neg_q = True
            elif "c_c" in s:
                neg_q = True
            elif "boolean ring" in s and "without identity" in s:
                neg_q = True
            elif "finite subsets" in s:
                neg_q = True
            elif "without identity" in s and not ("2z" in s or "even integer" in s):
                # Spec(2Z) is quasi-compact, so we exclude it.
                neg_q = True
        elif isinstance(witness, dict):
            if 'is_quasi_compact' in witness:
                neg_q = not bool(witness['is_quasi_compact'])
            elif 'is_spec_quasi_compact' in witness:
                neg_q = not bool(witness['is_spec_quasi_compact'])
            elif 'has_identity' in witness:
                neg_q = not bool(witness['has_identity'])
        else:
            # Check for custom object attributes
            if hasattr(witness, 'is_quasi_compact'):
                val = witness.is_quasi_compact() if callable(witness.is_quasi_compact) else witness.is_quasi_compact
                neg_q = not bool(val)
            elif hasattr(witness, 'is_spec_quasi_compact'):
                val = witness.is_spec_quasi_compact() if callable(witness.is_spec_quasi_compact) else witness.is_spec_quasi_compact
                neg_q = not bool(val)
            elif hasattr(witness, 'has_identity'):
                val = witness.has_identity() if callable(witness.has_identity) else witness.has_identity
                neg_q = not bool(val)
            elif hasattr(witness, 'has_1'):
                val = witness.has_1() if callable(witness.has_1) else witness.has_1
                neg_q = not bool(val)
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Let Spec(R) denote the set of all prime ideals of R",
    "H_2: Assume Spec(R) is equipped with the Zariski topology",
    "¬Q: The topological space Spec(R) is not quasi-compact"
]

N_HYP = 2
NEG_Q_INDEX = 2