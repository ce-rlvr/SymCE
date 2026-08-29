import sympy
from sympy import ZZ, QQ, RR, CC
import math
import itertools
import functools

# Top-level setup
# No specific named bindings needed for RingTheory beyond standard domains.

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, int) or (hasattr(witness, 'is_Integer') and witness.is_Integer):
            w_list = [witness]
        elif isinstance(witness, (list, tuple)):
            w_list = witness
        else:
            w_list = list(witness)
            
        parsed_witness = []
        for x in w_list:
            if x in (ZZ, QQ, RR, CC):
                parsed_witness.append(x)
            elif isinstance(x, int):
                parsed_witness.append(x)
            elif hasattr(x, 'mod'):
                parsed_witness.append(int(x.mod))
            elif hasattr(x, 'order'):
                if callable(x.order):
                    parsed_witness.append(int(x.order()))
                else:
                    parsed_witness.append(int(x.order))
            else:
                parsed_witness.append(int(x))
                
        h1 = len(parsed_witness) > 0 and all(
            (n in (ZZ, QQ, RR, CC)) or (isinstance(n, int) and n >= 2)
            for n in parsed_witness
        )
    except Exception:
        h1 = False
        parsed_witness = []

    try:
        if not h1:
            neg_q = False
        else:
            is_boolean = True
            for n in parsed_witness:
                if n in (ZZ, QQ, RR, CC):
                    is_boolean = False
                    break
                for x in range(n):
                    if (x**2) % n != x:
                        is_boolean = False
                        break
                if not is_boolean:
                    break
            neg_q = not is_boolean
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a direct product of rings",
    "¬Q: R is not a Boolean ring"
]

N_HYP = 1
NEG_Q_INDEX = 1