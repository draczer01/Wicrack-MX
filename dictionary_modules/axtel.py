import itertools

def axtel():

    print("Bienvenido al generador de contrasenias de Axtel, fabor de ingresar los ultimos 4 caracteres del ssid");

    par1 = input("AXTEL-EXTREMO")

    print(par1);

    print("por fabor eliga el nombre del archivo para generar las contrasenias");


    filename = input();

    archivo = open(filename,'w');

    gen = itertools.combinations_with_replacement('0123456789QWERTYUIOPASDFGHJKLZXCVBNM',4) 
    for password in gen:                                                       
        par2 = password[0]+password[1]+password[2]+password[3] + par1
        with open(filename, 'a') as file:
            file.write(par2 + '\n')
    
   # print(par2)
