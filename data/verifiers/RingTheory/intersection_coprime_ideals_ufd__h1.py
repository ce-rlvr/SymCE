import math
import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

# Expected witness format:
# witness = (n, a, b, y_elem)
# where:
#   n (int): a negative integer, defining the ring R = ZZ[\sqrt{n}]
#   a (tuple): (a0, a1) representing a0 + a1*sqrt(n) in R
#   b (tuple): (b0, b1) representing b0 + b1*sqrt(n) in R
#   y_elem (tuple): (y0, y1) representing y0 + y1*sqrt(n) in R
# The witness demonstrates that a and b are coprime, but the element
# b * y_elem is in (a) \cap (b) and not in (ab), so (a) \cap (b) != (ab).

def norm(elem, n):
    return elem[0]**2 - n * elem[1]**2

def mult(elem1, elem2, n):
    return (elem1[0]*elem2[0] + n*elem1[1]*elem2[1], elem1[0]*elem2[1] + elem1[1]*elem2[0])

def divides(elem1, elem2, n):
    nx = norm(elem1, n)
    if nx == 0:
        return elem2[0] == 0 and elem2[1] == 0
    num_z0 = elem2[0]*elem1[0] - n*elem1[1]*elem2[1]
    num_z1 = elem1[0]*elem2[1] - elem1[1]*elem2[0]
    return num_z0 % nx == 0 and num_z1 % nx == 0

def are_coprime(a, b, n):
    na = norm(a, n)
    nb = norm(b, n)
    if na == 0 or nb == 0:
        return False
    g = math.gcd(na, nb)
    divisors = []
    for i in range(1, math.isqrt(g) + 1):
        if g % i == 0:
            divisors.append(i)
            if i * i != g:
                divisors.append(g // i)
    abs_n = -n
    for k in divisors:
        if k == 1:
            continue
        max_y = math.isqrt(k // abs_n)
        for y_val in range(-max_y, max_y + 1):
            rem = k - abs_n * y_val**2
            if rem >= 0:
                x_val = math.isqrt(rem)
                if x_val * x_val == rem:
                    elem1 = (x_val, y_val)
                    if divides(elem1, a, n) and divides(elem1, b, n):
                        return False
                    elem2 = (-x_val, y_val)
                    if divides(elem2, a, n) and divides(elem2, b, n):
                        return False
    return True

def conditions(witness):
    # H_1: a and b are non-zero elements of R
    try:
        n, a, b, y_elem = witness
        h1 = (isinstance(n, int) and n < 0 and
              isinstance(a, tuple) and len(a) == 2 and isinstance(a[0], int) and isinstance(a[1], int) and
              isinstance(b, tuple) and len(b) == 2 and isinstance(b[0], int) and isinstance(b[1], int) and
              a != (0, 0) and b != (0, 0))
    except Exception:
        h1 = False

    # H_2: a and b are coprime
    try:
        if h1:
            n, a, b, y_elem = witness
            h2 = are_coprime(a, b, n)
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: The intersection of the principal ideals (a) and (b) is not the principal ideal (ab)
    try:
        if h1:
            n, a, b, y_elem = witness
            if not (isinstance(y_elem, tuple) and len(y_elem) == 2 and isinstance(y_elem[0], int) and isinstance(y_elem[1], int)):
                neg_q = False
            else:
                by = mult(b, y_elem, n)
                in_intersection = divides(a, by, n)
                not_in_ab = not divides(a, y_elem, n)
                neg_q = in_intersection and not_in_ab
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a and b are non-zero elements of R",
    "H_2: a and b are coprime",
    "¬Q: The intersection of the principal ideals (a) and (b) is not the principal ideal (ab)"
]

N_HYP = 2
NEG_Q_INDEX = 2