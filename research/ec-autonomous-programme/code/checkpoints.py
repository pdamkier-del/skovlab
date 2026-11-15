"""Lossless, hash-checked ECD field checkpoints. No object/pickle arrays.
Metadata distinguishes harmonic coordinate time from physical proper time.
"""
from pathlib import Path
import hashlib,json,os,tempfile
import numpy as np
from strong_benchmark import ecd


def array_digest(a):
    a=np.ascontiguousarray(a)
    h=hashlib.sha256();h.update(a.dtype.str.encode());h.update(str(a.shape).encode());h.update(a.tobytes());return h.hexdigest()


def save_checkpoint(path,grid,state,*,time,step,config,status='checkpoint',reason=None):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    if status not in ['initial','checkpoint','completed','rejected']:raise ValueError('Unknown checkpoint status.')
    shape=(grid.n,)*3
    if tuple(a.shape for a in state)!=(shape+(4,4),shape+(4,4),shape+(4,)):raise ValueError('Full 3D state shapes required.')
    if not all(np.all(np.isfinite(a)) for a in state):raise ValueError('Cannot persist nonfinite field as a restart checkpoint.')
    metadata={'schema':'skovlab-ecd-fields-v1','grid':{'n':grid.n,'half_width':grid.half_width,'boundary':grid.boundary,'dx':grid.dx},'coordinate_time':float(time),'time_coordinate':'harmonic; not uniform matter proper time','step':int(step),'units':'c=hbar=kappa=1; reduced Planck units','action':'neutral minimal one-species commuting classical ECD; m=0; GA=3/16','config':config,'status':status,'reason':reason,'field_hashes':{k:array_digest(a) for k,a in zip(['g','p','psi'],state)}}
    text=json.dumps(metadata,sort_keys=True,separators=(',',':'),allow_nan=False)
    fd,name=tempfile.mkstemp(prefix='.ecd-',suffix='.npz',dir=path.parent);os.close(fd)
    try:
        np.savez_compressed(name,g=state[0],p=state[1],psi=state[2],metadata=np.array(text))
        if path.exists():
            _,old,oldmeta=load_checkpoint(path,allow_rejected=True)
            if oldmeta!=metadata:raise FileExistsError('Refusing to overwrite a different checkpoint: '+str(path))
            os.unlink(name)
        else:os.replace(name,path)
    finally:
        if os.path.exists(name):os.unlink(name)
    return metadata


def load_checkpoint(path,*,allow_rejected=False):
    with np.load(path,allow_pickle=False) as data:
        metadata=json.loads(str(data['metadata'].item()));state=tuple(data[k].copy() for k in ['g','p','psi'])
    if metadata.get('schema')!='skovlab-ecd-fields-v1':raise ValueError('Unsupported field checkpoint schema.')
    if metadata['status']=='rejected' and not allow_rejected:raise ValueError('Rejected state is diagnostic evidence, not restart initial data.')
    grid=ecd.Grid(**{k:metadata['grid'][k] for k in ['n','half_width','boundary']})
    expected=((grid.n,)*3+(4,4),(grid.n,)*3+(4,4),(grid.n,)*3+(4,))
    if tuple(a.shape for a in state)!=expected:raise ValueError('Checkpoint shape/grid mismatch.')
    for k,a in zip(['g','p','psi'],state):
        if not np.all(np.isfinite(a)) or array_digest(a)!=metadata['field_hashes'][k]:raise ValueError('Corrupt field checkpoint: '+k)
    return grid,state,metadata
