import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.matrices

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            y = witness.get('y')
            n = witness.get('n')
        elif hasattr(witness, 'y') and hasattr(witness, 'n'):
            y = witness.y
            n = witness.n
        else:
            y, n = witness
    except Exception:
        return [False, False]

    # H_1: y is a positive real number
    try:
        y_val = sympy.sympify(y)
        h1 = (y_val.is_real is not False) and bool(y_val > 0)
    except Exception:
        h1 = False

    # neg_Q: not (there exists a unique positive real x such that x^n = y)
    try:
        n_val = sympy.sympify(n)
        y_val = sympy.sympify(y)
        
        if n_val.is_zero:
            unique = False
        elif n_val.is_real:
            unique = True
        else:
            x = sympy.Symbol('x', positive=True, real=True)
            sols = sympy.solve(x**n_val - y_val, x)
            pos_sols = []
            for s in sols:
                try:
                    if (s.is_real is not False) and bool(s > 0):
                        pos_sols.append(s)
                except Exception:
                    pass
            unique = (len(pos_sols) == 1)
            
        neg_q = not unique
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: y is a positive real number",
    "¬Q: It is not the case that there exists a unique positive real number x such that x^n = y"
]

N_HYP = 1
NEG_Q_INDEX = 1