'''Module to drive inlretro binary usage via subprocesses in Python.'''

import subprocess

class INLRunner(object):
    BIN = './inlretro'

    def __init__(self, dry_run=True):
        self._lock = False
        self._dry_run = dry_run
        self._dump_filename = 'dump.bin'
        self._process = None
    
    def _try_run_subprocess(self, args):

        args = [self.BIN, '--lua_filename=scripts/inlretro2.lua'] + [str(s) for s in args]
        if self._dry_run:
            args = ['echo'] + args
        if not self._lock:
            self._lock = True
            self._process = subprocess.Popen(args)#, stdout=subprocess.PIPE)
    
    def dump_rom(self, console_name, rom_size_mbit):
        '''Attempt dump of any non-NES cartridge.'''
        dump_args = ['-c', console_name, '-z', str(rom_size_mbit), '-d', self._dump_filename]
        self._try_run_subprocess(dump_args)
    
    def readline_stdout(self):
        if self._process:
            return self._process.stdout.readline()
        else:
            return None

    def is_done(self):
        if self._process is None:
            return True
        
        self._process.poll()
        if self._process.returncode != None:
            self._lock = False
            return True
        return False