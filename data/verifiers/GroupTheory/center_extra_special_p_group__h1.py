import sympy
import sympy.ntheory
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    
    The conjecture states that if G is an extra-special p-group, its center Z(G) is cyclic of order p.
    In the context of the dropped hypothesis, "extra-special" was likely relaxed to "special" 
    (i.e., G' = Z(G) = Phi(G)), allowing for counterexamples where |Z(G)| > p (e.g., central/direct products).
    """
    try:
        # Check if witness is a valid group object
        if not hasattr(witness, 'generate'):
            return [False, False]
        if not hasattr(witness, 'center'):
            return [False, False]
        if not hasattr(witness, 'derived_subgroup'):
            return [False, False]
            
        order = witness.order()
        if order == 1 or order == sympy.oo:
            return [False, False]
            
        # Check if G is a p-group
        factors = sympy.ntheory.factorint(order)
        if len(factors) != 1:
            return [False, False]
            
        p = list(factors.keys())[0]
        
        Z = witness.center()
        D = witness.derived_subgroup()
        
        Z_elems = set(Z.generate())
        D_elems = set(D.generate())
        
        h1 = False
        # Check if G' == Z(G)
        if Z_elems == D_elems:
            # Check if G/Z(G) is elementary abelian (i.e., g^p in Z(G) for all g in G)
            is_elem_abelian = True
            for g in witness.generate():
                if (g**p) not in Z_elems:
                    is_elem_abelian = False
                    break
            if is_elem_abelian:
                h1 = True
                
        # Conclusion: Z(G) is a cyclic group of order p.
        # Negation: Z(G) is NOT a cyclic group of order p.
        # Since Z(G) is a subgroup of a p-group, its order is a power of p.
        # It is cyclic of order p if and only if its order is exactly p.
        neg_q = (Z.order() != p)
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: G is an extra-special p-group",
    "¬Q: The center Z(G) is not a cyclic group of order p"
]

N_HYP = 1
NEG_Q_INDEX = 1