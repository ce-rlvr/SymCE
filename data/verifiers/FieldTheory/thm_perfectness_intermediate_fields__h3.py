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

class MockField:
    """
    A mock representation of a mathematical field to evaluate the conjecture.
    """
    def __init__(self, name, is_perfect, is_alg_closed, alg_over):
        self.name = name
        self.is_perfect = is_perfect
        self.is_alg_closed = is_alg_closed
        self.alg_over = alg_over
        self.is_field = True

    def __repr__(self):
        return f"MockField({self.name})"

# Top-level setup: named object bindings that the witness expression may reference.
# These represent various fields with their known algebraic properties.
QQ = MockField("QQ", is_perfect=True, is_alg_closed=False, alg_over=["QQ"])
QQ_bar = MockField("QQ_bar", is_perfect=True, is_alg_closed=True, alg_over=["QQ", "QQ_bar"])

Fp = MockField("Fp", is_perfect=True, is_alg_closed=False, alg_over=["Fp"])
Fp_bar = MockField("Fp_bar", is_perfect=True, is_alg_closed=True, alg_over=["Fp", "Fp_bar"])

# Fp(t) is a rational function field over a finite field, which is NOT perfect.
Fp_t = MockField("Fp(t)", is_perfect=False, is_alg_closed=False, alg_over=["Fp(t)"])
Fp_t_bar = MockField("Fp_t_bar", is_perfect=True, is_alg_closed=True, alg_over=["Fp(t)", "Fp_t_bar"])

CC = MockField("CC", is_perfect=True, is_alg_closed=True, alg_over=["RR", "CC"])
RR = MockField("RR", is_perfect=True, is_alg_closed=False, alg_over=["RR"])


def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (F, E, K), checks if it is a valid counterexample to the false conjecture.
    
    Remaining hypotheses:
      - F is a perfect field
      - E is an algebraic closure of F
    Conclusion to falsify:
      - K is a perfect field
    """
    try:
        if len(witness) != 3:
            return [False, False, False]
        F, E, K = witness
    except Exception:
        return [False, False, False]

    # H_1: F is a perfect field
    try:
        h1 = getattr(F, 'is_field', False) and getattr(F, 'is_perfect', False)
    except Exception:
        h1 = False

    # H_2: E is an algebraic closure of F
    try:
        h2 = (getattr(E, 'is_field', False) and 
              getattr(E, 'is_alg_closed', False) and 
              getattr(F, 'name', None) in getattr(E, 'alg_over', []))
    except Exception:
        h2 = False

    # neg_Q: K is NOT a perfect field
    try:
        neg_q = getattr(K, 'is_field', False) and not getattr(K, 'is_perfect', True)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a perfect field",
    "H_2: E is an algebraic closure of F",
    "¬Q: K is not a perfect field"
]

N_HYP = 2
NEG_Q_INDEX = 2