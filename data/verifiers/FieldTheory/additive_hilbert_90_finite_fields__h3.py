import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros, Matrix
from sympy.ntheory import factorint

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
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The dropped hypothesis is "Let alpha \in E". Without it, alpha can be an element
    of any F_q-algebra (e.g., a matrix ring or a direct product ring).
    """
    try:
        if len(witness) == 3:
            q, n, alpha = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: q is a prime power (F_q is a finite field)
    try:
        q_val = int(q)
        if q_val > 1:
            factors = factorint(q_val)
            h1 = len(factors) == 1
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: n is a positive integer (E is a finite extension)
    try:
        n_val = int(n)
        h2 = n_val >= 1
    except Exception:
        h2 = False

    # neg_Q: The conclusion fails
    try:
        if isinstance(alpha, Matrix):
            trace_alpha = alpha
            current_term = alpha
            for i in range(1, n_val):
                current_term = current_term**q_val
                trace_alpha = trace_alpha + current_term
            
            trace_alpha = trace_alpha.applyfunc(lambda x: x % q_val)
            is_trace_zero = all(x == 0 for x in trace_alpha)
            
            is_scalar_matrix = False
            if alpha.rows == alpha.cols:
                is_scalar = True
                val = alpha[0, 0]
                for r in range(alpha.rows):
                    for c in range(alpha.cols):
                        if r == c and alpha[r, c] != val:
                            is_scalar = False
                        if r != c and alpha[r, c] != 0:
                            is_scalar = False
                is_scalar_matrix = is_scalar
            
            if is_scalar_matrix:
                iff_holds = True
            else:
                rhs_any = False
                iff_holds = (is_trace_zero == rhs_any)
            
            neg_q = not iff_holds

        elif isinstance(alpha, tuple) or isinstance(alpha, list):
            trace_alpha = list(alpha)
            current_term = list(alpha)
            for i in range(1, n_val):
                current_term = [(x**q_val) % q_val for x in current_term]
                trace_alpha = [(trace_alpha[j] + current_term[j]) % q_val for j in range(len(alpha))]
            
            is_trace_zero = all(x == 0 for x in trace_alpha)
            
            rhs_any = False
            iff_holds = (is_trace_zero == rhs_any)
            neg_q = not iff_holds

        else:
            neg_q = False
            
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: q is a prime power (F_q is a finite field)",
    "H_2: n is a positive integer (E is a finite extension)",
    "¬Q: Tr_{E/F_q}(alpha) = 0 does NOT hold if and only if exists beta in E such that alpha = beta^q - beta"
]

N_HYP = 2
NEG_Q_INDEX = 2