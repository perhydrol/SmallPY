from cmath import inf
from multiprocessing import Process,Queue,Pipe
import os
from readline import write_history_file
from time import process_time_ns

def info(title):
  print('Name:',__name__)
  print('Parent Process:',os.getppid())
  print('Process id:',os.getpid())

def f(name,q):
  info('function f')
  print('Hello',name)
  while True:
    q.send(['f'])

def ff(name,q):
  info('function ff')
  print('Hello',name)
  while True:
    q.send(['ff'])
  n=0

if __name__=='__main__':
  q=Queue()
  pr,pc=Pipe()
  pr2,pc2=Pipe()
  info('Main Line')
  p=Process(target=f,args=('bob',pc,))
  pp=Process(target=ff,args=('Alex',pc2,))
  p.start()
  pp.start()
  while True:
    print(pr.recv())
    print(pr2.recv())
  p.join()
  pp.join()