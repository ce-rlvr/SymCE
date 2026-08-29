import math
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (m, n, k) representing the external 
    semidirect product Z_m ⋊_φ Z_n, where φ(1) is the automorphism of Z_m 
    given by multiplication by k.
    """
    try:
        # Extract parameters from the witness
        if isinstance(witness, dict):
            m = witness.get('m')
            n = witness.get('n')
            k = witness.get('k')
            if k is None:
                k = witness.get('phi')
        else:
            m, n, k = witness
            
        # Handle cases where m or n might be passed as sympy CyclicGroup objects
        if not isinstance(m, int):
            try:
                m = int(m.order())
            except Exception:
                pass
        if not isinstance(n, int):
            try:
                n = int(n.order())
            except Exception:
                pass
                
        # Handle cases where phi is passed as a function
        if callable(k):
            k = k(1)
            
        # H_1: G is an external semidirect product of finite cyclic groups Z_m and Z_n.
        # This requires m, n to be positive integers, and k to define a valid homomorphism 
        # from Z_n to Aut(Z_m). Thus, gcd(k, m) == 1 and k^n ≡ 1 (mod m).
        h1 = (isinstance(m, int) and isinstance(n, int) and isinstance(k, int) and 
              m > 0 and n > 0 and math.gcd(k, m) == 1 and pow(k, n, m) == 1 % m)
              
        neg_q = False
        if h1:
            # The conclusion claims "The isomorphism class of G is uniquely determined by phi".
            # In the context of the false conjecture, this is a mangled statement meaning 
            # "phi is uniquely determined by the isomorphism class of G".
            # The second part of the conclusion ("G is abelian iff phi is trivial") is unconditionally true.
            # Therefore, the conclusion fails (neg_q is True) if there exists another valid 
            # homomorphism φ' that yields an isomorphic group but is not equal to φ.
            # Two such semidirect products are isomorphic iff k' ≡ k^r (mod m) for some r coprime to n.
            for r in range(1, n):
                if math.gcd(r, n) == 1:
                    if pow(k, r, m) != k % m:
                        neg_q = True
                        break
                        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: G is an external semidirect product of finite cyclic groups",
    "¬Q: The isomorphism class does not uniquely determine phi"
]

N_HYP = 1
NEG_Q_INDEX = 1