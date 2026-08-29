import sympy
from sympy import symbols
import math

# Top-level setup for potential witness expressions
Zmod = lambda n: n
ZZ = sympy.S.Integers
QQ = sympy.S.Rationals

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, J = witness
        elif isinstance(witness, tuple) and len(witness) == 3:
            R = witness
            J = None
        else:
            R = witness
            J = None
    except Exception:
        return [False, False, False]

    h1 = False
    h2 = False
    neg_q = False

    try:
        if isinstance(R, (int, sympy.Integer)) and R >= 2:
            R = int(R)
            h1 = True
            expected_J = set()
            for x in range(R):
                is_in_J = True
                for r in range(R):
                    if math.gcd(1 - r * x, R) != 1:
                        is_in_J = False
                        break
                if is_in_J:
                    expected_J.add(x)
            
            if J is None:
                J_set = expected_J
                h2 = True
            else:
                try:
                    J_set = set(int(x) % R for x in J)
                    h2 = (J_set == expected_J)
                except Exception:
                    h2 = False
                    J_set = set()
            
            neg_q = (J_set != {0})
            
        elif isinstance(R, tuple) and len(R) == 3:
            elements, add_table, mul_table = R
            n_el = len(elements)
            identity = None
            for e_idx in range(n_el):
                if all(mul_table[e_idx][i] == i and mul_table[i][e_idx] == i for i in range(n_el)):
                    identity = e_idx
                    break
            if identity is not None:
                h1 = True
                expected_J_idx = set()
                for x_idx in range(n_el):
                    is_in_J = True
                    for r_idx in range(n_el):
                        rx = mul_table[r_idx][x_idx]
                        y_idx = None
                        for i in range(n_el):
                            if add_table[i][rx] == identity:
                                y_idx = i
                                break
                        if y_idx is None:
                            is_in_J = False
                            break
                        is_unit = False
                        for z in range(n_el):
                            if mul_table[y_idx][z] == identity and mul_table[z][y_idx] == identity:
                                is_unit = True
                                break
                        if not is_unit:
                            is_in_J = False
                            break
                    if is_in_J:
                        expected_J_idx.add(x_idx)
                
                expected_J = {elements[i] for i in expected_J_idx}
                if J is None:
                    J_set = expected_J
                    h2 = True
                else:
                    try:
                        J_set = set(J)
                        h2 = (J_set == expected_J)
                    except Exception:
                        h2 = False
                        J_set = set()
                
                zero_idx = None
                for e_idx in range(n_el):
                    if all(add_table[e_idx][i] == i and add_table[i][e_idx] == i for i in range(n_el)):
                        zero_idx = e_idx
                        break
                if zero_idx is not None:
                    zero_el = elements[zero_idx]
                    neg_q = (J_set != {zero_el})
                else:
                    neg_q = False
            else:
                h1 = False
                h2 = False
                neg_q = False
        else:
            h1 = False
            h2 = False
            neg_q = False
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R has a multiplicative identity",
    "H_2: J is the Jacobson radical of R",
    "¬Q: J != {0}"
]

N_HYP = 2
NEG_Q_INDEX = 2