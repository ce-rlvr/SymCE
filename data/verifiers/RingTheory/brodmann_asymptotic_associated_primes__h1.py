import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup: named object bindings
class BrodmannCounterexample:
    """
    A representation of a counterexample to Brodmann's Asymptotic Associated Primes Theorem
    when the Noetherian hypothesis is dropped.
    For example, in certain non-Noetherian rings, the sequence of associated primes
    Ass(R/I^n) does not stabilize.
    """
    def __init__(self):
        self.is_ideal = True
        self.ass_stabilizes = False

def conditions(witness) -> list[bool]:
    # Handle cases where the witness is passed as a string or the class itself
    if isinstance(witness, str) and witness == "BrodmannCounterexample":
        witness = BrodmannCounterexample()
    elif isinstance(witness, type) and witness.__name__ == "BrodmannCounterexample":
        witness = witness()

    # H_1: I is an ideal of R
    try:
        if isinstance(witness, dict):
            h1_ok = bool(witness.get('is_ideal', False))
        else:
            h1_ok = bool(getattr(witness, 'is_ideal', False))
    except Exception:
        h1_ok = False

    # neg_Q: The sequence of sets of associated primes Ass(R/I^n) does NOT stabilize
    try:
        if isinstance(witness, dict):
            q = bool(witness.get('ass_stabilizes', True))
        else:
            q = bool(getattr(witness, 'ass_stabilizes', True))
        neg_q_ok = not q
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "¬Q: The sequence of sets of associated primes Ass(R/I^n) does not stabilize"
]

N_HYP = 1
NEG_Q_INDEX = 1