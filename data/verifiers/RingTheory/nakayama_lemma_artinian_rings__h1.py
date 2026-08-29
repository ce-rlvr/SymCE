import sympy
from sympy import symbols, Rational, Integer

# Top-level setup: named object bindings that the witness expression may reference.
# Since SymPy lacks robust support for abstract modules and local rings, we provide
# a mock object framework for the witness to use.

class Ring:
    def __init__(self, name, J_gen=None):
        """
        name: str, name of the ring
        J_gen: generator of the Jacobson radical
        """
        self.name = str(name)
        self.J_gen = J_gen

    def __eq__(self, other):
        if not isinstance(other, Ring):
            return False
        return self.name == other.name and self.J_gen == other.J_gen

class Module:
    def __init__(self, name, ring, is_zero=False):
        """
        name: str, name of the module
        ring: Ring, the ring over which this module is defined
        is_zero: bool, whether this is the zero module
        """
        self.name = str(name)
        self.ring = ring
        self._is_zero = bool(is_zero)
        self.J_mult_result = None

    def is_zero(self):
        return self._is_zero

    def mult_by_J(self):
        # Allow explicit override by the witness
        if self.J_mult_result is not None:
            return self.J_mult_result
            
        if self._is_zero:
            return self
        
        # Standard counterexamples: Fraction field over a local domain
        # e.g., Q over Z_(p)
        if self.name.upper() == "Q" and self.ring.J_gen not in (0, None, "0"):
            return self
            
        # e.g., k((x)) over k[[x]]
        if "((x))" in self.name and "[[x]]" in self.ring.name and self.ring.J_gen not in (0, None, "0"):
            return self
            
        # Generic fraction field over local domain
        if "frac" in self.name.lower() and self.ring.J_gen not in (0, None, "0"):
            return self

        return Module(f"{self.name} * J({self.ring.name})", self.ring)

    def __eq__(self, other):
        if not isinstance(other, Module):
            return False
        return self.name == other.name and self.ring == other.ring and self._is_zero == other._is_zero

# Predefined standard counterexamples for the witness expression to reference directly
Z_2_local = Ring("Z_(2)", J_gen=2)
Q_mod_Z2 = Module("Q", Z_2_local, is_zero=False)

Z_3_local = Ring("Z_(3)", J_gen=3)
Q_mod_Z3 = Module("Q", Z_3_local, is_zero=False)

k_x_local = Ring("k[[x]]", J_gen="x")
k_x_frac = Module("k((x))", k_x_local, is_zero=False)


def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R = witness.get("R")
            M = witness.get("M")
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, M = witness
        else:
            return [False, False, False]
        
        h1 = False
        h2 = False
        neg_q = False
        
        if isinstance(R, Ring) and isinstance(M, Module):
            # H_1: M is a right R-module
            h1 = (M.ring == R)
            
            # H_2: M J(R) = M
            h2 = (M.mult_by_J() == M)
            
            # ¬Q: M is not the zero module
            neg_q = not M.is_zero()
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: M is a right R-module",
    "H_2: M J(R) = M",
    "¬Q: M is not the zero module"
]

N_HYP = 2
NEG_Q_INDEX = 2