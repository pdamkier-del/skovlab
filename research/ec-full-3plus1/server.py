"""Local browser access to the Python full-field research prototype."""
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
from threading import Lock
import argparse,json
from evolve import evolve
ROOT=Path(__file__).resolve().parent
LOCK=Lock()
ALLOWED={'n','half_width','amplitude','radius','mass','phase','spin_twist','K0','duration','dt'}

class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(ROOT),**kwargs)
    def send_json(self,value,status=200):
        payload=json.dumps(value,allow_nan=False).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(payload)));self.end_headers();self.wfile.write(payload)
    def do_GET(self):
        if self.path=='/api/status':self.send_json({'model':'full-3plus1-ecd','available':True});return
        super().do_GET()
    def do_POST(self):
        if self.path!='/api/run':self.send_json({'error':'Unknown endpoint'},404);return
        length=int(self.headers.get('Content-Length',0))
        if length<2 or length>4096:self.send_json({'error':'Invalid request size'},400);return
        if not LOCK.acquire(blocking=False):self.send_json({'error':'A calculation is already running.'},429);return
        try:
            values=json.loads(self.rfile.read(length))
            if not isinstance(values,dict) or set(values)-ALLOWED:raise ValueError('Unsupported parameters.')
            data,_=evolve(**values);self.send_json(data)
        except (ValueError,TypeError,RuntimeError) as e:self.send_json({'error':str(e)},400)
        finally:LOCK.release()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8770);args=p.parse_args()
    print(f'Open http://127.0.0.1:{args.port}/',flush=True)
    ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()
