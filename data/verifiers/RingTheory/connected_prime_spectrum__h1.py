import sympy
from sympy.ntheory import primefactors

# Top-level setup: no special named bindings needed for this domain,
# as rings can be represented by integers (Z/nZ) or sympy.ZZ / sympy.QQ.

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the conjecture:
    "Spec(R) is a connected topological space."
    
    Witnesses are represented as:
      - An integer n >= 0, representing the ring Z/nZ (n=0 represents Z).
      - sympy.ZZ or sympy.QQ.
      - A tuple/list of the above, representing a direct product of rings.
    """
    try:
        rings = []
        h1 = False
        
        if witness == sympy.ZZ or witness == sympy.QQ:
            h1 = True
            rings = [0]
        elif isinstance(witness, int) and witness >= 0:
            h1 = True
            rings = [witness]
        elif isinstance(witness, (tuple, list)):
            valid = True
            for x in witness:
                if x == sympy.ZZ or x == sympy.QQ:
                    rings.append(0)
                elif isinstance(x, int) and x >= 0:
                    rings.append(x)
                else:
                    valid = False
                    break
            if valid and len(witness) > 0:
                h1 = True
    except Exception:
        h1 = False
        rings = []

    try:
        if not h1:
            neg_q = False
        else:
            # Calculate the number of connected components of Spec(R).
            # For a finite product of rings, the spectrum is the disjoint union of their spectra.
            # For Z/nZ (n > 1), Spec(Z/nZ) has a discrete topology and its points correspond 
            # to the prime factors of n. Thus, it has len(primefactors(n)) components.
            # For Z (n = 0) or QQ, the spectrum is connected (1 component).
            # For the trivial ring (n = 1), the spectrum is empty (0 components).
            num_components = 0
            for n in rings:
                if n == 0:
                    num_components += 1
                elif n == 1:
                    num_components += 0
                else:
                    num_components += len(primefactors(n))
            
            # The space is disconnected if it has 2 or more connected components.
            neg_q = num_components >= 2
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Spec(R) is the set of all prime ideals of R equipped with the Zariski topology",
    "¬Q: Spec(R) is not a connected topological space"
]

N_HYP = 1
NEG_Q_INDEX = 1