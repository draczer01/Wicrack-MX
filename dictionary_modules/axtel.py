import itertools

def axtel(ssid):
  
    filename = "dictionary/" + ssid + ".txt"

    archivo = open(filename,'w');

    gen = itertools.combinations_with_replacement('0123456789ABCDEF',4) 
    for password in gen:                                                       
        par2 = password[0]+password[1]+password[2]+password[3] + ssid[-4:]
        with open(filename, 'a') as file:
            file.write(par2 + '\n')
    
   # print(par2)
