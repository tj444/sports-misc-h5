import os
import hashlib
import json

def isLocal():
  return os.environ.get('local') == 'true'

def sha256Sum(text):
  h = hashlib.sha256()
  h.update(text.encode())
  return h.hexdigest()

def http400(start_response):
  status = '400 Bad Request'
  response_headers = []
  start_response(status, response_headers)
  return []

def http500(start_response):
  status = '500 Server Error'
  response_headers = []
  start_response(status, response_headers)
  return []

def http200(start_response, data):
  status = '200 OK'
  response_headers = [('Content-type', 'application/json')]
  start_response(status, response_headers)
  return [json.dumps(data).encode()]