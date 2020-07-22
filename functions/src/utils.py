import os
import hashlib

def isLocal():
  return os.environ.get('local') == 'true'

def sha256Sum(text):
  h = hashlib.sha256()
  h.update(text.encode())
  return h.hexdigest()