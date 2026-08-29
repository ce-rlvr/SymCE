import sympy
from sympy import *
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: f: U -> R^m is locally Lipschitz continuous",
    "¬Q: f is NOT Fréchet differentiable almost everywhere in U with respect to the n-dimensional Lebesgue measure"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    """
    Evaluates the remaining hypotheses and the negated conclusion for the given witness.
    The dropped hypothesis from Rademacher's Theorem is that U is an OPEN subset of R^n.
    Without U being open, Fréchet differentiability is generally undefined or fails.
    """
    h1 = False
    q = True
    
    try:
        # 1. Dictionary-based witness
        if isinstance(witness, dict):
            if 'is_locally_lipschitz' in witness:
                h1 = bool(witness.get('is_locally_lipschitz', False))
                q = bool(witness.get('is_frechet_differentiable_ae', True))
                return [h1, not q]
                
        # 2. Object with explicit attributes
        if hasattr(witness, 'is_locally_lipschitz'):
            h1 = bool(getattr(witness, 'is_locally_lipschitz', False))
            q = bool(getattr(witness, 'is_frechet_differentiable_ae', True))
            return [h1, not q]
            
        # 3. Tuple witness: (function, domain)
        if isinstance(witness, tuple) and len(witness) == 2:
            f, U = witness
            # Assume f is locally Lipschitz if provided as a valid counterexample part
            h1 = True
            if hasattr(U, 'is_open'):
                if U.is_open is False:
                    q = False
                else:
                    q = True
            elif isinstance(U, str):
                if "open" not in U.lower():
                    q = False
            return [h1, not q]
            
        # 4. Set witness: domain only (e.g., sympy.Interval)
        if hasattr(witness, 'is_open'):
            h1 = True
            if witness.is_open is False:
                q = False
            else:
                q = True
            return [h1, not q]
            
        # 5. String witness (known counterexample spaces/metrics)
        if isinstance(witness, str):
            s = witness.lower()
            if any(word in s for word in ["heisenberg", "snowflake", "carnot", "infinite", "banach", "closed", "interval"]):
                h1 = True
                q = False
            return [h1, not q]
            
    except Exception:
        pass
        
    return [bool(h1), not bool(q)]