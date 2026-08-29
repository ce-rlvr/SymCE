import sympy as sp
import math

# Top-level setup: named object bindings that the witness expression may reference.
x, y, z = sp.symbols('x y z')
sqrt2i = sp.sqrt(-2)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Let N: R \ {0} -> N be defined by N(a+b*sqrt(-2)) = a^2 + 2b^2. 
    Then R is a Euclidean domain with Euclidean function N."
    
    The dropped hypothesis was "Let R = Z[sqrt(-2)]".
    A valid counterexample is a subring of Z[sqrt(-2)] (to satisfy H1) 
    that is NOT Euclidean with N (to satisfy neg_Q).
    Such subrings are of the form Z[k*sqrt(-2)] for integer k >= 2.
    """
    k = None
    
    try:
        if type(witness) is int:
            k = witness
        elif isinstance(witness, str):
            w = witness.replace(' ', '')
            if 'sqrt(-2)' in w:
                if w == 'Z[sqrt(-2)]':
                    k = 1
                elif w.startswith('Z[') and w.endswith('*sqrt(-2)]'):
                    num_str = w[2:-10]
                    if num_str.isdigit():
                        k = int(num_str)
                elif w.startswith('Z[') and w.endswith('sqrt(-2)]'):
                    num_str = w[2:-9]
                    if num_str.isdigit():
                        k = int(num_str)
            elif w == 'Z':
                k = 0
        elif isinstance(witness, (list, tuple, set)):
            k_temp = 0
            valid = True
            for w in witness:
                expr = sp.sympify(w)
                if expr.is_integer is True:
                    continue
                coeff = expr.coeff(sp.sqrt(-2))
                const = expr - coeff * sp.sqrt(-2)
                if const.is_integer is not True or coeff.is_integer is not True:
                    valid = False
                    break
                if int(coeff) != 0:
                    val = abs(int(coeff))
                    if k_temp == 0:
                        k_temp = val
                    else:
                        k_temp = math.gcd(k_temp, val)
            if valid and k_temp is not None:
                k = k_temp
        else:
            try:
                expr = sp.sympify(witness)
                if expr.is_integer is True:
                    k = 0
                else:
                    coeff = expr.coeff(sp.sqrt(-2))
                    const = expr - coeff * sp.sqrt(-2)
                    if const.is_integer is True and coeff.is_integer is True:
                        k = abs(int(coeff))
            except Exception:
                pass
    except Exception:
        pass

    # H1: N is defined on R \ {0} -> N by N(a+b*sqrt(-2)) = a^2 + 2b^2
    # This implies R is a subring of Z[sqrt(-2)], which means k is a non-negative integer.
    try:
        h1_ok = (k is not None and type(k) is int and k >= 0)
    except Exception:
        h1_ok = False
    
    # neg_Q: R is NOT a Euclidean domain with Euclidean function N
    # Z[k*sqrt(-2)] is Euclidean with N if and only if k = 0 or k = 1.
    # Therefore, it fails to be Euclidean with N for k >= 2.
    try:
        neg_q = (h1_ok and k >= 2)
    except Exception:
        neg_q = False
        
    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: Let N: R \\ {0} -> N be defined by N(a+b*sqrt(-2)) = a^2 + 2b^2",
    "¬Q: R is NOT a Euclidean domain with Euclidean function N"
]

N_HYP = 1
NEG_Q_INDEX = 1