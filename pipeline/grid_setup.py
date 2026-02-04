import numpy as np

# siatka - ok 15000 punktow
X, Y = np.meshgrid(np.arange(0, 7.55, 0.05), np.arange(0, 5.05, 0.05))
Nx = X.shape[1]
Ny = X.shape[0]
N = Nx * Ny

''' Cała konstrukcja podzialu przestrzeni opiera się na nieco może prymitywnym pomyśle , 
ale krótko mówiąc dodaje wartości True/False określonym punktom siatki w zależności od tego 
jakim są sektorem : okno, wnętrze itd. 

Jeśli chciałem np. sprawdzić poprawność pokrycia mojej siatki, wystarczy sprawdzić czy w tablicy ,
która łączy wszystkei te sektory znajdują się wart. False. 
Gdy to sprwdzałem był dosłownie jeden punkt siatki nie przypisany co pominąłem bo w zasadzie 
nic to nie zmienia dla siatki w której punktów jest 15 000   
'''


'''
 sciana zewnetrzna - laczac mieszkanie z otoczeniem zewnetrznym bloku(nie sciana z sasiadem)
 tutaj o wymiarach na szerokosc 1 punkta siatki 
 tylko 1 w cel uzastosowania warunku robina prosto. 
 w zmiennej is_innerwall dodane sa dwa punkty szerokosci siatki ktore maja mniejsza dyfuzje 
 co koncowa daje zew. sciane postaci 3 punkty siatki szerokosci , gdzie dwa wewnetrzne peirwsze 
 punkty maja jedynie zmniejszona dyfuzje zgodnei z konstrukcja sciany
'''
is_outerwall = np.isclose(X, 7) & (((Y > 0) & (Y < 1)) | ((Y > 4) & (Y < 5)))

# sciana z sasiadem
is_neighborwall = np.isclose(Y, 0) | np.isclose(Y, 5) | np.isclose(X, 0)

# sciany wewnetrzne - miedzy pokojami
is_innerwall = ((((Y > 2.95) & (Y < 3.15)) & ((X > 0) & (X < 1.5))) |
                (((X > 1.45) & (X < 1.65)) & ((Y > 3.5) & (Y < 5))) |
                (((X > 1.95) & (X < 2.10)) & ((Y > 0) & (Y < 3))) |
                (((X > 3.45) & (X < 3.65)) & ((Y > 3.45) & (Y < 5))) |
                (((X > 6.85) & (X < 7)) & (((Y > 0) & (Y < 1)) | ((Y > 4) & (Y < 5)))) |
                (((X > 3.45) & (X < 7)) & ((Y > 2.95) & (Y < 3.15))))

# okno - szeroksoc 1 punkta siatki - uwzglednia to realna grubosc okien.
is_window = np.isclose(X, 7) & ((Y >= 1) & (Y <= 4))

# punkty grzejnika
is_radiator = ((((X > 0.45) & (X < 1.25)) & np.isclose(Y, 3.2)) |
               (((X <= 6.75) & (X > 6.60)) & ((Y > 0.50) & (Y < 1.2))) |
               (((X <= 6.60) & (X > 6.4)) & ((Y < 4) & (Y > 3.3))))


# wewnetrzna przestrzen - czyli wszsytko poza powyzszymi
is_innerspace = ~(is_outerwall | is_neighborwall | is_innerwall | is_window | is_radiator)
