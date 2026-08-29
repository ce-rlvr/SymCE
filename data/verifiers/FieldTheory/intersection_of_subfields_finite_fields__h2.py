import math
import sympy
from sympy.ntheory import factorint
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for standard algebra objects
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

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and fails the conclusion.
    The witness is expected to be a tuple: (q, m, n)
    """
    try:
        q, m, n = witness
    except Exception:
        return [False, False, False]
        
    # H1: F_q is a finite field with q elements
    try:
        q_sym = sympy.sympify(q)
        if not q_sym.is_integer or q_sym < 2:
            h1 = False
        else:
            factors_q = factorint(int(q_sym))
            h1 = (len(factors_q) == 1)
    except Exception:
        h1 = False
        
    # H2: F_{q^m} and F_{q^n} are subfields of a common algebraic closure of F_q
    try:
        if not h1:
            h2 = False
        else:
            p = list(factorint(int(q_sym)).keys())[0]
            m_sym = sympy.sympify(m)
            n_sym = sympy.sympify(n)
            qm = q_sym ** m_sym
            qn = q_sym ** n_sym
            
            # For F_{q^m} and F_{q^n} to be valid finite fields in the same algebraic closure,
            # their sizes must be integers and powers of the same characteristic p.
            if not qm.is_integer or not qn.is_integer or qm < 2 or qn < 2:
                h2 = False
            else:
                qm_int = int(qm)
                qn_int = int(qn)
                factors_qm = factorint(qm_int)
                factors_qn = factorint(qn_int)
                h2 = (len(factors_qm) == 1 and list(factors_qm.keys())[0] == p and
                      len(factors_qn) == 1 and list(factors_qn.keys())[0] == p)
    except Exception:
        h2 = False
        
    # Conclusion: The intersection F_{q^m} \cap F_{q^n} is exactly the field F_{q^{\gcd(m,n)}}
    try:
        if not h2:
            q_holds = False
        else:
            p = list(factorint(int(q_sym)).keys())[0]
            m_sym = sympy.sympify(m)
            n_sym = sympy.sympify(n)
            qm_int = int(q_sym ** m_sym)
            qn_int = int(q_sym ** n_sym)
            
            # True intersection size: F_{p^A} \cap F_{p^B} = F_{p^{\gcd(A,B)}}
            A = int(sympy.log(qm_int, p))
            B = int(sympy.log(qn_int, p))
            true_intersect_size = p ** math.gcd(A, B)
            
            # The formula F_{q^{\gcd(m,n)}} is only well-defined in standard terms if m and n are integers.
            # If they are not integers (e.g., rational numbers), standard gcd is undefined, making the conclusion fail.
            if m_sym.is_integer and n_sym.is_integer:
                m_int = int(m_sym)
                n_int = int(n_sym)
                formula_size = int(q_sym) ** math.gcd(m_int, n_int)
                q_holds = (true_intersect_size == formula_size)
            else:
                q_holds = False
    except Exception:
        q_holds = False
        
    neg_q = not q_holds
    
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: F_{q^m} and F_{q^n} are subfields of a common algebraic closure of F_q",
    "¬Q: The intersection F_{q^m} \\cap F_{q^n} is not exactly the field F_{q^{\\gcd(m,n)}}"
]

N_HYP = 2
NEG_Q_INDEX = 2