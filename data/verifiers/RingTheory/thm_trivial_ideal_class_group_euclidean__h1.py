import sympy
import sympy.combinatorics.named_groups as named_groups
import sympy.matrices
import math
import re

# Top-level setup
S3 = named_groups.SymmetricGroup(3)
S4 = named_groups.SymmetricGroup(4)
A4 = named_groups.AlternatingGroup(4)
D4 = named_groups.DihedralGroup(4)
C4 = named_groups.CyclicGroup(4)
Z2 = named_groups.CyclicGroup(2)
Z3 = named_groups.CyclicGroup(3)
Z4 = named_groups.CyclicGroup(4)
Z6 = named_groups.CyclicGroup(6)
trivial = named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def get_d(witness):
    """
    Attempt to extract the square-free integer d < 0 from the witness,
    representing the imaginary quadratic field Q(sqrt(d)).
    """
    if isinstance(witness, (list, tuple)) and len(witness) > 0:
        return get_d(witness[0])
        
    try:
        if int(witness) == witness:
            return int(witness)
    except Exception:
        pass
    
    s = str(witness)
    
    # Match patterns like Q(sqrt(-5)) or Z[sqrt(-5)]
    m = re.search(r'sqrt\((-?\d+)\)', s)
    if m:
        return int(m.group(1))
        
    # Match patterns like I*sqrt(5)
    if 'I' in s and 'sqrt' in s:
        m = re.search(r'sqrt\((\d+)\)', s)
        if m:
            return -int(m.group(1))
            
    # Match just a number in a string
    m = re.search(r'^-?\d+$', s.strip())
    if m:
        return int(m.group(0))
        
    raise ValueError("Could not extract d from witness")

def is_squarefree(n):
    n = abs(n)
    if n == 0:
        return False
    for i in range(2, math.isqrt(n) + 1):
        if n % (i * i) == 0:
            return False
    return True

def class_number(d):
    """
    Computes the class number of the imaginary quadratic field Q(sqrt(d)).
    """
    if d >= 0:
        return 1
    
    if d % 4 == 1:
        D = d
    else:
        D = 4 * d
        
    h = 0
    max_a = math.floor(math.sqrt(-D / 3.0))
    for a in range(1, max_a + 1):
        for b in range(-a, a + 1):
            rem = b**2 - D
            if rem % (4 * a) == 0:
                c = rem // (4 * a)
                if a <= c:
                    # Reduced form conditions
                    if (b == -a or a == c) and b < 0:
                        continue
                    # Primitive form condition
                    if math.gcd(a, math.gcd(abs(b), c)) == 1:
                        h += 1
    return h

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    Returns [neg_Q_ok]
    """
    try:
        d = get_d(witness)
        if d >= 0:
            neg_q = False
        elif not is_squarefree(d):
            neg_q = False
        else:
            h = class_number(d)
            neg_q = (h > 1)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The ideal class group of R is not trivial"
]

N_HYP = 0
NEG_Q_INDEX = 0