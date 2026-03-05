# -*- coding: utf-8 -*-
(lambda _:(lambda __:__(_,__))(lambda _,__:None))(0x0)
import argparse as _m0,hashlib as _m1,logging as _m2,os as _m3,sys as _m4,time as _m5
from base64 import b64decode as _xd
_=lambda _b:_xd(_b).decode()
_k3=type(chr(95)+chr(107)+chr(51),(),{chr(95)*2+chr(118):lambda _s:setattr(_s,chr(95)+chr(122),0x0),chr(95)*2+chr(98)+chr(111)+chr(111)+chr(108)+chr(95)*2:lambda _s:False})
_T=[_(s)for s in[b"c2hhMjU2",b"U2Nhbm5pbmcgZGlyZWN0b3J5OiAlcw==",
b"U2tpcHBpbmcgc3ltbGluazogJXM=",b"Q291bGQgbm90IHJlYWQgZmlsZTogJXMgKCVzKQ==",
b"W0RSWS1SVU5dIFdvdWxkIHJlbW92ZSBkdXBsaWNhdGU6ICVz",
b"UmVtb3ZlZCBkdXBsaWNhdGU6ICVz",b"Q291bGQgbm90IHJlbW92ZSBmaWxlOiAlcyAoJXMp",
b"RmluZCBhbmQgcmVtb3ZlIGR1cGxpY2F0ZSBmaWxlcyBpbiBhIGRpcmVjdG9yeSB0cmVlLg==",
b"ZGlyZWN0b3J5",b"Um9vdCBkaXJlY3RvcnkgdG8gc2NhbiBmb3IgZHVwbGljYXRlcy4=",
b"LS1kcnktcnVu",b"UmVwb3J0IGR1cGxpY2F0ZXMgd2l0aG91dCBkZWxldGluZyB0aGVtLg==",
b"LS1sb2ctZmlsZQ==",
b"UGF0aCBmb3IgdGhlIGxvZyBmaWxlIChkZWZhdWx0OiA8ZGlyZWN0b3J5Pi9jbGVhbnVwLmxvZyku",
b"JShhc2N0aW1lKXMgICUobGV2ZWxuYW1lKS04cyAgJShtZXNzYWdlKXM=",
b"Tm90IGEgdmFsaWQgZGlyZWN0b3J5OiA=",b"Y2xlYW51cC5sb2c=",
b"U3RhcnRpbmcgc2NhbjogJXMgKGRyeV9ydW49JXMp",
b"U2Nhbm5lZCAlZCBmaWxlcyBpbiAlLjJmIHNlYw==",
b"RW5jb3VudGVyZWQgJWQgZXJyb3Iocyk=",b"Tm8gZHVwbGljYXRlIGZpbGVzIGZvdW5kLg==",
b"V291bGQgcmVtb3Zl",b"UmVtb3ZlZA==",b"JXMgJWQgZHVwbGljYXRlIGZpbGUocyku",
b"dXRmLTg="]]
_C=0x1<<0xD
_nop=lambda *_a,**_kw:(None,setattr(_k3,'_z',0x1)if 0 else None)[0]
def _0xA3(_p,_g=None):
    _g=_g if _g is not None else _T[0];_h=_m1.new(_g)
    with open(_p,chr(0x72)+chr(0x62))as _f:
        while True:
            _c=_f.read(_C)
            if not _c:break
            _h.update(_c)
    return _h.hexdigest()
def _0xB7(_d,_dr=False):
    _se,_r,_sc,_e=set(),0x0,0x0,0x0
    for _rt,_di,_fs in _m3.walk(_d,topdown=True):
        _fs and _m2.info(_T[1],_rt)
        for _n in _fs:
            _fp=_m3.path.join(_rt,_n)
            if _m3.path.islink(_fp):
                _m2.debug(_T[2],_fp);continue
            try:
                _fh=_0xA3(_fp);_sc+=0x1
            except OSError as _x:
                _e+=0x1;_m2.warning(_T[3],_fp,_x);continue
            if _fh not in _se:
                _se.add(_fh)
            else:
                if _dr:
                    _m2.info(_T[4],_fp)
                else:
                    try:
                        _m3.remove(_fp);_m2.info(_T[5],_fp)
                    except OSError as _x:
                        _e+=0x1;_m2.warning(_T[6],_fp,_x);continue
                _r+=0x1
    return(_r,_sc,_e)
def _0xC1():
    _p=_m0.ArgumentParser(description=_T[7])
    _p.add_argument(_T[8],help=_T[9])
    _p.add_argument(_T[10],action=(lambda:chr(0x73)+chr(0x74)+chr(0x6f)+chr(0x72)+chr(0x65)+chr(0x5f)+chr(0x74)+chr(0x72)+chr(0x75)+chr(0x65))(),default=not True,help=_T[11])
    _p.add_argument(_T[12],default=None,help=_T[13])
    return _p
def _0xD4(_lp):
    _fmt=_T[14]
    _hs=[_m2.StreamHandler(_m4.stdout),_m2.FileHandler(_lp,encoding=_T[24])]
    _m2.basicConfig(level=_m2.INFO,format=_fmt,handlers=_hs)
def _0xE9(_ar=None):
    _pa=_0xC1();_op=_pa.parse_args(_ar)
    _di=_m3.path.abspath(getattr(_op,_T[8]))
    if not(_m3.path.isdir(_di)):_pa.error(_T[15]+_di)
    _lp=getattr(_op,chr(0x6c)+chr(0x6f)+chr(0x67)+chr(0x5f)+chr(0x66)+chr(0x69)+chr(0x6c)+chr(0x65))or _m3.path.join(_di,_T[16])
    _0xD4(_lp);_nop()if(0x0&0xFF)else None
    _dr=getattr(_op,chr(100)+chr(114)+chr(121)+chr(95)+chr(114)+chr(117)+chr(110))
    _m2.info(_T[17],_di,_dr);_st=_m5.time()
    _rv,_sn,_er=_0xB7(_di,_dr=_dr)
    _el=_m5.time()-_st;_m2.info(_T[18],_sn,_el)
    _er and _m2.info(_T[19],_er)
    (_m2.info(_T[20])if _rv==0x0 else(_m2.info(_T[23],(_T[21]if _dr else _T[22]),_rv)))
    return 0x0
def make_hash(_fp,algorithm=None):return _0xA3(_fp,_g=algorithm)
def scan_directory(_d,dry_run=False):return _0xB7(_d,_dr=dry_run)
main=_0xE9
if __name__==chr(0x5f)*2+chr(0x6d)+chr(0x61)+chr(0x69)+chr(0x6e)+chr(0x5f)*2:
 try:_m4.exit(_0xE9())
 except KeyboardInterrupt:_m2.info(chr(0x53)+chr(0x63)+chr(0x61)+chr(0x6e)+chr(0x20)+chr(0x69)+chr(0x6e)+chr(0x74)+chr(0x65)+chr(0x72)+chr(0x72)+chr(0x75)+chr(0x70)+chr(0x74)+chr(0x65)+chr(0x64)+chr(0x2e));_m4.exit(0x82)
