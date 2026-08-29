import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness references
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
    Checks the hypotheses and negated conclusion for the false conjecture:
    "The Lagrange resolvent (alpha, zeta) satisfies sigma((alpha, zeta)) = zeta * (alpha, zeta)"
    where the hypothesis alpha \in K was dropped.
    
    Expected witness dictionary format:
    {
        'n': int (degree of extension),
        'zeta': sympy expression (primitive n-th root of unity),
        'sigma': callable (automorphism acting on expressions),
        'theta': sympy expression (generator of K/F),
        'alpha': sympy expression (element for which the resolvent relation fails)
    }
    """
    try:
        n = int(witness['n'])
        zeta = sympy.sympify(witness['zeta'])
        sigma = witness['sigma']
        theta = sympy.sympify(witness['theta'])
        alpha = sympy.sympify(witness['alpha'])
    except Exception:
        return [False, False, False, False]
        
    # H_1: K/F is a cyclic Galois extension of degree n
    # We verify n >= 2 and that sigma acts as a homomorphism on the generator theta
    try:
        h1 = False
        if n >= 2:
            t1 = sympy.simplify(sigma(theta**2) - sigma(theta)**2) == 0
            t2 = sympy.simplify(sigma(theta + 1) - (sigma(theta) + 1)) == 0
            if t1 and t2:
                h1 = True
    except Exception:
        h1 = False

    # H_2: F contains a primitive n-th root of unity zeta
    # We verify zeta is a primitive n-th root and is fixed by sigma (so it's in F)
    try:
        h2 = False
        if sympy.simplify(zeta**n - 1) == 0:
            is_prim = True
            for k in range(1, n):
                if sympy.simplify(zeta**k - 1) == 0:
                    is_prim = False
                    break
            if is_prim and sympy.simplify(sigma(zeta) - zeta) == 0:
                h2 = True
    except Exception:
        h2 = False

    # H_3: sigma is a generator of the Galois group Gal(K/F)
    # We verify sigma has exact order n on the generator theta
    try:
        h3 = False
        val = theta
        has_order_n = True
        for k in range(1, n):
            val = sigma(val)
            if sympy.simplify(val - theta) == 0:
                has_order_n = False
                break
        if has_order_n:
            val = sigma(val)
            if sympy.simplify(val - theta) == 0:
                h3 = True
    except Exception:
        h3 = False

    # neg_Q: The Lagrange resolvent relation sigma((alpha, zeta)) == zeta * (alpha, zeta) fails
    try:
        resolvent = 0
        curr_alpha = alpha
        for i in range(n):
            resolvent += (zeta**(-i)) * curr_alpha
            curr_alpha = sigma(curr_alpha)
            
        lhs = sigma(resolvent)
        rhs = zeta * resolvent
        
        neg_q = sympy.simplify(lhs - rhs) != 0
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K/F is a cyclic Galois extension of degree n",
    "H_2: F contains a primitive n-th root of unity zeta",
    "H_3: sigma is a generator of the Galois group Gal(K/F)",
    "¬Q: The Lagrange resolvent relation sigma((alpha, zeta)) == zeta * (alpha, zeta) fails"
]

N_HYP = 3
NEG_Q_INDEX = 3