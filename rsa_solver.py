#!/usr/bin/env python3

print('\nThe fastest way to retreive the prime numbers of "n" is to run the command "msieve" in the terminal.\nElse, you can go to https://www.alpertron.com.ar/ECM.HTM .\n')

prime_factor_1 = int(input('Provide the first prime factor: '))
prime_factor_2 = int(input('Provide the second prime factor: '))

x = [prime_factor_1, prime_factor_2]

n = int(input('Provide the n value: '))
e = int(input('Provide the e value: '))

ct = int(input('Provide the ciphertext: '))

# start value for phi(n)
i = 1

# loop through prime factors and multiply them together with (factor-1)*(nextFactor-1)...
for a in x:
    i = i * (a-1)

# inverse pow (3.8+ syntax, for previous versions of python use gmpy2.invert)
d = pow(e, -1, i)

# solve for the answer
ans = pow(ct, d, n)

# print the answer
print(bytes.fromhex(hex(ans)[2:]).decode('ascii'))
