import itertools

def izzi(ssid):

    filename = "dictionary/" + ssid + ".txt"

    archivo = open(filename,'w');

    gen = itertools.combinations_with_replacement('0123456789ABCDEF',8) 
    for password in gen:                                                       
        par2 = password[0]+password[1]+password[2]+password[3]+password[4]+password[5]+password[6]+password[7] + ssid[-4:]
        with open(filename, 'a') as file:
            file.write(par2 + '\n')
    
   # print(par2)

