import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, CyclicGroup
from sympy.matrices import eye
from sympy.ntheory import isprime, primefactors

# Top-level setup
S3 = SymmetricGroup(3)
Z2 = CyclicGroup(2)
I2 = eye(2)

def conditions(witness) -> list[bool]:
    """
    witness is expected to be a dictionary representing a ring and its maximal ideals.
    Supported types:
      - {"type": "Z_(p)", "p": <prime_int>, "M_list": [<prime_int>]}
        Represents the localization of Z at the prime ideal (p).
      - {"type": "Z_n", "n": <int>, "M_list": [<prime_factors>]}
        Represents Z/nZ.
      - {"type": "Q[x]_(x)", "M_list": ["x"]}
        Represents the localization of Q[x] at (x).
    """
    h1 = False
    neg_q = False
    
    try:
        # Allow tuple format as a fallback
        if isinstance(witness, tuple) and len(witness) == 3:
            ring_type, param, M_list = witness
            if ring_type == "Z_(p)":
                witness = {"type": "Z_(p)", "p": param, "M_list": M_list}
            elif ring_type == "Z_n":
                witness = {"type": "Z_n", "n": param, "M_list": M_list}
                
        if not isinstance(witness, dict):
            return [False, False]
            
        ring_type = witness.get("type")
        M_list = witness.get("M_list", [])
        
        if ring_type == "Z_(p)":
            p = witness.get("p")
            if isinstance(p, (int, sympy.Integer)) and isprime(p):
                if isinstance(M_list, list) and len(M_list) == 1 and M_list[0] == p:
                    h1 = True
                    # In Z_(p), the zero ideal (0) is prime, hence primary.
                    # Its radical is (0).
                    # The only maximal ideal is M = (p).
                    # Since radical((0)) = (0) != M, (0) is not M-primary.
                    # Therefore, (0) does not have a primary decomposition into M_i-primary ideals.
                    neg_q = True
                    
        elif ring_type == "Z_n":
            n = witness.get("n")
            if isinstance(n, (int, sympy.Integer)) and n > 1:
                factors = primefactors(n)
                if isinstance(M_list, list) and sorted(M_list) == sorted(factors):
                    h1 = True
                    # Z_n is an Artinian ring. The zero ideal has a primary decomposition.
                    neg_q = False
                    
        elif ring_type == "Q[x]_(x)":
            if isinstance(M_list, list) and len(M_list) == 1 and M_list[0] == "x":
                h1 = True
                # Similar to Z_(p), the zero ideal is not (x)-primary.
                neg_q = True
                
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: M_1, ..., M_k are all the distinct maximal ideals of R",
    "¬Q: The zero ideal (0) does NOT have a minimal primary decomposition (0) = Q_1 \\cap \\dots \\cap Q_k, where each Q_i is an M_i-primary ideal."
]

N_HYP = 1
NEG_Q_INDEX = 1