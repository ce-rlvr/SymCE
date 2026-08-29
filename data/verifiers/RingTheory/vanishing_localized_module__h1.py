import sympy
from sympy import symbols, Rational, Integer
from sympy.matrices import eye, zeros
import itertools
import functools
import math

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        M_list = list(witness.M)
        R_list = list(witness.R)
        S_list = list(witness.S)
    except Exception:
        return [False, False, False]
        
    try:
        h1 = True
        if witness.zero_M not in M_list:
            h1 = False
            
        for x in M_list:
            for y in M_list:
                if witness.add_M(x, y) not in M_list: h1 = False
        for r in R_list:
            for x in M_list:
                if witness.act_M(r, x) not in M_list: h1 = False
                
        for x in M_list:
            if witness.add_M(x, witness.zero_M) != x: h1 = False
            inv_exists = False
            for y in M_list:
                if witness.add_M(x, y) == witness.zero_M:
                    inv_exists = True
                    break
            if not inv_exists: h1 = False
            for y in M_list:
                if witness.add_M(x, y) != witness.add_M(y, x): h1 = False
                for z in M_list:
                    if witness.add_M(witness.add_M(x, y), z) != witness.add_M(x, witness.add_M(y, z)): h1 = False
        
        for r in R_list:
            for x in M_list:
                for y in M_list:
                    if witness.act_M(r, witness.add_M(x, y)) != witness.add_M(witness.act_M(r, x), witness.act_M(r, y)): h1 = False
            for s in R_list:
                for x in M_list:
                    if witness.act_M(witness.add_R(r, s), x) != witness.add_M(witness.act_M(r, x), witness.act_M(s, x)): h1 = False
                    if witness.act_M(witness.mul_R(r, s), x) != witness.act_M(r, witness.act_M(s, x)): h1 = False
                    
        if hasattr(witness, 'one_R'):
            for x in M_list:
                if witness.act_M(witness.one_R, x) != x: h1 = False
    except Exception:
        h1 = False

    try:
        h2 = True
        for a in S_list:
            if a not in R_list: h2 = False
            for b in S_list:
                if witness.mul_R(a, b) not in S_list: h2 = False
    except Exception:
        h2 = False

    try:
        if not S_list:
            lhs = all(m == witness.zero_M for m in M_list)
        else:
            lhs = True
            for m in M_list:
                for t in S_list:
                    tm = witness.act_M(t, m)
                    if not any(witness.act_M(u, tm) == witness.zero_M for u in S_list):
                        lhs = False
                        break
                if not lhs:
                    break
        
        rhs = True
        for m in M_list:
            if not any(witness.act_M(s, m) == witness.zero_M for s in S_list):
                rhs = False
                break
        
        neg_q = (lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: M is an R-module",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: S^{-1}M = 0 is not equivalent to (for every m in M, exists s in S such that sm = 0)"
]

N_HYP = 2
NEG_Q_INDEX = 2