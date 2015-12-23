#!/bin/python

def fetch(l, index, default):
    try:
        return l[index]
    except:
        return default
