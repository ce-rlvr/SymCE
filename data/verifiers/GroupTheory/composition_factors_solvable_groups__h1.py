import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.ntheory import isprime
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    try:
        # Determine if the witness is solvable and if its composition factors are prime
        if witness == sympy.S.Integers:
            solv = True
            factors_prime = False
        elif witness.__class__.__name__ == 'FreeGroup':
            solv = witness.rank <= 1
            factors_prime = False
        elif witness.__class__.__name__ == 'FpGroup':
            if len(witness.relators) == 0:
                solv = len(witness.generators) <= 1
            else:
                solv = False
            factors_prime = False
        elif hasattr(witness, 'is_solvable'):
            solv = bool(witness.is_solvable)
            if hasattr(witness, 'composition_series'):
                try:
                    series = witness.composition_series()
                    factors_prime = True
                    for i in range(len(series) - 1):
                        o1 = series[i].order()
                        o2 = series[i+1].order()
                        if o1 == o2:
                            continue
                        if not isprime(o1 // o2):
                            factors_prime = False
                            break
                except Exception:
                    factors_prime = False
            else:
                factors_prime = False
        else:
            return [False]

        # The conjecture states: G is solvable iff every composition factor is cyclic of prime order.
        # We evaluate if this equivalence holds.
        conclusion = (solv == factors_prime)
        
        # The negated conclusion is True if the equivalence fails
        neg_q = not conclusion
        
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The equivalence between solvability and having only prime order cyclic composition factors fails"
]
N_HYP = 0
NEG_Q_INDEX = 0