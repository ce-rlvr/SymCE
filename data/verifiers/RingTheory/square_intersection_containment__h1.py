import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.combinatorics.permutations import *
from sympy.matrices import *
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *
import z3
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "H_2: J is an ideal of R",
    "¬Q: (I \\cap J)^2 \\not\\subseteq IJ"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    # Try sympy witness first
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            R, I_gens, J_gens = witness
            if hasattr(R, 'ideal'):
                I = R.ideal(*I_gens)
                J = R.ideal(*J_gens)
                I_cap_J = I.intersection(J)
                sq = I_cap_J * I_cap_J
                IJ = I * J
                is_subset = all(IJ.contains(g) for g in sq.gens)
                return [True, True, not is_subset]
    except Exception:
        pass

    try:
        if hasattr(witness, 'R') and hasattr(witness, 'I') and hasattr(witness, 'J'):
            R = witness.R
            I = witness.I
            J = witness.J
            if hasattr(I, 'intersection') and hasattr(I, '__mul__'):
                I_cap_J = I.intersection(J)
                sq = I_cap_J * I_cap_J
                IJ = I * J
                if hasattr(sq, 'gens') and hasattr(IJ, 'contains'):
                    is_subset = all(IJ.contains(g) for g in sq.gens)
                    return [True, True, not is_subset]
    except Exception:
        pass

    # Finite ring witness
    h1 = False
    h2 = False
    neg_q = False

    try:
        if isinstance(witness, dict):
            elements = witness.get('R', witness.get('elements', []))
            add_func = witness.get('add')
            mul_func = witness.get('mul')
            I = witness.get('I', [])
            J = witness.get('J', [])
            zero = witness.get('zero')
        else:
            elements = getattr(witness, 'R', getattr(witness, 'elements', []))
            add_func = getattr(witness, 'add', None)
            mul_func = getattr(witness, 'mul', None)
            I = getattr(witness, 'I', [])
            J = getattr(witness, 'J', [])
            zero = getattr(witness, 'zero', None)

        if not elements or add_func is None or mul_func is None:
            return [False, False, False]

        elements = list(elements)
        I = list(I)
        J = list(J)

        def get_op(op_func):
            if callable(op_func):
                return op_func
            elif isinstance(op_func, dict):
                if op_func and isinstance(next(iter(op_func.keys())), tuple):
                    return lambda x, y: op_func[(x, y)]
                else:
                    return lambda x, y: op_func[x][y]
            else:
                return lambda x, y: op_func[elements.index(x)][elements.index(y)]

        add = get_op(add_func)
        mul = get_op(mul_func)

        if zero is None:
            for e in elements:
                if all(add(e, x) == x and add(x, e) == x for x in elements):
                    zero = e
                    break

        if zero is None:
            return [False, False, False]

        def is_ideal(subset):
            if not subset:
                return False
            for x in subset:
                for y in subset:
                    if add(x, y) not in subset:
                        return False
            if zero not in subset:
                return False
            for x in subset:
                if not any(add(x, y) == zero for y in subset):
                    return False
            for x in subset:
                for r in elements:
                    if mul(r, x) not in subset:
                        return False
                    if mul(x, r) not in subset:
                        return False
            return True

        try:
            h1 = is_ideal(I)
        except Exception:
            h1 = False

        try:
            h2 = is_ideal(J)
        except Exception:
            h2 = False

        try:
            I_cap_J = [x for x in I if x in J]

            def additive_closure(gens):
                closure = set(gens)
                if not closure:
                    closure.add(zero)
                added = True
                while added:
                    added = False
                    new_elements = set()
                    for x in closure:
                        for y in closure:
                            s = add(x, y)
                            if s not in closure and s not in new_elements:
                                new_elements.add(s)
                    if new_elements:
                        closure.update(new_elements)
                        added = True
                return closure

            def ideal_product(A, B):
                gens = set()
                for a in A:
                    for b in B:
                        gens.add(mul(a, b))
                return additive_closure(gens)

            sq = ideal_product(I_cap_J, I_cap_J)
            IJ = ideal_product(I, J)

            is_subset = sq.issubset(IJ)
            neg_q = not is_subset
        except Exception:
            neg_q = False

    except Exception:
        pass

    return [h1, h2, neg_q]