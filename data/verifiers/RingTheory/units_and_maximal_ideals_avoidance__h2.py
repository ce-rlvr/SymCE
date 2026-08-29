import sympy
import sympy.combinatorics as comb
import sympy.matrices as mat
import math

# Top-level setup
S3 = comb.SymmetricGroup(3)
S4 = comb.SymmetricGroup(4)
A4 = comb.AlternatingGroup(4)
D4 = comb.DihedralGroup(4)
C4 = comb.CyclicGroup(4)
V4 = comb.AlternatingGroup(4)
Z2 = comb.CyclicGroup(2)
Z3 = comb.CyclicGroup(3)
Z4 = comb.CyclicGroup(4)
Z6 = comb.CyclicGroup(6)
trivial = comb.CyclicGroup(1)

I2 = mat.eye(2)
I3 = mat.eye(3)
O2 = mat.zeros(2, 2)
O3 = mat.zeros(3, 3)

def conditions(witness):
    """
    Given a witness object, checks whether it is a valid counterexample.
    The witness is expected to provide a ring R and an element u.
    """
    try:
        if hasattr(witness, 'R') and hasattr(witness, 'u'):
            R, u = witness.R, witness.u
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, u = witness
        elif isinstance(witness, dict) and 'R' in witness and 'u' in witness:
            R, u = witness['R'], witness['u']
        else:
            R, u = witness, None
    except Exception:
        return [False, False]

    # H_1: R is a commutative ring with identity
    h1 = False
    try:
        if hasattr(R, 'is_commutative_ring_with_identity'):
            h1 = bool(R.is_commutative_ring_with_identity())
        elif hasattr(R, 'is_commutative') and hasattr(R, 'is_Ring'):
            if R.is_commutative and R.is_Ring:
                if hasattr(R, 'one') and R.one is not None:
                    h1 = True
                elif R in (sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
                    h1 = True
        elif isinstance(R, int) and R >= 1:
            # Representing Z/nZ
            h1 = True
    except Exception:
        h1 = False

    # ¬Q: u is a unit in R is NOT equivalent to u not being in any maximal ideal of R
    # The theorem holds for all u IN R. It fails when u is NOT in R.
    neg_q = False
    try:
        if hasattr(R, 'maximal_ideals'):
            try:
                in_R = (u in R)
            except Exception:
                in_R = True
                
            if not in_R:
                is_unit = False
                in_any_M = False
            else:
                try:
                    is_unit = bool(R.is_unit(u))
                except Exception:
                    is_unit = False
                try:
                    in_any_M = any(u in M for M in R.maximal_ideals())
                except Exception:
                    in_any_M = False
                    
            not_in_any_M = not in_any_M
            q = (is_unit == not_in_any_M)
            neg_q = not q

        elif isinstance(R, int) and R >= 1:
            n = R
            # Elements of Z/nZ are 0, 1, ..., n-1
            if isinstance(u, int) and 0 <= u < n:
                is_unit = (math.gcd(u, n) == 1)
                if n == 1:
                    in_any_M = False
                else:
                    prime_factors = sympy.primefactors(n)
                    in_any_M = any(u % p == 0 for p in prime_factors)
                not_in_any_M = not in_any_M
            else:
                is_unit = False
                not_in_any_M = True
            q = (is_unit == not_in_any_M)
            neg_q = not q

        elif R in (sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
            try:
                in_R = (u in R)
            except Exception:
                in_R = False
                
            if in_R:
                is_unit = bool(R.is_unit(u))
                if R == sympy.S.Integers:
                    in_any_M = (abs(u) != 1)
                else:
                    in_any_M = (u == 0)
                not_in_any_M = not in_any_M
            else:
                is_unit = False
                not_in_any_M = True
            q = (is_unit == not_in_any_M)
            neg_q = not q
            
        elif hasattr(R, 'is_commutative') and R.is_commutative:
            try:
                in_R = (u in R)
            except Exception:
                in_R = False
                
            if in_R:
                is_unit = bool(R.is_unit(u))
                if hasattr(R, 'is_Field') and R.is_Field:
                    in_any_M = (u == R.zero)
                else:
                    raise NotImplementedError
                not_in_any_M = not in_any_M
            else:
                is_unit = False
                not_in_any_M = True
            q = (is_unit == not_in_any_M)
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "¬Q: u is a unit in R is not equivalent to u not being in any maximal ideal of R"
]

N_HYP = 1
NEG_Q_INDEX = 1