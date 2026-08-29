import sympy
from sympy import Matrix, eye, zeros, Symbol
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness (e.g., a matrix representing a bilinear form B),
    checks the hypotheses and the negated conclusion.
    """
    try:
        # Extract the bilinear form B from the witness
        if isinstance(witness, tuple):
            B = witness[0]
        else:
            B = witness
            
        # Validate that B can represent a bilinear form
        if not isinstance(B, (Matrix, Symbol)):
            return [False, False, False]
            
        if isinstance(B, Matrix) and B.shape[0] != B.shape[1]:
            return [False, False, False]
            
        # H_1: B is a bilinear form on V
        # A square matrix or a generic symbol validly represents a bilinear form.
        h1_ok = True
        
        # H_2: O(V, B) is the set of all bijective linear transformations T: V \to V 
        # such that B(T(u), T(v)) = B(u, v) for all u, v \in V
        # This is a definitional hypothesis, so it holds by definition for the space.
        h2_ok = True
        
        # ¬Q: The set O(V, B) does NOT form a group under function composition.
        # Mathematically, the set of all *bijective* functions from a set to itself 
        # that preserve a given structure (like a bilinear form) ALWAYS forms a group 
        # (the automorphism group of that structure). 
        # 1. Closure: Composition of bijective structure-preserving maps is bijective and structure-preserving.
        # 2. Identity: The identity map is bijective and structure-preserving.
        # 3. Inverses: The inverse of a bijective structure-preserving map is also structure-preserving.
        # 4. Associativity: Function composition is always associative.
        # Because the hypothesis explicitly restricts O(V, B) to "bijective" linear transformations,
        # O(V, B) is guaranteed to be a group. Thus, the conclusion is always true, and its negation is false.
        neg_q_ok = False
        
        return [h1_ok, h2_ok, neg_q_ok]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    r"H_1: B is a bilinear form on V",
    r"H_2: O(V, B) is the set of all bijective linear transformations T: V \to V such that B(T(u), T(v)) = B(u, v) for all u, v \in V",
    r"¬Q: The set O(V, B) does not form a group under function composition"
]

N_HYP = 2
NEG_Q_INDEX = 2