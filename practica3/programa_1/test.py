"""placeholder"""
g = "110100111"
c = "0" * (len(g) - 1)
d = "101"


def crc_encode(g, c, d):
    """placeholder"""
    g = [ int(x, 2) for x in g ]
    c = [ int(x, 2) for x in c ]
    d = [ int(x, 2) for x in d ]
    
    print("-"*40)
    for b in d:
        p = c[0] ^ b
        for i in range(0, len(c) - 1):
            #print(i, " | ", c[i+1], " ^ (" , p, " & ", g[i+1], " ) = ", end=" ")
            c[i] = c[i+1] ^ (p & g[i+1])
            #print(c[i])
        #print("z"," | ", c[-1], " <== " , p, " = ", end=" ")
        c[-1] = p
        #print(c[-1])
        print(b, p, c)

    print("-"*40)
    print(c)
    return d + c


def crc_decode(g, c, m):
    """placeholder"""
    g = [int(x, 2) for x in g ]
    c = [int(x, 2) for x in c ]
    #m = [int(x, 2) for x in m]
    
    print("-"*40)
    for b in m:
        p = c[0] ^ b
        for i in range(0, len(c) - 1):
            #print(i, " | ", c[i+1], " ^ (" , p, " & ", g[i+1], " ) = ", end=" ")
            c[i] = c[i+1] ^ (p & g[i+1])
            #print(c[i])
        #print("z"," | ", c[-1], " <== " , p, " = ", end=" ")
        c[-1] = p
        #print(c[-1])
        print(b, p, c)

    print("-"*40)
    print(c)
    return any(c)



def main():
    """main"""
    m = crc_encode(g,c,d)
    print(m)
    r = crc_decode(g,c,m)
    print(r)


if __name__ == "__main__":
    print("start")
    main()
    print("end")