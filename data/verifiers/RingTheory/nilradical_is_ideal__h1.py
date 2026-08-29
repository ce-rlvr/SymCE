import sympy
from sympy import Matrix, eye, zeros
from sympy import abc
import itertools

# Top-level setup
def _make_Zn(n):
    elements = list(range(n))
    zero = 0
    def add(a, b): return (a + b) % n
    def mul(a, b): return (a * b) % n
    return elements, add, mul, zero

Z2 = _make_Zn(2)
Z3 = _make_Zn(3)
Z4 = _make_Zn(4)
Z6 = _make_Zn(6)

def _make_M2_Z2():
    elements = [Matrix(2, 2, [a, b, c, d]) for a in (0, 1) for b in (0, 1) for c in (0, 1) for d in (0, 1)]
    zero = Matrix(2, 2, [0, 0, 0, 0])
    def add(A, B):
        return (A + B).applyfunc(lambda x: x % 2)
    def mul(A, B):
        return (A * B).applyfunc(lambda x: x % 2)
    return elements, add, mul, zero

M2_Z2 = _make_M2_Z2()

CONDITION_LABELS = [
    "H_1: N is the set of nilpotent elements of R",
    "¬Q: N is not an ideal of R"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 4:
            R, add, mul, zero = witness
            R = list(R)
        elif hasattr(witness, 'elements') and hasattr(witness, 'add') and hasattr(witness, 'mul') and hasattr(witness, 'zero'):
            R = list(witness.elements)
            add = witness.add
            mul = witness.mul
            zero = witness.zero
        else:
            R = list(witness)
            add = lambda a, b: a + b
            mul = lambda a, b: a * b
            zero = None
            for e in R:
                if all(add(x, e) == x for x in R):
                    zero = e
                    break
            if zero is None:
                return [False, False]

        if not R:
            return [False, False]

        # Check closure to ensure R is a valid ring
        if len(R) <= 100:
            for a in R:
                for b in R:
                    if add(a, b) not in R:
                        return [False, False]
                    if mul(a, b) not in R:
                        return [False, False]

        max_power = len(R) if hasattr(R, '__len__') else 100
        N = []
        for x in R:
            curr = x
            is_nil = False
            for _ in range(max_power):
                if curr == zero:
                    is_nil = True
                    break
                curr = mul(curr, x)
            if is_nil:
                N.append(x)

        h1_ok = (zero in N)

        is_ideal = True
        
        # Check closed under addition
        for a in N:
            for b in N:
                if add(a, b) not in N:
                    is_ideal = False
                    break
            if not is_ideal:
                break
                
        # Check additive inverse in N
        if is_ideal:
            for a in N:
                has_inv = False
                for b in N:
                    if add(a, b) == zero and add(b, a) == zero:
                        has_inv = True
                        break
                if not has_inv:
                    is_ideal = False
                    break

        # Check absorbs multiplication
        if is_ideal:
            for a in N:
                for r in R:
                    if mul(a, r) not in N or mul(r, a) not in N:
                        is_ideal = False
                        break
                if not is_ideal:
                    break

        neg_q = not is_ideal

        return [h1_ok, neg_q]
    except Exception:
        return [False, False]