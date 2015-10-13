import collections
import functools
import cPickle as pickle

class memoized(object):
   '''Decorator. Caches a function's return value each time it is called.
   If called later with the same arguments, the cached value is returned
   (not reevaluated).

   https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
   '''
   def __init__(self, func):
      self.func = func
      try:
         with open('.search_cache','rb') as inf:
            self.cache = pickle.load(inf)
      except Exception:
         self.cache = {}
   def __call__(self, *args):
      if not isinstance(args, collections.Hashable):
         # uncacheable. a list, for instance.
         # better to not cache than blow up.
         print "Uncacheable"
         return self.func(*args)
      if args in self.cache:
         print "Read from cache"
         return self.cache[args]
      else:
         value = self.func(*args)
         self.cache[args] = value
         with open('.search_cache', 'wb') as op:
            pickle.dump(self.cache, op)
            print "Wrote to cache"
         return value
   def __repr__(self):
      '''Return the function's docstring.'''
      return self.func.__doc__
   def __get__(self, obj, objtype):
      '''Support instance methods.'''
      return functools.partial(self.__call__, obj)
