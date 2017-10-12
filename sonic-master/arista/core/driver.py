from __future__ import print_function

import logging
import subprocess

from utils import inDebug, inSimulation

def modprobe(name, args=None):
   logging.debug('loading module %s', name)
   if args is None:
      args = []
   args = ['modprobe', name.replace('-', '_')] + args
   if inDebug():
      args += [ 'dyndbg=+pf' ]
   if inSimulation():
      logging.debug('exec: %s', ' '.join(args))
   else:
      subprocess.check_call(args)

def rmmod(name):
   logging.debug('unloading module %s', name)
   args = ['modprobe', '-r', name.replace('-', '_')]
   if inSimulation():
      logging.debug('exec: %s', ' '.join(args))
   else:
      subprocess.check_call(args)

def isModuleLoaded(name):
   with open('/proc/modules') as f:
      start = '%s ' % name.replace('-', '_')
      for line in f.readlines():
         if line.startswith(start):
            return True
   return False

class Driver(object):
   def __init__(self, component):
      self.component = component

   def setup(self):
      pass

   def finish(self):
      pass

   def clean(self):
      pass

   def resetIn(self):
      pass

   def resetOut(self):
      pass

   def dump(self, depth=0, prefix=' - '):
      spacer = ' ' * (depth * 3)
      print('%s%s%s' % (spacer, prefix, self))

class KernelDriver(Driver):
   # TODO: handle multiple kernel modules
   def __init__(self, component, module, args=None):
      super(KernelDriver, self).__init__(component)
      self.component = component
      self.module = module
      self.args = args if args is not None else []

   def setup(self):
      modprobe(self.module, self.args)

   def clean(self):
      if self.loaded():
         try:
            rmmod(self.module)
         except Exception as e:
            logging.error('Failed to unload %s: %s', self.module, e)
      else:
         logging.debug('Module %s is not loaded', self.module)

   def loaded(self):
      return isModuleLoaded(self.module)

   def getSysfsPath(self):
      raise NotImplementedError

   def __str__(self):
      return '%s(%s)' % (self.__class__.__name__, self.module)
