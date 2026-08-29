import sympy
from sympy import Rational
import math
import functools

# Expected witness format:
# A tuple (d, gens) where:
# - d is a negative square-free integer (e.g., -5)
# - gens is a list of tuples (a, b) representing the generators a + b*omega
#   of the fractional ideal, where a, b can be integers or rationals.
#   omega is sqrt(d) if d = 2, 3 mod 4, and (1 + sqrt(d))/2 if d = 1 mod 4.

CONDITION_LABELS = [
    "H_1: I is an invertible fractional ideal of R",
    "¬Q: I is not a principal fractional ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1

def gcdex(a, b):
    """Extended Euclidean Algorithm."""
    x0, x1 = 1, 0
    y0, y1 = 0, 1
    while b != 0:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return x0, y0, a

def multi_gcd(lst):
    """Computes the GCD of a list of numbers and the coefficients of Bezout's identity."""
    if not lst:
        return 0, []
    g = lst[0]
    coeffs = [1]
    for i in range(1, len(lst)):
        x, y, g_new = gcdex(g, lst[i])
        coeffs = [c * x for c in coeffs]
        coeffs.append(y)
        g = g_new
    if g < 0:
        g = -g
        coeffs = [-c for c in coeffs]
    return g, coeffs

def conditions(witness):
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False]
        d, gens = witness
        
        if not isinstance(d, int) or d >= 0:
            return [False, False]
            
        # Check if d is square-free
        factors = sympy.factorint(abs(d))
        if any(e > 1 for e in factors.values()):
            return [False, False]
            
        if not isinstance(gens, list) or len(gens) == 0:
            return [False, False]
            
        # Parse generators
        parsed_gens = []
        for g in gens:
            if not isinstance(g, (tuple, list)) or len(g) != 2:
                return [False, False]
            a, b = sympy.Rational(g[0]), sympy.Rational(g[1])
            parsed_gens.append((a, b))
            
        if all(a == 0 and b == 0 for a, b in parsed_gens):
            return [False, False] # Zero ideal is not invertible
            
        # H1: I is an invertible fractional ideal of R
        # In the ring of integers of a number field (a Dedekind domain), 
        # every non-zero finitely generated fractional ideal is invertible.
        h1_ok = True
        
        # Compute the Z-basis of the ideal
        # First, multiply generators by 1 and omega to get Z-generators
        vectors = []
        for a, b in parsed_gens:
            vectors.append((a, b))
            if d % 4 == 1:
                # omega^2 = omega + (d-1)/4
                # omega * (a + b omega) = b (d-1)/4 + (a + b) omega
                vectors.append((b * sympy.Rational(d - 1, 4), a + b))
            else:
                # omega^2 = d
                # omega * (a + b omega) = b d + a omega
                vectors.append((b * d, a))
                
        # Find common denominator to work with integer vectors
        denoms = [sympy.Rational(v[0]).q for v in vectors] + [sympy.Rational(v[1]).q for v in vectors]
        C = functools.reduce(sympy.lcm, denoms)
        
        # Scale to integer vectors
        V = [(int(v[0] * C), int(v[1] * C)) for v in vectors]
        
        # Compute Hermite Normal Form (HNF) for the 2D lattice
        y_coords = [v[1] for v in V]
        g_y, coeffs = multi_gcd(y_coords)
        
        if g_y == 0:
            return [False, False] # Should not happen for a non-zero ideal in O_K
            
        x_0 = sum(c * V[i][0] for i, c in enumerate(coeffs))
        
        U_x = []
        for v in V:
            mult = v[1] // g_y
            U_x.append(v[0] - mult * x_0)
            
        g_x = abs(functools.reduce(math.gcd, U_x))
        if g_x > 0:
            x_0 = x_0 % g_x
        else:
            x_0 = 0
            
        if g_x == 0:
            return [False, False]
            
        # Check if the ideal is principal
        # An ideal is principal iff there exists an element in it with norm equal to the ideal's norm.
        is_principal = False
        
        if d % 4 == 1:
            # Norm equation: (2X + Y)^2 - d Y^2 = 4 g_x g_y
            max_v2 = (4 * g_x) // (-d * g_y)
            max_v = math.isqrt(max_v2) + 1
            if max_v > 100000:
                return [False, False] # Prevent DOS
                
            for v in range(-max_v, max_v + 1):
                Y = v * g_y
                rem = 4 * g_x * g_y + d * Y**2
                if rem >= 0:
                    W = math.isqrt(rem)
                    if W**2 == rem:
                        for sign in (1, -1):
                            num = sign * W - Y
                            if num % 2 == 0:
                                X = num // 2
                                if (X - v * x_0) % g_x == 0:
                                    is_principal = True
                                    break
                        if is_principal:
                            break
        else:
            # Norm equation: X^2 - d Y^2 = g_x g_y
            max_v2 = g_x // (-d * g_y)
            max_v = math.isqrt(max_v2) + 1
            if max_v > 100000:
                return [False, False] # Prevent DOS
                
            for v in range(-max_v, max_v + 1):
                Y = v * g_y
                rem = g_x * g_y + d * Y**2
                if rem >= 0:
                    X = math.isqrt(rem)
                    if X**2 == rem:
                        for sign in (1, -1):
                            X_signed = sign * X
                            if (X_signed - v * x_0) % g_x == 0:
                                is_principal = True
                                break
                        if is_principal:
                            break
                            
        neg_q_ok = not is_principal
        
        return [h1_ok, neg_q_ok]
        
    except Exception:
        return [False, False]