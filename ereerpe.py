from math import ceil

class shannon():
  def __init__(self, d):
    self.d = d
    self.code = {}

  def shanon_start(self):
    diff1=diff2=0
    if len(self.d) == 1:
      k = list(self.d.keys())[0]
      self.code[k] = "1"
      return
    if len(self.d) == 2:
      k = list(self.d.keys())
      k1 = k[0]
      k2 = k[1]
      self.code[k1] = "0"
      self.code[k2] = "1"
      return
    half = ceil(sum(self.d.values()) / 2)
    for index in range(len(self.d)-1):
      d1 = dict(list(self.d.items())[:index+1])
      d2 = dict(list(self.d.items())[index+1:])
      sum1 = sum(d1.values())
      sum2 = sum(d2.values())
      diff1 = (sum1 - half)
      diff2 = (sum2 - half)
      if sum1 >= half:
        break

    self.sha(d1, "0")
    self.sha(d2, "1")

  def sha(self, dict_, c):
    diff1=diff2=0
    if len(dict_) == 1:
      k = list(dict_.keys())[0]
      self.code[k] = c
      return
    if len(dict_) == 2:
      self.sha(dict(list(dict_.items())[:1]), c+"0")
      self.sha(dict(list(dict_.items())[1:]), c+"1")
      return
      
    half = ceil(sum(dict_.values()) / 2)
    for index in range(len(dict_)-1):
      d1 = dict(list(dict_.items())[:index+1])
      d2 = dict(list(dict_.items())[index+1:])
      sum1 = sum(d1.values())
      sum2 = sum(d2.values())
      diff1 = (sum1 - half)
      diff2 = (sum2 - half)

      if sum1 >= half:
        break
      
    self.sha(d1, c+"0")
    self.sha(d2, c+"1")

    
def main():

  print('Hello, world!')

  l = [1/2, 1/4, 1/8, 1/16, 1/32, 1/64, 1/64]
  anita = [6/15, 2/15, 2/15, 2/15, 2/15, 1/15]
  anita2 = [6, 2, 2, 2, 2, 1]
  d = {"a":6, "i":2, "l":2, "n":2, "t":2, "v":1}
  d = dict(sorted(d.items(), key=lambda item: item[1], reverse=True))
  
  w = shannon(d)
  w.shanon_start()
  print("CODIGO: ", w.code)

if __name__ == "__main__":
  main()
