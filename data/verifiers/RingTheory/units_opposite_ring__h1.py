import sympy
from sympy.matrices import eye, zeros, MatrixBase
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.abc import x, y, z
import math
import itertools
import functools
import z3

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
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
    "H_1: R^op is the opposite ring of R",
    "H_2: u is an element of R",
    "¬Q: u is a unit in R is not equivalent to u is a unit in R^op"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    R = None
    R_op = None
    u = None
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            R_op = witness.get('R_op')
            u = witness.get('u')
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                R, u = witness
            elif len(witness) == 3:
                R, R_op, u = witness
        else:
            R = getattr(witness, 'R', None)
            R_op = getattr(witness, 'R_op', None)
            u = getattr(witness, 'u', None)
            
        if R_op is None and R is not None:
            if hasattr(R, 'opposite_ring'):
                R_op = R.opposite_ring()
            elif hasattr(R, 'op'):
                R_op = R.op
            else:
                R_op = R
    except Exception:
        pass

    h1 = False
    try:
        if R is not None and R_op is not None:
            if hasattr(R, 'is_opposite'):
                h1 = bool(R.is_opposite(R_op))
            elif hasattr(R_op, 'is_opposite'):
                h1 = bool(R_op.is_opposite(R))
            elif hasattr(R, 'opposite_ring') and R.opposite_ring() == R_op:
                h1 = True
            elif hasattr(R, 'op') and R.op == R_op:
                h1 = True
            elif getattr(R_op, 'original_ring', None) == R:
                h1 = True
            elif getattr(R_op, 'is_op_of', None) == R:
                h1 = True
            elif R == R_op:
                h1 = True
            elif hasattr(R, 'mult') and hasattr(R_op, 'mult'):
                h1 = True
                elements = list(R)[:10]
                for a in elements:
                    for b in elements:
                        if R.mult(a, b) != R_op.mult(b, a):
                            h1 = False
                            break
                    if not h1:
                        break
            else:
                if isinstance(witness, dict) and 'R_op' in witness:
                    h1 = True
                elif hasattr(witness, 'R_op'):
                    h1 = True
                elif isinstance(witness, tuple) and len(witness) == 3:
                    h1 = True
    except Exception:
        h1 = False

    h2 = False
    try:
        if R is not None and u is not None:
            if hasattr(R, '__contains__'):
                h2 = bool(u in R)
            elif hasattr(R, 'contains'):
                h2 = bool(R.contains(u))
            elif hasattr(u, 'in_ring'):
                h2 = bool(u.in_ring(R))
            else:
                try:
                    h2 = u in list(R)
                except Exception:
                    if hasattr(u, 'domain') and u.domain == R:
                        h2 = True
                    elif hasattr(R, 'has'):
                        h2 = bool(R.has(u))
                    elif isinstance(witness, dict) and 'u' in witness and 'R' in witness:
                        h2 = True
                    elif hasattr(witness, 'u') and hasattr(witness, 'R'):
                        h2 = True
                    elif isinstance(witness, tuple):
                        h2 = True
    except Exception:
        h2 = False

    neg_q = False
    try:
        def check_unit(ring, elem):
            if hasattr(ring, 'is_unit'):
                return bool(ring.is_unit(elem))
            if hasattr(elem, 'is_unit'):
                try:
                    return bool(elem.is_unit(ring))
                except TypeError:
                    return bool(elem.is_unit())
            if hasattr(ring, 'one') and hasattr(ring, 'mult'):
                for v in ring:
                    if ring.mult(elem, v) == ring.one and ring.mult(v, elem) == ring.one:
                        return True
                return False
            if hasattr(ring, 'one'):
                for v in ring:
                    if elem * v == ring.one and v * elem == ring.one:
                        return True
                return False
            if isinstance(elem, MatrixBase):
                return elem.det() != 0
            
            try:
                try:
                    inv = ~elem
                except Exception:
                    inv = elem**-1
                if hasattr(ring, '__contains__'):
                    return inv in ring
                elif hasattr(ring, 'contains'):
                    return ring.contains(inv)
            except Exception:
                pass
            
            raise ValueError("Cannot determine unit status")

        if R is not None and R_op is not None and u is not None:
            unit_in_R = check_unit(R, u)
            unit_in_R_op = check_unit(R_op, u)
            neg_q = (unit_in_R != unit_in_R_op)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]