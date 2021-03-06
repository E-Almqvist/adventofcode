#!/usr/bin/env python

from aoc import get_input # AoC
import re # regex
import itertools as it

data = get_input(14).splitlines()

def listToString(s):

    str1 = ""
    for ele in s:
        str1 += ele

    return str1

def dectobin(num):
    return format(num, "036b")

def bintodec(_bin):
    return int(_bin, 2)

def parseLine(line):
    if( line[0:3] == "mem" ):
        address, val = re.match( r"^mem\[([0-9]+)\] = ([0-9]+)$", line ).groups()
        _bin = dectobin(int(val))

        return address, _bin

    else:
        op, mask = line.split(" = ")
        return op, mask

def applyMask( _bin, mask, includeX=False ):
    newbin = []
    newbin[:0] = _bin

    for i in range(len(mask)):
        if( mask[i] != "X" or includeX ):
            newbin[i] = mask[i]

    return listToString(newbin)

def getallcombs(xlen):
    return [list(i) for i in it.product(["0", "1"], repeat=xlen)]

def getAddressCombos(mask, addr):
    addrlist = []
    addrlist[:0] = addr

    combs = getallcombs( mask.count("X") )

    addrcombos = []

    for comb in combs:
        xcount = 0
        newaddrlist = [addr for addr in addrlist]
        for i in range( len(newaddrlist) ):
            char = newaddrlist[i]
            maskchar = mask[i]

            if(maskchar == "X"):
                newaddrlist[i] = comb[xcount]
                xcount += 1
            elif(maskchar == "1"):
                newaddrlist[i] = maskchar

        addrcombos.append( listToString(newaddrlist) )

    return addrcombos

# Part 1 & 2
mem, mem2, curMask = dict(), dict(), None

for line in data:
    address, val = parseLine(line)
    if( address != "mask" ):
        val = applyMask(val, curMask)
        dec_val = bintodec(val)

        mem[address] = dec_val

        # apply mask to address
        address = dectobin(int(address))
        addrlist = getAddressCombos(curMask, address)

        for addr in addrlist:
            decaddr = bintodec(addr)
            mem2[decaddr] = bintodec(val)

    else:
        curMask = val
        continue

memsum, memsum2 = sum(mem.values()), sum(mem2.values())

print("Part1:", memsum)
print("Part2:", memsum2)
