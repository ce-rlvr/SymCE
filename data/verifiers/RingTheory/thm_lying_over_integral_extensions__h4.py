import sympy
from sympy import isprime

# Top-level setup: named object bindings
Z = "Z"
Q = "Q"
Z_i = "Z[i]"
Z_x = "Z[x]"
Q_x = "Q[x]"

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (R, S, P_gen) where:
      - R and S are rings (e.g., Z, Q, Z_i)
      - P_gen is the generator of the ideal P in R
    """
    try:
        R_raw, S_raw, P_gen = witness
    except Exception:
        return [False, False, False, False]
        
    def get_ring_name(ring):
        if ring == "Z" or ring == sympy.ZZ: return "Z"
        if ring == "Q" or ring == sympy.QQ: return "Q"
        if isinstance(ring, str): return ring
        return str(ring)
        
    R = get_ring_name(R_raw)
    S = get_ring_name(S_raw)
    
    # H_1: R and S are commutative rings with identity
    valid_rings = ["Z", "Q", "Z[i]", "Z[x]", "Q[x]"]
    try:
        h1 = (R in valid_rings) and (S in valid_rings)
    except Exception:
        h1 = False
        
    # H_2: R is a subring of S
    subrings = {
        "Z": ["Z", "Q", "Z[i]", "Z[x]", "Q[x]"],
        "Q": ["Q", "Q[x]"],
        "Z[i]": ["Z[i]"],
        "Z[x]": ["Z[x]", "Q[x]"],
        "Q[x]": ["Q[x]"]
    }
    try:
        h2 = S in subrings.get(R, [])
    except Exception:
        h2 = False
        
    # H_3: S is an integral extension of R
    integral_exts = {
        "Z": ["Z", "Z[i]"],
        "Q": ["Q"],
        "Z[i]": ["Z[i]"],
        "Z[x]": ["Z[x]"],
        "Q[x]": ["Q[x]"]
    }
    try:
        h3 = S in integral_exts.get(R, [])
    except Exception:
        h3 = False
        
    # ¬Q: There does not exist a prime ideal Q of S such that Q ∩ R = P
    def exists_Q_ideal(R, S, P_gen):
        try:
            if R == "Z":
                if isinstance(P_gen, str):
                    return False
                p = int(P_gen)
                if p != P_gen: 
                    return False
                if S in ["Z", "Z[i]", "Z[x]"]:
                    return p == 0 or isprime(abs(p))
                elif S in ["Q", "Q[x]"]:
                    return p == 0
            elif R == "Q":
                if P_gen == 0:
                    return True
                return False
            elif R == "Z[i]":
                if P_gen == 0:
                    return True
                return False
        except Exception:
            return False
        return False

    try:
        q_exists = exists_Q_ideal(R, S, P_gen)
        neg_q = not q_exists
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings with identity",
    "H_2: R is a subring of S",
    "H_3: S is an integral extension of R",
    "¬Q: There does not exist a prime ideal Q of S such that Q ∩ R = P"
]

N_HYP = 3
NEG_Q_INDEX = 3