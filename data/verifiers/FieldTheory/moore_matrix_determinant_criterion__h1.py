import sympy
from sympy.combinatorics.named_groups import CyclicGroup
from sympy.matrices import eye
from sympy.ntheory import factorint
import itertools

# Top-level setup
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
I2 = eye(2)
I3 = eye(3)

def is_prime_power(n):
    if n < 2:
        return False
    factors = factorint(n)
    return len(factors) == 1

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and falsifies the conclusion.
    The witness should be a dictionary with keys: 'q', 'n', 'alphas', 'M', 
    and optionally 'F_q_elements' (the elements of the base field F_q).
    """
    try:
        if isinstance(witness, dict):
            q = witness['q']
            n = witness['n']
            alphas = witness['alphas']
            M = witness['M']
            F_q_elements = witness.get('F_q_elements', list(range(q)))
        else:
            q, n, alphas, M = witness
            F_q_elements = list(range(q))
    except Exception:
        return [False, False, False, False]

    # H_1: n is a positive integer
    try:
        h1_ok = isinstance(n, int) and n > 0
    except Exception:
        h1_ok = False

    # H_2: alphas are elements of the extension field F_{q^n}
    try:
        h2_ok = False
        if len(alphas) == n and is_prime_power(q):
            h2_ok = True
            # In a field of size q^n, every element satisfies a^(q^n) == a
            for a in alphas:
                if sympy.simplify(a**(q**n) - a) != 0:
                    h2_ok = False
                    break
    except Exception:
        h2_ok = False

    # H_3: M is the n x n Moore matrix defined by M_{i,j} = alpha_i^{q^{j-1}}
    try:
        h3_ok = False
        if getattr(M, 'shape', None) == (n, n):
            h3_ok = True
            for i in range(n):
                for j in range(n):
                    # 0-indexed j corresponds to j-1 in the 1-indexed definition
                    if sympy.simplify(M[i, j] - alphas[i]**(q**j)) != 0:
                        h3_ok = False
                        break
    except Exception:
        h3_ok = False

    # ¬Q: The determinant of M is non-zero if and only if alphas are linearly independent over F_q
    try:
        det_M = M.det()
        det_non_zero = (sympy.simplify(det_M) != 0)

        # Check linear independence over F_q
        lin_indep = True
        for coeffs in itertools.product(F_q_elements, repeat=n):
            # Skip the all-zero coefficient vector
            is_zero = True
            for c in coeffs:
                if c != 0:
                    is_zero = False
                    break
            if is_zero:
                continue
            
            # Evaluate the linear combination
            total = 0
            for c, a in zip(coeffs, alphas):
                total = total + c * a
                
            if sympy.simplify(total) == 0:
                lin_indep = False
                break
        
        # The conclusion is the iff statement. We want it to FAIL.
        neg_q_ok = (det_non_zero != lin_indep)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: alphas are elements of the extension field F_{q^n}",
    "H_3: M is the n x n Moore matrix",
    "¬Q: The equivalence (det(M) != 0 iff alphas are linearly independent over F_q) is FALSE"
]

N_HYP = 3
NEG_Q_INDEX = 3