import json, os, random
os.chdir(os.path.dirname(__file__))
ABECEDARIO = "qwertyuiopasdfghjklñzxcvbnmáéíóú"
MAX_ERRORES = 10


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def archivos():
    with open("spanish.json", "r", encoding="utf-8") as f:  
        data = json.load(f) # Abre y carga los datos json (cierra el archivo automaticamente) 
    with open("hangman.json", "r", encoding="utf-8") as f:
        ascii_art = json.load(f) # Abre y carga los datos, pero el resultado queda en el diccionario. 


    # Verificación para que hangman.json tenga las suficientes etapas antes de empezar.
    etapas = ascii_art["Hangman"] # Atajo para no escribir ascii_art["Hangman"] cada vez.
    if len(etapas) < MAX_ERRORES + 1: # Verifica que la lista tenga 11 elementos. 
        raise ValueError( # Si esto se cumple mostrar error. 
            f"hangman.json tiene solo {len(etapas)} etapas en 'Hangman', "
            f"pero se necesitan {MAX_ERRORES + 1} (índices 0 a {MAX_ERRORES})."
        )
    
    return data, etapas

def imprimir(etapas, errores, tabla):
    clear() # Imprime el nuevo estado del juego y elimina el anterior, funciona como loop.
    print(etapas[errores])
    linea = ' '.join(tabla) # Une los elementos de la tabla con separación de un espacio 
    print(f"\n  {linea}\n") 
    print(f"  Intentos fallidos  : {errores}/{MAX_ERRORES}")
    print(f"  Intentos restantes : {MAX_ERRORES - errores}")
    return linea

def normalizar(c):
    return 'a' if c == 'á' else 'e' if c == 'é' else 'i' if c == 'í' else 'o' if c == 'ó' else 'u' if c == 'ú' else c

def valida(usadas):
    print()
    c= input("  Adivinanza: ").lower().strip()
    while not (len(c) == 1 and c in ABECEDARIO and c not in usadas):
        print("\033[A\033[2K", end="")   # sube 1 línea y la borra
        print("\033[A\033[2K", end="")   # sube otra línea y la borra
        
        if len(c) !=1 : print("  ERROR: Ingresa solo UNA letra a la vez.")
        elif c not in ABECEDARIO: print(f"  ERROR:'{c}' no es una letra válida del abecedario.")
        elif c in usadas: print(f"  ERROR: la letra '{c}' ya fue ingresada antes.")
        c= input("  Adivinanza: ")
    c = normalizar(c)
    return c

data, etapas = archivos()
invalido = []
usadas = set()
errores = 0
real = random.choice(data).lower()
palabra_norm = ''.join(normalizar(x) for x in real)
tabla = ['_' for i in range(len(real))]


clear()
while True:
    lineas = imprimir(etapas, errores, tabla)
    if invalido: print(f"  Letras incorrectas : {', '.join(invalido)}")

    if '_' not in lineas:
        print("\n  Ganaste!")
        break    
    if errores>=MAX_ERRORES:
        print("\n  Perdiste!")
        print(f"  Palabra correcta: {real.capitalize()}")
        break    

    print()
    caracter = valida(usadas)
    if caracter in palabra_norm: 
        for i,x in enumerate(real):
            v = normalizar(x)
            if caracter == v: 
                tabla[i] = x

    else: 
        errores+=1
        invalido.append(caracter)
    usadas.add(caracter)

#Nota, los tildes son una cosa medio rara del juego que hay que tener en cuenta. 