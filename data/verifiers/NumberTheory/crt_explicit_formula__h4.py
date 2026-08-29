import sympy
import math

# Top-level setup
# (No named bindings needed for this Number Theory conjecture)

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the Chinese Remainder Theorem formula.
    The dropped hypothesis is that a_1, ..., a_k are integers.
    """
    try:
        if isinstance(witness, dict):
            m = list(witness["m"])
            a = list(witness["a"])
            y = list(witness["y"])
        elif isinstance(witness, (list, tuple)) and len(witness) == 3:
            m = list(witness[0])
            a = list(witness[1])
            y = list(witness[2])
        else:
            return [False, False, False, False]
        k = len(m)
    except Exception:
        return [False, False, False, False]

    # H1: m_1, ..., m_k are pairwise coprime positive integers
    h1 = True
    try:
        if k < 1:
            h1 = False
        if len(a) != k or len(y) != k:
            h1 = False
        for mi in m:
            mi_sym = sympy.sympify(mi)
            if mi_sym.is_integer != True or mi_sym <= 0:
                h1 = False
                break
        if h1:
            for i in range(k):
                for j in range(i + 1, k):
                    if math.gcd(int(sympy.sympify(m[i])), int(sympy.sympify(m[j]))) != 1:
                        h1 = False
                        break
    except Exception:
        h1 = False

    # H2: M_i = M / m_i for each 1 <= i <= k
    h2 = True
    try:
        M = math.prod(int(sympy.sympify(mi)) for mi in m)
        M_i = [M // int(sympy.sympify(mi)) for mi in m]
        if isinstance(witness, dict):
            if "M" in witness and witness["M"] != M:
                h2 = False
            if "M_i" in witness and list(witness["M_i"]) != M_i:
                h2 = False
    except Exception:
        h2 = False

    # H3: y_i is an integer such that M_i y_i = 1 (mod m_i) for each 1 <= i <= k
    h3 = True
    try:
        for i in range(k):
            yi_sym = sympy.sympify(y[i])
            if yi_sym.is_integer != True:
                h3 = False
                break
            yi = int(yi_sym)
            mi = int(sympy.sympify(m[i]))
            if (M_i[i] * yi) % mi != 1 % mi:
                h3 = False
                break
    except Exception:
        h3 = False

    # ¬Q: The integer x = sum(a_i M_i y_i) is a solution to x = a_i (mod m_i)
    # Negation: x is not an integer, or x is not a solution.
    neg_q = False
    try:
        x = sum(sympy.sympify(a[i]) * M_i[i] * int(sympy.sympify(y[i])) for i in range(k))
        is_solution = True
        
        x_sym = sympy.sympify(x)
        if x_sym.is_integer != True:
            is_solution = False
        else:
            for i in range(k):
                diff = x_sym - sympy.sympify(a[i])
                quot = diff / int(sympy.sympify(m[i]))
                if sympy.sympify(quot).is_integer != True:
                    is_solution = False
                    break
        neg_q = not is_solution
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: m_1, ..., m_k are pairwise coprime positive integers",
    "H_2: M_i = M / m_i for each 1 <= i <= k",
    "H_3: y_i is an integer such that M_i y_i = 1 (mod m_i) for each 1 <= i <= k",
    "¬Q: x is not an integer or not a solution to x = a_i (mod m_i)"
]

N_HYP = 3
NEG_Q_INDEX = 3