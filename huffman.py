# -*- coding: utf-8 -*-

# Developed by : Wesley Ferreira de Ferreira
# Computer Science student on Universidade Federal do Pampa(UNIPAMPA) - RS, Brazil
# Contact: wferreira531@gmail.com

import struct
import binascii
from sys import *
from string import *

def huffman(p): #Method of the huffman algorithm
    if(len(p) == 2):
        return dict(zip(p.keys(), ['0', '1']))

    #Creates a node with the sum of the lowest recurrence
    novo = p.copy()
    a1, a2 = parMenorProb(p)
    p1, p2 = novo.pop(a1), novo.pop(a2)
    novo[a1 + a2] = p1 + p2

    #Recursive call
    c = huffman(novo)
    ca1a2 = c.pop(a1 + a2)
    c[a1], c[a2] = ca1a2 + '0', ca1a2 + '1'

    return c

def parMenorProb(p):# return from list the less probability pair
	assert(len(p) >= 2)
	sorted_p = sorted(p.items(), key=lambda (i,pi): pi)
	return sorted_p[0][0], sorted_p[1][0]

def hextobin(hexval):
        tam = len(hexval)*4
        binval = bin(int(hexval, 16))[2:]
        while ((len(binval)) < tam):
            binval = '0' + binval
        return binval
        
def compress(arquivoi):

	try:
		fi = open(arquivoi, "r")
		fo = open(arquivoi[:find(arquivoi, '.'):]+".dat", "wb")
	except:
		print("\nError 1: Could not open file {} to compress\n".format(arquivoi))
		return
	texto = ""
	contagem = {}
	
	while True:
		c = fi.read(1)
		if not c:
			break
		if c in contagem:
			contagem[c] += 1
		else:
			contagem[c] = 1
	
	contagem = huffman(contagem)
	fi.seek(0)
	while True:
		c = fi.read(1)
		if not c:
			break
		texto+=contagem[c]
		
	b = bytearray()
	for i in range(0, len(texto), 8):
		byte = texto[i:i+8]
		b.append(int(byte, 2))
		
	fo.write(bytes(arquivoi + "  "))
	fo.write(bytes(str(contagem) + "  "))
	fo.write(bytes(b))
	fi.close()
	fo.close()

def decompress(arquivoi):

	try:
		fi = open(arquivoi, "rb")
		arquivoo = ""
		while not ("  " in arquivoo):
			arquivoo += fi.read(1)
		arquivoo = arquivoo[:find(arquivoo, ' '):]
		fo = open(arquivoo, "w")
		texto = ""
		temp = ""
		contagem = ""
	except:
		print("\nError 2: Could not open file {} to decompress\n".format(arquivoi))
		return
	
	while not ("  " in contagem):
		contagem += fi.read(1)
	contagem = eval(contagem)
	
	texto = binascii.hexlify(fi.read())
	texto = hextobin(texto)

	for i in texto:
		if bool(temp):
			if temp in contagem.values():
				fo.write("{}".format(contagem.keys()[contagem.values().index(temp)]))
				temp = ""
			temp+=i
		else:
			temp+=i
	fi.close()
	fo.close()

def main():
	try:
		if(argv[1] == "-h"):
			print("\nHow to use:	{} <options> <file>".format(argv[0]))
			print("Options:")
			print("-h: show this text")
			print("-c: compress the file")
			print("-d: decompress the file")
			print("Error codes:")
			print("Error 1: Could not open file {} to compress")
			print("Error 2: Could not open file {} to decompress\n")
		if(argv[1] == "-c"):
			compress(argv[2])
		if(argv[1] == "-d"):
			decompress(argv[2])
	except:
		print("\nUse: {} -h to know how tu use\n".format(argv[0]))
		return

if __name__=="__main__":
	main()
