import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def conditions(witness):
    h1 = False
    try:
        if witness == sympy.S.Integers:
            h1 = True
        elif type(witness).__name__ == 'FreeGroup' and len(witness.generators) == 1:
            h1 = True
        elif hasattr(witness, 'is_infinite_cyclic'):
            h1 = bool(witness.is_infinite_cyclic() if callable(witness.is_infinite_cyclic) else witness.is_infinite_cyclic)
        elif isinstance(witness, dict) and 'is_infinite_cyclic' in witness:
            h1 = bool(witness['is_infinite_cyclic'])
        elif hasattr(witness, 'group'):
            g = witness.group
            if g == sympy.S.Integers:
                h1 = True
            elif type(g).__name__ == 'FreeGroup' and len(g.generators) == 1:
                h1 = True
            elif hasattr(g, 'is_infinite_cyclic'):
                h1 = bool(g.is_infinite_cyclic() if callable(g.is_infinite_cyclic) else g.is_infinite_cyclic)
            elif isinstance(g, str):
                s = g.lower()
                words = s.replace(',', ' ').replace('.', ' ').split()
                h1 = 'z' in words or 'infinite cyclic' in s or 'integers' in s
        elif isinstance(witness, str):
            s = witness.lower()
            words = s.replace(',', ' ').replace('.', ' ').split()
            h1 = 'z' in words or 'infinite cyclic' in s or 'integers' in s
    except Exception:
        h1 = False

    neg_q = False
    try:
        dual_is_s1 = True
        if hasattr(witness, 'dual_is_S1'):
            dual_is_s1 = bool(witness.dual_is_S1() if callable(witness.dual_is_S1) else witness.dual_is_S1)
        elif isinstance(witness, dict) and 'dual_is_S1' in witness:
            dual_is_s1 = bool(witness['dual_is_S1'])
        elif hasattr(witness, 'pontryagin_dual'):
            dual = witness.pontryagin_dual
            if callable(dual):
                dual = dual()
            if isinstance(dual, str):
                s = dual.lower()
                dual_is_s1 = 's^1' in s or 's1' in s or 'circle' in s
            elif hasattr(dual, 'is_S1'):
                dual_is_s1 = bool(dual.is_S1() if callable(dual.is_S1) else dual.is_S1)
        elif hasattr(witness, 'topology'):
            top = witness.topology
            if isinstance(top, str):
                if 'trivial' in top.lower() or 'indiscrete' in top.lower() or 'non-discrete' in top.lower() or 'not discrete' in top.lower():
                    dual_is_s1 = False
        elif isinstance(witness, dict) and 'topology' in witness:
            top = witness['topology']
            if isinstance(top, str):
                if 'trivial' in top.lower() or 'indiscrete' in top.lower() or 'non-discrete' in top.lower() or 'not discrete' in top.lower():
                    dual_is_s1 = False
        elif isinstance(witness, str):
            s = witness.lower()
            if 'trivial' in s or 'indiscrete' in s or 'non-discrete' in s or 'not discrete' in s:
                dual_is_s1 = False
        
        neg_q = not dual_is_s1
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is the infinite cyclic group Z",
    "¬Q: \widehat{G} is not isomorphic as a topological group to the circle group S^1"
]

N_HYP = 1
NEG_Q_INDEX = 1