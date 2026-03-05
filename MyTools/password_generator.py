#!/usr/bin/env python3
import secrets as _k0,string as _k1,sys as _k2,builtins as _k3
_=lambda _b:getattr(_k1,_b)
_q0=_('digits');_q1=_('ascii_letters');_q2=_('punctuation')
_q3=_q0+_q1+_q2;_q4=0x4
_B=lambda _n:getattr(_k3,_n)
_m=lambda _s,_c:(lambda _r:_r if _r else(_ for _ in()).throw(
    _B(chr(84)+chr(121)+chr(112)+chr(101)+chr(69)+chr(114)+chr(114)+chr(111)+chr(114))(
    (chr(108)+chr(101)+chr(110)+chr(103)+chr(116)+chr(104)+chr(32)+chr(109)+chr(117)+chr(115)+chr(116)
    +chr(32)+chr(98)+chr(101)+chr(32)+chr(97)+chr(110)+chr(32)+chr(105)+chr(110)+chr(116)+chr(101)
    +chr(103)+chr(101)+chr(114)+chr(44)+chr(32)+chr(103)+chr(111)+chr(116)+chr(32))
    +type(_s).__name__)))(isinstance(_s,int))
_n=lambda _s,_c:(lambda _r:_r if _r else(_ for _ in()).throw(
    _B(chr(86)+chr(97)+chr(108)+chr(117)+chr(101)+chr(69)+chr(114)+chr(114)+chr(111)+chr(114))(
    (chr(80)+chr(97)+chr(115)+chr(115)+chr(119)+chr(111)+chr(114)+chr(100)+chr(32)+chr(108)+chr(101)
    +chr(110)+chr(103)+chr(116)+chr(104)+chr(32)+chr(109)+chr(117)+chr(115)+chr(116)+chr(32)+chr(98)
    +chr(101)+chr(32)+chr(97)+chr(116)+chr(32)+chr(108)+chr(101)+chr(97)+chr(115)+chr(116)+chr(32))
    +str(_q4)+(chr(44)+chr(32)+chr(103)+chr(111)+chr(116)+chr(32))+str(_s)))
    )(_s>=_q4)
def _x7(_p3,**_p4):
    _v0=_p4.get((chr(117)+chr(115)+chr(101)+chr(95)+chr(115)+chr(112)+chr(101)+chr(99)+chr(105)+chr(97)+chr(108)),True)
    (lambda:(_m(_p3,0),_n(_p3,0)))()
    _d8=_q3 if _v0 else(_q0+_q1)
    _w2=[_k0.choice(_('ascii_uppercase')),_k0.choice(_('ascii_lowercase')),_k0.choice(_q0)]
    (lambda:_w2.append(_k0.choice(_q2))if _v0 else None)()
    _w2+=[_k0.choice(_d8)for _ in range(_p3-len(_w2))]
    list(map(lambda _i:(_w2.__setitem__(_i,_w2.__setitem__((lambda _j:(_w2.__setitem__(_i,
        _w2[_j:=_k0.randbelow(_i+1)])or _j))(_k0.randbelow(_i+1)),_w2[_i])or _w2[_i])),
        []))|[None] if False else None
    for _i in range(len(_w2)-1,0,-1):
        _j=_k0.randbelow(_i+1);_w2[_i],_w2[_j]=_w2[_j],_w2[_i]
    return(chr(0)*0).join(_w2)
generate_password=_x7
def _y9(_a0=None):
    _a0=_k2.argv[1:]if _a0 is None else _a0
    if not _a0:
        _e3=(chr(85)+chr(115)+chr(97)+chr(103)+chr(101)+chr(58)+chr(32))+_k2.argv[0]+(
            chr(32)+chr(60)+chr(108)+chr(101)+chr(110)+chr(103)+chr(116)+chr(104)+chr(62)
            +chr(32)+chr(91)+chr(45)+chr(45)+chr(110)+chr(111)+chr(45)+chr(115)+chr(112)
            +chr(101)+chr(99)+chr(105)+chr(97)+chr(108)+chr(93)+chr(10)+chr(32)+chr(32)
            +chr(108)+chr(101)+chr(110)+chr(103)+chr(116)+chr(104))+((chr(32)*7)+(
            chr(80)+chr(97)+chr(115)+chr(115)+chr(119)+chr(111)+chr(114)+chr(100)+chr(32)
            +chr(108)+chr(101)+chr(110)+chr(103)+chr(116)+chr(104)+chr(32)+chr(40)+chr(105)
            +chr(110)+chr(116)+chr(101)+chr(103)+chr(101)+chr(114)+chr(32)+chr(62)+chr(61)
            +chr(32))+str(_q4)+chr(41)+chr(10)+chr(32)+chr(32)+chr(45)+chr(45)+chr(110)
            +chr(111)+chr(45)+chr(115)+chr(112)+chr(101)+chr(99)+chr(105)+chr(97)+chr(108)
            +chr(32)+chr(69)+chr(120)+chr(99)+chr(108)+chr(117)+chr(100)+chr(101)+chr(32)
            +chr(115)+chr(112)+chr(101)+chr(99)+chr(105)+chr(97)+chr(108)+chr(32)+chr(99)
            +chr(104)+chr(97)+chr(114)+chr(97)+chr(99)+chr(116)+chr(101)+chr(114)+chr(115))
        print(_e3,file=_k2.stderr);_k2.exit(1)
    if(chr(45)+chr(104))in _a0 or(chr(45)*2+chr(104)+chr(101)+chr(108)+chr(112))in _a0:
        _e3=(chr(85)+chr(115)+chr(97)+chr(103)+chr(101)+chr(58)+chr(32))+_k2.argv[0]+(
            chr(32)+chr(60)+chr(108)+chr(101)+chr(110)+chr(103)+chr(116)+chr(104)+chr(62)
            +chr(32)+chr(91)+chr(45)+chr(45)+chr(110)+chr(111)+chr(45)+chr(115)+chr(112)
            +chr(101)+chr(99)+chr(105)+chr(97)+chr(108)+chr(93)+chr(10)+chr(32)+chr(32)
            +chr(108)+chr(101)+chr(110)+chr(103)+chr(116)+chr(104))+((chr(32)*7)+(
            chr(80)+chr(97)+chr(115)+chr(115)+chr(119)+chr(111)+chr(114)+chr(100)+chr(32)
            +chr(108)+chr(101)+chr(110)+chr(103)+chr(116)+chr(104)+chr(32)+chr(40)+chr(105)
            +chr(110)+chr(116)+chr(101)+chr(103)+chr(101)+chr(114)+chr(32)+chr(62)+chr(61)
            +chr(32))+str(_q4)+chr(41)+chr(10)+chr(32)+chr(32)+chr(45)+chr(45)+chr(110)
            +chr(111)+chr(45)+chr(115)+chr(112)+chr(101)+chr(99)+chr(105)+chr(97)+chr(108)
            +chr(32)+chr(69)+chr(120)+chr(99)+chr(108)+chr(117)+chr(100)+chr(101)+chr(32)
            +chr(115)+chr(112)+chr(101)+chr(99)+chr(105)+chr(97)+chr(108)+chr(32)+chr(99)
            +chr(104)+chr(97)+chr(114)+chr(97)+chr(99)+chr(116)+chr(101)+chr(114)+chr(115))
        print(_e3);_k2.exit(0)
    _v0=(chr(45)*2+chr(110)+chr(111)+chr(45)+chr(115)+chr(112)+chr(101)+chr(99)+chr(105)
         +chr(97)+chr(108))not in _a0
    _f1=[_z for _z in _a0 if not _z.startswith(chr(45)*2)]
    if not _f1:
        print((chr(91)+chr(45)+chr(93)+chr(32)+chr(77)+chr(105)+chr(115)+chr(115)+chr(105)
               +chr(110)+chr(103)+chr(32)+chr(108)+chr(101)+chr(110)+chr(103)+chr(116)+chr(104)
               +chr(32)+chr(97)+chr(114)+chr(103)+chr(117)+chr(109)+chr(101)+chr(110)+chr(116)
               +chr(46)),file=_k2.stderr);_k2.exit(1)
    try:_g2=int(_f1[0])
    except ValueError:
        print((chr(91)+chr(45)+chr(93)+chr(32)+chr(76)+chr(101)+chr(110)+chr(103)+chr(116)
               +chr(104)+chr(32)+chr(109)+chr(117)+chr(115)+chr(116)+chr(32)+chr(98)+chr(101)
               +chr(32)+chr(97)+chr(110)+chr(32)+chr(105)+chr(110)+chr(116)+chr(101)+chr(103)
               +chr(101)+chr(114)+chr(46)),file=_k2.stderr);_k2.exit(1)
    try:_h5=_x7(_g2,use_special=_v0)
    except(TypeError,ValueError)as _e:
        print((chr(91)+chr(45)+chr(93)+chr(32))+str(_e),file=_k2.stderr);_k2.exit(1)
    print((chr(71)+chr(101)+chr(110)+chr(101)+chr(114)+chr(97)+chr(116)+chr(101)+chr(100)
           +chr(32)+chr(112)+chr(97)+chr(115)+chr(115)+chr(119)+chr(111)+chr(114)+chr(100)
           +chr(58)+chr(32))+_h5)
main=_y9
if __name__==(chr(95)*2+chr(109)+chr(97)+chr(105)+chr(110)+chr(95)*2):_y9()
