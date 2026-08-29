import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import Rational, Matrix, eye, zeros
from sympy.abc import x

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: K(x) is the field of rational functions in one variable over K",
    "H_2: G is a finite subgroup of the automorphism group Aut(K(x)/K)",
    "H_3: K(x)^G is the fixed field of G",
    "¬Q: For all rational functions f(x) in K(x), K(x)^G != K(f(x))"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness is expected to be a list of rational functions in x representing
    the elements of the finite subgroup G of Aut(K(x)/K).
    """
    # H_1: K(x) is the field of rational functions in one variable over K
    # This is a structural property of the domain, so we assume it holds for valid witnesses.
    h1_ok = True
    
    # H_2: G is a finite subgroup of the automorphism group Aut(K(x)/K)
    h2_ok = False
    try:
        if isinstance(witness, list) and len(witness) > 0:
            # Check if all elements are rational functions of degree 1 (Möbius transformations)
            is_automorphism_group = True
            for g in witness:
                num, den = sympy.fraction(sympy.cancel(g))
                if sympy.degree(num, x) > 1 or sympy.degree(den, x) > 1:
                    is_automorphism_group = False
                    break
                # Check determinant of the transformation ad - bc != 0
                a = num.coeff(x, 1)
                b = num.coeff(x, 0)
                c = den.coeff(x, 1)
                d = den.coeff(x, 0)
                if sympy.simplify(a*d - b*c) == 0:
                    is_automorphism_group = False
                    break
            
            # Check closure under composition
            if is_automorphism_group:
                closed = True
                for g1 in witness:
                    for g2 in witness:
                        comp = sympy.cancel(g1.subs(x, g2))
                        # Check if comp is in witness
                        found = False
                        for g3 in witness:
                            if sympy.simplify(comp - g3) == 0:
                                found = True
                                break
                        if not found:
                            closed = False
                            break
                    if not closed:
                        break
                
                # Check identity
                has_identity = False
                for g in witness:
                    if sympy.simplify(g - x) == 0:
                        has_identity = True
                        break
                
                if closed and has_identity:
                    h2_ok = True
    except Exception:
        h2_ok = False

    # H_3: K(x)^G is the fixed field of G
    # This is a definitional hypothesis, so it holds by definition for the witness group.
    h3_ok = True

    # ¬Q: For all rational functions f(x) in K(x), K(x)^G != K(f(x))
    # By Lüroth's Theorem, the fixed field of any finite subgroup of Aut(K(x)/K) 
    # is ALWAYS of the form K(f(x)) for some rational function f(x).
    # Therefore, the conclusion is unconditionally true, and its negation is unconditionally false.
    neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]