import sympy
from sympy.abc import X, Y, Z
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    neg_q = False
    
    try:
        n = int(witness)
        if n > 1 and not sympy.isprime(n):
            neg_q = True
        elif n == 1:
            neg_q = True
    except Exception:
        pass
        
    try:
        s = str(witness).lower()
        if "matrix" in s or "m_2" in s or "m2" in s:
            neg_q = True
        if "zmod" in s or "z/" in s or "quotient" in s or "z_" in s:
            num_str = "".join(c if c.isdigit() else " " for c in s)
            nums = num_str.split()
            for num in nums:
                n = int(num)
                if n > 1 and not sympy.isprime(n):
                    neg_q = True
                    break
    except Exception:
        pass

    try:
        if hasattr(witness, 'is_integral_domain') and witness.is_integral_domain is False:
            neg_q = True
        if hasattr(witness, 'is_IntegralDomain') and witness.is_IntegralDomain is False:
            neg_q = True
    except Exception:
        pass

    try:
        if isinstance(witness, (list, tuple)) and len(witness) >= 2:
            F, G = witness[0], witness[1]
            prod = sympy.expand(F * G)
            diff = sympy.expand(prod - (X**2 - Y*Z))
            if len(witness) == 3:
                n = int(witness[2])
                coeffs = diff.as_coefficients_dict().values()
                if all(c % n == 0 for c in coeffs):
                    if not F.is_number and not G.is_number:
                        neg_q = True
            else:
                if diff == 0:
                    if not F.is_number and not G.is_number:
                        neg_q = True
    except Exception:
        pass

    return [neg_q]

CONDITION_LABELS = ["¬Q: The polynomial X^2 - Y Z is not absolutely irreducible"]
N_HYP = 0
NEG_Q_INDEX = 0