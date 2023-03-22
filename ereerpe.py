from math import ceil

class shannon():
  def __init__(self, d):
    self.d = d
    self.code = [] #{}

  def shanon_start(self):
    #print("***")
    diff1=diff2=0
    #print("I: ", self.d)
    if len(self.d) == 1:
      self.code.append("1")
      return
    if len(self.d) == 2:
      self.code.append("0")
      self.code.append("1")
      return
    half = ceil(sum(self.d.values() / 2)
    #print("H:", half)
    for index in range(len(self.d)-1):
      #group1 = iterable[:index+1]
      #group2 = iterable[index+1:]
      d1 = dict(list(self.d.items())[:index+1])
      d2 = dict(list(self.d.items())[index+1:])
      sum1 = sum(d1.values())
      sum2 = sum(d2.values())
      diff1 = (sum1 - half)
      diff2 = (sum2 - half)
      if sum1 >= half:
        #print("G:", group1, group2)
        #print("S:", sum1, sum2)
        #print("D:", diff1, diff2)
        #print("====================")
        break

    self.sha(d1, "0")
    self.sha(d2, "1")

  def sha(self, iterable, c):
    print("*_*")
    print("i: ", iterable)
    diff1=diff2=0
    if len(iterable) == 1:
      self.code.append(c)
      print("[c): ", c)
      return
    if len(iterable) == 2:
      self.sha(iterable[:1], c+"0")
      self.sha(iterable[1:], c+"1")
      return
      
    half = ceil(sum(iterable) / 2)
    print("h:", half)
    for index in range(len(iterable)-1):
      group1 = iterable[:index+1]
      group2 = iterable[index+1:]
      sum1 = sum(group1)
      sum2 = sum(group2)
      diff1 = (sum1 - half)
      diff2 = (sum2 - half)

      if sum1 >= half:
        print("g:", group1, group2)
        print("s", sum1, sum2)
        print("d:", diff1, diff2)
        print("-------------------")
        break
      
    self.sha(group1, c+"0")
    self.sha(group2, c+"1")

    
def main():

  print('Hello, world!')

  l = [1/2, 1/4, 1/8, 1/16, 1/32, 1/64, 1/64]
  anita = [6/15, 2/15, 2/15, 2/15, 2/15, 1/15]
  anita2 = [6, 2, 2, 2, 2, 1]
  d = {"a":6, "i":2, "l":2, "n":2, "t":2, "v":1}
  d = sorted(d)

  w = shannon(d)
  w.shanon_start()
  print("CODIGO: ", w.code)

if __name__ == "__main__":
  main()
