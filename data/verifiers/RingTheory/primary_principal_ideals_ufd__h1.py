import sympy
from sympy import *
import itertools

# Top-level setup: define rings that can serve as counterexamples.
# F2_xy_ideal represents elements of the finite ring F_2[x, y] / (x^2, xy, y^2)
class F2_xy_ideal:
    def __init__(self, c0, c1, c2):
        self.c0 = c0 % 2
        self.c1 = c1 % 2
        self.c2 = c2 % 2

    def __eq__(self, other):
        if not isinstance(other, F2_xy_ideal):
            return False
        return self.c0 == other.c0 and self.c1 == other.c1 and self.c2 == other.c2

    def __add__(self, other):
        return F2_xy_ideal(self.c0 + other.c0, self.c1 + other.c1, self.c2 + other.c2)

    def __mul__(self, other):
        return F2_xy_ideal(
            self.c0 * other.c0,
            self.c0 * other.c1 + self.c1 * other.c0,
            self.c0 * other.c2 + self.c2 * other.c0
        )

    def __hash__(self):
        return hash((self.c0, self.c1, self.c2))
        
    def __repr__(self):
        return f"F2_xy_ideal({self.c0}, {self.c1}, {self.c2})"

F2_xy_elements = [F2_xy_ideal(c0, c1, c2) for c0 in (0,1) for c1 in (0,1) for c2 in (0,1)]

# Z_sqrt_minus_5 represents elements of Z[sqrt(-5)]
class Z_sqrt_minus_5:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        
    def __eq__(self, other):
        if isinstance(other, Z_sqrt_minus_5):
            return self.a == other.a and self.b == other.b
        return False
        
    def __hash__(self):
        return hash((self.a, self.b))
        
    def __repr__(self):
        return f"Z_sqrt_minus_5({self.a}, {self.b})"

def conditions(witness):
    try:
        # Handle the classic infinite ring counterexample Z[sqrt(-5)]
        if isinstance(witness, Z_sqrt_minus_5):
            a, b = witness.a, witness.b
            if a == 0 and b == 0:
                return [False, False]
            if (a == 1 and b == 0) or (a == -1 and b == 0):
                return [False, False]
            h1 = True
            # In Z[sqrt(-5)], the ideal (2) is primary, but 2 is not associate to any prime power.
            if a == 2 and b == 0:
                return [True, True]
            return [True, False]

        # Handle finite ring counterexamples
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], list):
            elements, a = witness
        elif isinstance(witness, F2_xy_ideal):
            elements = F2_xy_elements
            a = witness
        else:
            return [False, False]

        # Find zero and one in the finite ring
        zero = None
        for e in elements:
            if all(e * x == e for x in elements):
                zero = e
                break
        
        one = None
        for e in elements:
            if all(e * x == x for x in elements):
                one = e
                break

        if zero is None or one is None:
            return [False, False]

        def get_principal_ideal(x):
            I = []
            for r in elements:
                rx = r * x
                if rx not in I:
                    I.append(rx)
            return I

        I_a = get_principal_ideal(a)

        # H1: (a) is a proper, non-zero principal ideal of R
        is_proper = len(I_a) < len(elements) and one not in I_a
        is_nonzero = len(I_a) > 1 or (len(I_a) == 1 and I_a[0] != zero)
        
        h1 = is_proper and is_nonzero

        # Check if I_a is a primary ideal
        def is_primary(I):
            for x in elements:
                for y in elements:
                    if (x * y) in I:
                        if x not in I:
                            y_n = y
                            found = False
                            for n in range(1, len(elements) + 2):
                                if y_n in I:
                                    found = True
                                    break
                                y_n = y_n * y
                            if not found:
                                return False
            return True

        is_prim = is_primary(I_a)

        # Check if an element is a prime element
        def is_prime_element(p):
            I_p = get_principal_ideal(p)
            if len(I_p) == 1 or one in I_p:
                return False
            for x in elements:
                for y in elements:
                    if (x * y) in I_p:
                        if x not in I_p and y not in I_p:
                            return False
            return True

        units = [e for e in elements if any(e * x == one for x in elements)]

        def is_associate(x, y):
            for u in units:
                if x == u * y:
                    return True
            return False

        primes = [p for p in elements if is_prime_element(p)]
        
        is_assoc_to_prime_power = False
        for p in primes:
            p_n = p
            for n in range(1, len(elements) + 2):
                if is_associate(a, p_n):
                    is_assoc_to_prime_power = True
                    break
                p_n = p_n * p
            if is_assoc_to_prime_power:
                break

        # Conclusion: (a) is primary iff a is associate to p^n
        conclusion = (is_prim == is_assoc_to_prime_power)
        neg_q = not conclusion

        return [bool(h1), bool(neg_q)]

    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: (a) is a proper, non-zero principal ideal of R",
    "¬Q: (a) is primary iff a is associate to p^n for some prime p and n >= 1 FAILS"
]

N_HYP = 1
NEG_Q_INDEX = 1