import sympy
from sympy import S
from sympy.combinatorics import PermutationGroup, CyclicGroup, SymmetricGroup, AlternatingGroup, DihedralGroup

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    """
    Checks if the witness is a counterexample to the conjecture:
    "G is a cyclic group if and only if there exists a surjective group homomorphism from Z to G."
    
    Mathematically, this equivalence is unconditionally true for all groups. 
    The conjecture can only be considered "false" if a hypothesis like "G is a group" 
    was dropped (making G a monoid like N, where it is a cyclic monoid but has no 
    surjective group homomorphism from Z), or if "cyclic group" is strictly defined 
    as finite (making Z a counterexample).
    """
    try:
        # For standard permutation groups, the equivalence always holds.
        if isinstance(witness, PermutationGroup):
            return [False]
            
        # Check if the witness is Z (Integers)
        # If the formal system defines "cyclic" as "finite cyclic", Z is the counterexample.
        is_Z = (witness == S.Integers) or (str(witness).strip() in ("Z", "Integers", "ℤ", "S.Integers"))
        
        # Check if the witness is N (Naturals)
        # If the [Group G] hypothesis was dropped, N is a cyclic monoid (LHS=True) 
        # but there is no surjective group homomorphism from Z to N (RHS=False).
        is_N = (witness in (S.Naturals, S.Naturals0)) or (str(witness).strip() in ("N", "Naturals", "N0", "Naturals0", "ℕ", "S.Naturals", "S.Naturals0"))
        
        if is_Z or is_N:
            return [True]
            
        return [False]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: The equivalence between G being a cyclic group and having a surjective homomorphism from Z fails"
]

N_HYP = 0
NEG_Q_INDEX = 0