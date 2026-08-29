import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    h1, h2, neg_q = False, False, False
    try:
        R, I, J = witness
    except Exception:
        return [h1, h2, neg_q]
        
    is_sympy_ring = hasattr(R, 'ideal')
    
    if is_sympy_ring:
        try:
            h1 = bool(getattr(R, 'is_commutative', True))
        except Exception:
            h1 = False
            
        try:
            h2 = hasattr(J, 'is_ideal') or (hasattr(J, 'ring') and J.ring == R)
        except Exception:
            h2 = False
            
        try:
            zero_ideal = R.ideal(0)
            
            if hasattr(I, 'is_ideal'):
                I_ideal = I
            else:
                try:
                    I_ideal = R.ideal(*I)
                except TypeError:
                    I_ideal = R.ideal(I)
                
            if hasattr(J, 'is_ideal'):
                J_ideal = J
            else:
                try:
                    J_ideal = R.ideal(*J)
                except TypeError:
                    J_ideal = R.ideal(J)
                
            Ann_I = zero_ideal.quotient(I_ideal)
            Ann_I_colon_J = Ann_I.quotient(J_ideal)
            
            IJ = I_ideal * J_ideal
            Ann_IJ = zero_ideal.quotient(IJ)
            
            neg_q = bool(Ann_IJ != Ann_I_colon_J)
        except Exception:
            neg_q = False
    else:
        try:
            elements = list(R.elements)
            
            try:
                I_list = list(I)
            except TypeError:
                I_list = [I]
                
            try:
                J_list = list(J)
            except TypeError:
                J_list = [J]
            
            zero = getattr(R, 'zero', None)
            if zero is None:
                for e in elements:
                    if all(R.add(e, a) == a for a in elements):
                        zero = e
                        break
            
            h1_ok = True
            for a in elements:
                for b in elements:
                    if R.mul(a, b) != R.mul(b, a):
                        h1_ok = False
                        break
                if not h1_ok: break
            if h1_ok:
                for a in elements:
                    for b in elements:
                        for c in elements:
                            if R.mul(R.mul(a, b), c) != R.mul(a, R.mul(b, c)):
                                h1_ok = False
                                break
                        if not h1_ok: break
            h1 = h1_ok
            
            h2_ok = True
            if zero not in J_list:
                h2_ok = False
            else:
                for a in J_list:
                    for b in J_list:
                        if R.add(a, b) not in J_list:
                            h2_ok = False
                            break
                    if not h2_ok: break
                if h2_ok:
                    for r in elements:
                        for j in J_list:
                            if R.mul(r, j) not in J_list:
                                h2_ok = False
                                break
                        if not h2_ok: break
            h2 = h2_ok
            
            Ann_I_colon_J = []
            for r in elements:
                ok = True
                for j in J_list:
                    rj = R.mul(r, j)
                    if any(R.mul(rj, i) != zero for i in I_list):
                        ok = False
                        break
                if ok:
                    Ann_I_colon_J.append(r)
                    
            ij_prods = []
            for i in I_list:
                for j in J_list:
                    ij_prods.append(R.mul(i, j))
                    
            Ann_IJ = []
            for r in elements:
                if all(R.mul(r, x) == zero for x in ij_prods):
                    Ann_IJ.append(r)
                    
            neg_q = False
            for x in Ann_IJ:
                if x not in Ann_I_colon_J:
                    neg_q = True
                    break
            if not neg_q:
                for x in Ann_I_colon_J:
                    if x not in Ann_IJ:
                        neg_q = True
                        break
        except Exception:
            pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: J is an ideal of R",
    "¬Q: Ann_R(IJ) != (Ann_R(I) : J)"
]

N_HYP = 2
NEG_Q_INDEX = 2