import sympy
import math
import itertools
import functools

# Top-level setup
# We support the ring of integers Z for this counterexample.
Z = 'Z'

def conditions(witness) -> list[bool]:
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    Expected witness format:
      A dictionary {'ring': 'Z', 'Q': q_gen, 'P': p_gen, 'S': [s1, s2, ...]}
      or a tuple (q_gen, p_gen, S) assuming ring 'Z'.
    """
    try:
        if isinstance(witness, dict):
            ring = witness.get('ring', 'Z')
            q = witness.get('Q')
            p = witness.get('P')
            S = witness.get('S')
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                ring = 'Z'
                q, p, S = witness
            elif len(witness) == 4:
                ring, q, p, S = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
            
        if ring != 'Z':
            # For simplicity and fast verification, we restrict to the ring of integers
            return [False, False, False, False]
            
        try:
            S = list(S)
        except Exception:
            return [False, False, False, False]
            
        # H_1: R is a commutative ring with identity
        # The ring of integers Z is a commutative ring with identity.
        h1 = True
        
        try:
            q_val = abs(int(q))
            p_val = abs(int(p))
        except Exception:
            return [h1, False, False, False]
            
        # H_2: Q is a P-primary ideal in R
        h2 = False
        try:
            if q_val == 0 and p_val == 0:
                # (0) is a (0)-primary ideal in Z
                h2 = True
            elif q_val > 1 and sympy.isprime(p_val):
                # In Z, (q) is (p)-primary iff q = p^k for some k >= 1
                temp = q_val
                while temp % p_val == 0:
                    temp //= p_val
                if temp == 1:
                    h2 = True
        except Exception:
            h2 = False
            
        # H_3: S \cap P \neq \emptyset
        h3 = False
        try:
            for s in S:
                try:
                    s_val = int(s)
                except Exception:
                    continue
                
                if p_val == 0:
                    if s_val == 0:
                        h3 = True
                        break
                else:
                    if s_val % p_val == 0:
                        h3 = True
                        break
        except Exception:
            h3 = False
            
        # ¬Q: S \cap Q == \emptyset
        neg_q = True
        try:
            for s in S:
                try:
                    s_val = int(s)
                except Exception:
                    continue
                
                if q_val == 0:
                    if s_val == 0:
                        neg_q = False
                        break
                else:
                    if s_val % q_val == 0:
                        neg_q = False
                        break
        except Exception:
            neg_q = False
            
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: Q is a P-primary ideal in R",
    "H_3: S intersection P is non-empty",
    "¬Q: S intersection Q is empty"
]

N_HYP = 3
NEG_Q_INDEX = 3