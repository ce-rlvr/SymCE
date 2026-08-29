import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.matrices

# Top-level setup for standard algebra objects
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Evaluates the remaining hypotheses and the negated conclusion for the given witness.
    
    The conjecture is:
    Hypothesis: R is a commutative Noetherian ring
    Conclusion: I is a primary ideal if and only if Ass(R/I) consists of exactly one prime ideal
    """
    h1 = False
    neg_q = False
    
    # Evaluate Hypothesis 1: R is a commutative Noetherian ring
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_commutative_noetherian', True))
        else:
            h1 = bool(getattr(witness, 'is_commutative_noetherian', True))
    except Exception:
        h1 = False

    # Evaluate Negated Conclusion: 
    # It is NOT the case that (I is primary <==> Ass(R/I) has exactly one prime ideal)
    try:
        if isinstance(witness, dict):
            is_prim = bool(witness['is_primary'])
            if 'associated_primes' in witness:
                ass_len = len(witness['associated_primes'])
            else:
                ass_len = int(witness['ass_len'])
        else:
            is_prim = bool(witness.is_primary)
            if hasattr(witness, 'associated_primes'):
                ass_len = len(witness.associated_primes)
            else:
                ass_len = int(witness.ass_len)
                
        # The conclusion is (is_prim == (ass_len == 1))
        # We want the negation of the conclusion
        neg_q = not (is_prim == (ass_len == 1))
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "¬Q: It is not the case that I is a primary ideal if and only if Ass(R/I) consists of exactly one prime ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1