import sympy
import sympy.ntheory
import sympy.combinatorics.named_groups
import sympy.matrices
import math

# Top-level setup
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    # H_1: k >= 3
    try:
        h1 = bool(witness >= 3)
    except Exception:
        h1 = False

    # neg_Q: lambda(2^k) != 2^{k-2}
    try:
        k = witness
        two_k = 2**k
        
        is_int = False
        if isinstance(two_k, int):
            is_int = True
            two_k_int = two_k
        elif isinstance(two_k, sympy.Integer):
            is_int = True
            two_k_int = int(two_k)
        else:
            try:
                if hasattr(two_k, 'evalf'):
                    val = two_k.evalf()
                else:
                    val = two_k
                
                fval = float(val)
                if math.isfinite(fval) and fval.is_integer():
                    is_int = True
                    two_k_int = int(fval)
            except Exception:
                pass
                
        if is_int:
            left = sympy.ntheory.reduced_totient(two_k_int)
            right = 2**(k - 2)
            
            try:
                is_eq = (left == right)
                if isinstance(is_eq, bool):
                    neg_q = not is_eq
                else:
                    neg_q = not bool(sympy.simplify(left - right) == 0)
            except Exception:
                neg_q = True
        else:
            # If 2^k is not an integer, the Carmichael function is undefined,
            # so the equality lambda(2^k) == 2^{k-2} fails.
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: k >= 3",
    "¬Q: lambda(2^k) != 2^{k-2}"
]

N_HYP = 1
NEG_Q_INDEX = 1