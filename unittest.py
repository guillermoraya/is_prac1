# -*- coding: utf-8 -*-
"""
@author: david
"""

import numpy as np
np.set_printoptions(formatter={'int':hex})
from AES import AES

if __name__ == "__main__":
    # Key matrix
    initial = np.array([
        [0x2b, 0x28, 0xab, 0x09],
        [0x7e, 0xae, 0xf7, 0xcf],
        [0x15, 0xd2, 0x15, 0x4f],
        [0x16, 0xa6, 0x88, 0x3c],
    ], dtype='int')
    
    transformed = np.array([
        [0xa0, 0x88, 0x23, 0x2a],
        [0xfa, 0x54, 0xa3, 0x6c],
        [0xfe, 0x2c, 0x39, 0x76],
        [0x17, 0xb1, 0x39, 0x05],
    ], dtype='int')
    
    # State matrix
    message = np.array([
        [0x32, 0x88, 0x31, 0xe0],
        [0x43, 0x5a, 0x31, 0x37],
        [0xf6, 0x30, 0x98, 0x07],
        [0xa8, 0x8d, 0xa2, 0x34],
    ], dtype='int')
    
    rounded = np.array([
        [0x19, 0xa0, 0x9a, 0xe9],
        [0x3d, 0xf4, 0xc6, 0xf8],
        [0xe3, 0xe2, 0x8d, 0x48],
        [0xbe, 0x2c, 0x2a, 0x08],
    ], dtype='int')
    
    substituted = np.array([
        [0xd4, 0xe0, 0xb8, 0x1e],
        [0x27, 0xbf, 0xb4, 0x41],
        [0x11, 0x98, 0x5d, 0x52],
        [0xae, 0xf1, 0xe5, 0x30],
    ], dtype='int')
    
    shifted = np.array([
        [0xd4, 0xe0, 0xb8, 0x1e],
        [0xbf, 0xb4, 0x41, 0x27],
        [0x5d, 0x52, 0x11, 0x98],
        [0x30, 0xae, 0xf1, 0xe5],
    ], dtype='int')
    
    mixed = np.array([
        [0x04, 0xe0, 0x48, 0x28],
        [0x66, 0xcb, 0xf8, 0x06],
        [0x81, 0x19, 0xd3, 0x26],
        [0xe5, 0x9a, 0x7a, 0x4c],
    ], dtype='int')
    
    added = np.array([
        [0xa4, 0x68, 0x6b, 0x02],
        [0x9c, 0x9f, 0x5b, 0x6a],
        [0x7f, 0x35, 0xea, 0x50],
        [0xf2, 0x2b, 0x43, 0x49],
    ], dtype='int')
    
    output = np.array([
        [0x39, 0x02, 0xdc, 0x19],
        [0x25, 0xdc, 0x11, 0x6a],
        [0x84, 0x09, 0x85, 0x0b],
        [0x1d, 0xfb, 0x97, 0x32],
    ], dtype='int')
    
    aes = AES(None)

    aes.key_i = initial.copy()
    aes.transform_key()
    if not np.all(aes.key_i == transformed):
        print("Error while transforming key")
        print(f"Expected:\n{transformed}")
        print(f"Result:\n{aes.key_i}")
        print()
        
    aes.block = rounded.copy()
    aes.byte_sub()
    if not np.all(aes.block == substituted):
        print("Error while substituting state")
        print(f"Expected:\n{substituted}")
        print(f"Result:\n{aes.block}")
        print()
    
    aes.block = substituted.copy()
    aes.shift_row()
    if not np.all(aes.block == shifted):
        print("Error while shifting state ")
        print(f"Expected:\n{shifted}")
        print(f"Result:\n{aes.block}")
        print()
    
    aes.block = shifted.copy()
    aes.mix_column()
    if not np.all(aes.block == mixed):
        print("Error while mixing state")
        print(f"Expected:\n{mixed}")
        print(f"Result:\n{aes.block}")
        print()
    
    aes.block = mixed.copy()
    aes.key_i = transformed.copy()
    aes.transform_key = lambda: None
    aes.add_round_key()
    if not np.all(aes.block == added):
        print("Error while adding key to state")
        print(f"Expected:\n{added}")
        print(f"Result:\n{aes.block}")
        print()
        
    aes = AES(initial)
    out = aes.transform_block(message, 10)
    if not np.all(out == output):
        print("Error while transforming block")
        print(f"Expected:\n{output}")
        print(f"Result:\n{out}")
        print()