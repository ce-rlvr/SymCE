import sympy
import sympy.combinatorics
import sympy.matrices
import math
from itertools import product

# Top-level setup
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    try:
        # Handle standard infinite domains
        if witness == sympy.ZZ or witness == sympy.QQ:
            is_prufer = True
            is_gaussian = True
            conclusion = (is_prufer == is_gaussian)
            return [not conclusion]
            
        # Parse witness as an integer n representing the ring Z/nZ
        n = None
        if isinstance(witness, (list, tuple)):
            n = 1
            for x in witness:
                n *= int(x)
        elif isinstance(witness, str):
            witness = witness.strip()
            import re
            m = re.search(r'Z/(\d+)Z', witness)
            if m:
                n = int(m.group(1))
            else:
                m = re.search(r'Z_(\d+)', witness)
                if m:
                    n = int(m.group(1))
                else:
                    n = int(witness)
        else:
            n = int(witness)
            
        if n < 2:
            return [False]
            
        # P: R is a Prüfer domain
        # A Prüfer domain must be an integral domain.
        # Z/nZ is an integral domain iff n is prime.
        is_prufer = sympy.isprime(n)
        
        # Q: c(fg) = c(f)c(g) for all f, g in R[x] (Gaussian ring property)
        # Z/nZ is always a Gaussian ring, as it is a quotient of Z (which is Gaussian).
        # We verify this property for polynomials of degree <= 1 if n <= 20.
        is_gaussian = True
        if n <= 20:
            coeffs = list(range(n))
            polys = list(product(coeffs, repeat=2))
            for f in polys:
                for g in polys:
                    f0, f1 = f
                    g0, g1 = g
                    
                    # Content of f and g
                    cf = math.gcd(math.gcd(f0, f1), n)
                    cg = math.gcd(math.gcd(g0, g1), n)
                    cfcg = math.gcd(cf * cg, n)
                    
                    # Coefficients of fg
                    fg0 = (f0 * g0) % n
                    fg1 = (f0 * g1 + f1 * g0) % n
                    fg2 = (f1 * g1) % n
                    
                    # Content of fg
                    cfg = math.gcd(math.gcd(math.gcd(fg0, fg1), fg2), n)
                    
                    if cfcg != cfg:
                        is_gaussian = False
                        break
                if not is_gaussian:
                    break
        else:
            # For larger n, we rely on the mathematical guarantee to keep it fast
            is_gaussian = True
            
        # The conclusion is the equivalence P <==> Q
        conclusion = (is_prufer == is_gaussian)
        neg_q = not conclusion
        
        return [neg_q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: The equivalence 'R is a Prüfer domain iff c(fg) = c(f)c(g)' fails"
]
N_HYP = 0
NEG_Q_INDEX = 0