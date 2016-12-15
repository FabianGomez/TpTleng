import dibu.parser
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Parametros invalidos.")
        print("Uso:")
        print("  main.py expression")
        exit()
    # si desde la consola escrito la string asi con el \n no funcionaba
    # pero si lo asigno aca asi aun escribiendo \n anda.
    #text = "size width=200, height=200 \n rectangle width=200, height=200, upper_left=(1,1)"
    text = sys.argv[1]
    svg = dibu.parser.parse(text)
    print(svg)