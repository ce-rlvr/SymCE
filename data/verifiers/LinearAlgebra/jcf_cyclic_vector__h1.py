import sympy
from sympy import Matrix, eye, zeros, Rational
from sympy.abc import x
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
        # The witness must be a square matrix
        if not isinstance(witness, Matrix) or witness.rows != witness.cols:
            return [False]
            
        A = witness
        
        # LHS: Check if A has a cyclic vector.
        # A matrix has a cyclic vector iff its minimal polynomial equals its characteristic polynomial.
        try:
            charpoly = A.charpoly(x).as_expr()
            minpoly = sympy.minpoly(A, x)
            has_cyclic_vector = (sympy.simplify(charpoly - minpoly) == 0)
        except Exception:
            # Fallback: geometric multiplicity of every eigenvalue must be 1
            has_cyclic_vector = True
            for evalue, alg_mult, vecs in A.eigenvects():
                if len(vecs) > 1:
                    has_cyclic_vector = False
                    break
                    
        # RHS: The Jordan canonical form of A contains exactly one Jordan block for each distinct eigenvalue.
        # This implicitly requires that the Jordan canonical form EXISTS over the base field of the matrix.
        # We determine the base field from the entries and check if the characteristic polynomial splits.
        entries = list(A)
        if all(e.is_rational == True for e in entries):
            # Base field is Q
            evals = A.eigenvals().keys()
            splits = all(e.is_rational == True for e in evals)
        elif all(e.is_real == True for e in entries):
            # Base field is R
            evals = A.eigenvals().keys()
            splits = all(e.is_real == True for e in evals)
        else:
            # Base field is C (or algebraically closed), JCF always exists
            splits = True
            
        # If the JCF exists (splits == True), the condition "exactly one block per eigenvalue" 
        # is mathematically equivalent to having a cyclic vector.
        # If the JCF does not exist over the base field, the RHS statement is false.
        rhs = splits and has_cyclic_vector
        lhs = has_cyclic_vector
        
        # The conjecture states LHS <==> RHS
        conjecture_holds = (lhs == rhs)
        
        # We want neg_Q to be True when the conjecture FAILS
        neg_q = not conjecture_holds
        
        return [neg_q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: The matrix has a cyclic vector but its Jordan canonical form does not contain exactly one block per eigenvalue (e.g. JCF doesn't exist over the base field)"
]

N_HYP = 0
NEG_Q_INDEX = 0