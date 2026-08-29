import sympy
from sympy import Rational, Integer, pi, E, sqrt
from sympy.abc import x, y, z
import sympy.combinatorics
import sympy.matrices

# Standard algebra objects
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The dropped hypothesis was the definition of the sequences a and b as the 
    continued fraction expansions of x and y. Without it, a and b are free variables,
    and the equivalence does not hold for arbitrary sequences.
    Witness format expected: (x, y, a, b)
    """
    try:
        if len(witness) != 4:
            return [False, False]
        x_val, y_val, a, b = witness
    except Exception:
        return [False, False]
    
    # H1: x and y are irrational numbers
    try:
        h1 = bool(x_val.is_irrational and y_val.is_irrational)
    except Exception:
        h1 = False

    # neg_Q: The conclusion fails
    try:
        # LHS: a and b are eventually the same
        lhs = False
        if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
            a_list = list(a)
            b_list = list(b)
            for N in range(len(a_list)):
                for M in range(len(b_list)):
                    if a_list[N:] == b_list[M:] and len(a_list[N:]) > 0:
                        lhs = True
                        break
                if lhs: break
        elif callable(a) and callable(b):
            for N in range(10):
                for M in range(10):
                    match = True
                    for k in range(20):
                        if a(N+k) != b(M+k):
                            match = False
                            break
                    if match:
                        lhs = True
                        break
                if lhs: break
        else:
            lhs = False

        # RHS: x and y are equivalent (i.e., related by a fractional linear transformation)
        # By Serret's Theorem, this is true iff their actual continued fractions are eventually the same.
        def get_cf(val, depth=200):
            cf = []
            v = val.evalf(500)
            for _ in range(depth):
                f = int(sympy.floor(v))
                cf.append(f)
                v = v - f
                if v < 1e-100:
                    break
                v = 1 / v
            return cf
        
        cf_x = get_cf(x_val, 200)
        cf_y = get_cf(y_val, 200)
        
        rhs = False
        tail_x = cf_x[-100:]
        if len(tail_x) == 100:
            for i in range(len(cf_y) - 100 + 1):
                if cf_y[i:i+100] == tail_x:
                    rhs = True
                    break
        
        # The conclusion is an if-and-only-if statement. It fails if LHS != RHS.
        neg_q = (lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x and y are irrational numbers",
    "¬Q: The equivalence between the sequence condition and the fractional linear transformation fails"
]
N_HYP = 1
NEG_Q_INDEX = 1