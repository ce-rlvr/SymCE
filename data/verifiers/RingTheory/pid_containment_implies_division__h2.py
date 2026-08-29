import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x, y, z

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

# Standard ring/field objects
ZZ = sympy.S.Integers
QQ = sympy.S.Rationals

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "In a PID R, I \subseteq J if and only if J divides I (i.e., I = JK for some ideal K)"
    
    The dropped hypothesis is that I and J must be ideals. 
    A valid witness provides subsets I and J that are not ideals, causing the equivalence to fail.
    """
    # Parse witness
    if isinstance(witness, tuple):
        if len(witness) == 3:
            R, I, J = witness
        elif len(witness) == 2:
            R = ZZ
            I, J = witness
        else:
            return [False, False]
    else:
        return [False, False]

    # H_1: R is a principal ideal domain
    h1 = False
    try:
        if hasattr(R, 'is_PID') and R.is_PID:
            h1 = True
        elif R in [ZZ, QQ]:
            h1 = True
        elif str(R) in ['ZZ', 'QQ']:
            h1 = True
    except Exception:
        pass

    # neg_Q: The conclusion fails at the witness
    # Conclusion: I \subseteq J iff J divides I (I = JK for some ideal K)
    neg_q = False
    try:
        def to_set(obj):
            if isinstance(obj, (set, list, tuple)):
                return set(obj)
            if hasattr(obj, 'is_FiniteSet') and obj.is_FiniteSet:
                return set(obj)
            return None

        I_set = to_set(I)
        J_set = to_set(J)

        if I_set is not None and J_set is not None:
            # Check containment
            subset = I_set.issubset(J_set)
            
            # Check division: I = JK for some ideal K
            # In an infinite domain like ZZ, the only finite ideal is {0}.
            # The product of any subset J and an ideal K is always an ideal.
            # Therefore, if I is a finite set, I = JK is only possible if I is the zero ideal.
            # If I == {0}, then for K = {0}, JK = {0} = I, so J divides I is True.
            # If I != {0}, since I is finite, it cannot be an ideal (other than {0}),
            # but JK is always an ideal. So I != JK. Thus J divides I is False.
            zero_elem = 0
            if hasattr(R, 'zero'):
                zero_elem = R.zero
                
            is_zero_ideal = (I_set == {zero_elem} or I_set == {0})
            divides = is_zero_ideal
            
            conclusion = (subset == divides)
            neg_q = not conclusion
        else:
            # If they are not finite sets, they might be actual ideals.
            # For true ideals in a PID, the conclusion holds, so neg_q is False.
            neg_q = False
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "¬Q: I is a subset of J is not equivalent to J divides I"
]

N_HYP = 1
NEG_Q_INDEX = 1