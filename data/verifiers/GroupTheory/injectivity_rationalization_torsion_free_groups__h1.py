import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Standard group theory objects
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

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_group(witness):
    if hasattr(witness, 'is_group'):
        val = witness.is_group
        return bool(val() if callable(val) else val)
    if type(witness).__name__ in ['FreeGroup', 'FpGroup', 'PermutationGroup']:
        return True
    if hasattr(witness, 'generators'):
        return True
    return False

def check_torsion_free(witness):
    if hasattr(witness, 'is_torsion_free'):
        val = witness.is_torsion_free
        return bool(val() if callable(val) else val)
    
    if type(witness).__name__ == 'FreeGroup':
        return True
        
    if hasattr(witness, 'order'):
        val = witness.order
        order = val() if callable(val) else val
        if order != sympy.oo and order != float('inf'):
            return order == 1
            
    if hasattr(witness, 'elements'):
        try:
            return len(list(witness.elements)) == 1
        except Exception:
            pass
            
    raise AttributeError("Cannot determine if torsion-free")

def check_abelian(witness):
    if hasattr(witness, 'is_abelian'):
        val = witness.is_abelian
        return bool(val() if callable(val) else val)
        
    if type(witness).__name__ == 'FreeGroup':
        return len(witness.generators) <= 1
        
    if hasattr(witness, 'generators'):
        gens = list(witness.generators)
        for i in range(len(gens)):
            for j in range(i+1, len(gens)):
                if gens[i]*gens[j] != gens[j]*gens[i]:
                    return False
        return True
        
    raise AttributeError("Cannot determine if abelian")

def conditions(witness) -> list[bool]:
    """
    Check if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    try:
        h1 = is_group(witness)
    except Exception:
        h1 = False

    try:
        tf = check_torsion_free(witness)
        ab = check_abelian(witness)
        
        # The kernel of phi: G -> G \otimes Q is the preimage of the torsion subgroup of G/[G,G].
        # Thus, phi is injective iff G is abelian AND torsion-free.
        phi_injective = tf and ab
        
        # The conjecture states: phi is injective iff G is torsion-free.
        conclusion = (phi_injective == tf)
        
        # The negated conclusion is True when the conjecture fails.
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: phi is the natural group homomorphism to the rationalization",
    "¬Q: phi is injective iff G is torsion-free is FALSE"
]

N_HYP = 1
NEG_Q_INDEX = 1