# -*- coding: utf-8 -*-
"""
@authors: david & guille
"""

import numpy as np

def ROTL8(x, shift):
    return ((x << shift) | (x >> (8 - shift))) & 0xFF

class AES():
    def __init__(self, key):
        self.key = key
        self.make_sbox()
       
    def encode(self, message, rounds=10, padding=' '):
        if isinstance(message, str):
            message = list(map(ord, message))
        message += 15 * [ord(padding)]
        blocks = len(message) // 16
        cipher = []
        for i in range(blocks):
            block = message[i * 16:(i + 1) * 16]
            block = np.array(block, dtype='uint8').reshape((4, 4))
            block = self.transform_block(block, rounds)
            cipher += list(block.flatten())
        return np.array(cipher)
    
    def transform_block(self, block, rounds):
        self.key_i = self.key.copy()
        self.Rcon = np.array([1,0,0,0])
        self.block = block
        self.add_round_key()
        for _ in range(rounds - 1):
            self.byte_sub()
            self.shift_row()
            self.mix_column()
            self.add_round_key()
        self.byte_sub()
        self.shift_row()
        self.add_round_key()
        return self.block
    
    def add_round_key(self):
        self.block = self.block ^ self.key_i
        self.transform_key()
        
    def byte_sub(self):
        # The goal of this function is to perform the byte substitution 
        # (hence the name) of each element in the message block, using the
        # corresponding elements of the substitution bytes matrix (sbox).
        for row in range(4):
            for col in range(4):
                self.block[row,col] = self.sbox[self.block[row,col]]
    
    def shift_row(self):
        # Get the block, and shift its rows to the left:
            # The first row doesn't change at all
            # The second row gets its columns shifted one position
            # The third one gets them shifted two positions to the left
            # And the fourth gets them shifted three positions to the left
        for row in range(4):
            self.block[row] = np.roll(self.block[row], -row)
    
    def mix_column(self):
        # Polynomial reduction / capping the result
        poly = 0b100011011
        cap = lambda num: num ^ poly if num >> 8 else num
        
        # Multiplication functions
        x1 = lambda num: num
        x2 = lambda num: cap(num << 1)
        x3 = lambda num: x2(num) ^ num
        mix = np.array([
            [x2, x3, x1, x1],
            [x1, x2, x3, x1],
            [x1, x1, x2, x3],
            [x3, x1, x1, x2]
        ])
        
        # Matrix multiplication
        result = np.zeros((4, 4), dtype='uint8')
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    result[i,j] ^= mix[i,k](self.block[k,j])
        
        # Save result
        self.block = result

    def transform_key(self):
        # Select the last column of the current key,
        rotWord = self.key_i[:,-1].copy()
        for i in range(4):
            # Substitute its contents using the sbox
            rotWord[i] = self.sbox[rotWord[i]]
        # Shift the substituted last column
        rotWord = np.roll(rotWord,-1)
        
        # We will now perform the XOR on:
            #The transformed last column
            #The first column of the key
            #Rcon
        newKey = np.zeros([4,4], dtype='uint8')
        newKey[:,0] = self.key_i[:,0] ^ rotWord ^ self.Rcon
        newKey[:,1] = self.key_i[:,1] ^ newKey[:,0]
        newKey[:,2] = self.key_i[:,2] ^ newKey[:,1]
        newKey[:,3] = self.key_i[:,3] ^ newKey[:,2]
        
        self.key_i = newKey
        
        # Update the Rcon vector.
        # For that, we will need some utility functions:
            # Polynomial reduction / capping the result
        poly = 0b100011011
        cap = lambda num: num ^ poly if num >> 8 else num
            # Multiplication by 2
        x2 = lambda num: cap(num << 1)
        self.Rcon[0] = x2(self.Rcon[0])

            
    def make_sbox(self):
        # This function creates the subsitution matrix for the AES ciphering
        # algorithm.
        
        # Code adapted from Wikipedia:
            # https://en.wikipedia.org/wiki/Rijndael_S-box
        p = 1
        q = 1
        firstTime = True
        sbox = np.zeros((256), dtype='uint8')
        
        while p != 1 or firstTime:
            # multiply p by 3
            p = (p ^ (p << 1) ^ (0x1B if (p & 0x80) else 0)) & 0xFF
            
            # divide q by 3 (equals multiplication by 0xf6)
            q ^= q << 1
            q ^= q << 2
            q ^= q << 4
            q ^= 0x09 if q & 0x80 else 0
            q &= 0xFF
            
            # compute the affine transformation
            xformed = q ^ ROTL8(q, 1) ^ ROTL8(q, 2) ^ ROTL8(q, 3) ^ ROTL8(q, 4);
            
            sbox[p] = xformed ^ 0x63
            firstTime = False
        
        # 0 is a special case since it has no inverse
        sbox[0] = 0x63
        
        self.sbox=sbox
        