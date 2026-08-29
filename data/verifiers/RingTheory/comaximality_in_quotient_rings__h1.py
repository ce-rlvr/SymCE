import math
import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness expressions
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: K is a proper ideal of R",
    "H_2: I and J are ideals of R that both contain K",
    "¬Q: I and J are comaximal in R iff I/K and J/K are comaximal in R/K fails"
]

N_HYP = 2
NEG_Q_INDEX = 2

def gcd3(a, b, c):
    return math.gcd(a, math.gcd(b, c))

def divides(a, b):
    if a == 0:
        return b == 0
    return b % a == 0

def conditions(witness):
    # 1. Try integer witness: (n, k, i, j) for Z/nZ or (k, i, j) for Z
    try:
        if isinstance(witness, tuple) and len(witness) in (3, 4):
            if all(isinstance(x, int) for x in witness):
                if len(witness) == 4:
                    n, k, i, j = witness
                    n = abs(n)
                else:
                    k, i, j = witness
                    n = 0
                
                k_gen = math.gcd(k, n) if n > 0 else abs(k)
                i_gen = math.gcd(i, n) if n > 0 else abs(i)
                j_gen = math.gcd(j, n) if n > 0 else abs(j)

                h1 = (k_gen != 1)
                h2 = divides(i_gen, k_gen) and divides(j_gen, k_gen)
                
                comax_R = (math.gcd(i_gen, j_gen) == 1)
                comax_RK = (gcd3(i_gen, j_gen, k_gen) == 1)
                q = (comax_R == comax_RK)
                
                return [bool(h1), bool(h2), not bool(q)]
    except Exception:
        pass

    # 2. Try sympy ideal witness
    try:
        if isinstance(witness, tuple) and len(witness) in (3, 4):
            if len(witness) == 3:
                K, I, J = witness
            else:
                R, K, I, J = witness
            
            ring = K.ring
            h1 = (K != ring.ideal(1))
            h2 = all(I.contains(g) for g in K.gens) and all(J.contains(g) for g in K.gens)
            
            comax_R = ((I + J) == ring.ideal(1))
            comax_RK = ((I + J + K) == ring.ideal(1))
            q = (comax_R == comax_RK)
            
            return [bool(h1), bool(h2), not bool(q)]
    except Exception:
        pass

    # 3. Try dictionary witness
    try:
        if isinstance(witness, dict):
            K = witness['K']
            I = witness['I']
            J = witness['J']
            R = witness['R']
            
            h1 = (K != R)
            
            if hasattr(K, 'issubset'):
                h2 = K.issubset(I) and K.issubset(J)
            else:
                h2 = (K <= I) and (K <= J)
                
            comax_R = ((I + J) == R)
            comax_RK = ((I + J + K) == R)
            q = (comax_R == comax_RK)
            
            return [bool(h1), bool(h2), not bool(q)]
    except Exception:
        pass

    # 4. Try object witness
    try:
        K = witness.K
        I = witness.I
        J = witness.J
        R = witness.R
        
        h1 = (K != R)
        
        if hasattr(K, 'issubset'):
            h2 = K.issubset(I) and K.issubset(J)
        else:
            h2 = (K <= I) and (K <= J)
            
        comax_R = ((I + J) == R)
        comax_RK = ((I + J + K) == R)
        q = (comax_R == comax_RK)
        
        return [bool(h1), bool(h2), not bool(q)]
    except Exception:
        pass

    return [False, False, False]