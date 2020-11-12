def cipher(plaintext,key):
    newstring=""
    encrypted_text=""
  
    alphabet = ("abcdefghijklmnopqrstuvwxyz")

    if plaintext.isupper():
        alphabet=alphabet.upper()
        
    for i in range(0,len(alphabet)):
        if (i+key) > 25:
            ciphertext = {alphabet[i]:alphabet[(i%(25-key+1))]}
          
        else:
            ciphertext = {alphabet[i]:alphabet[i+key]}

        newstring+=ciphertext[alphabet[i]]

    for c in range(len(plaintext)):
        for i in range(len(alphabet)):
            if plaintext[c] == alphabet[i]:
                encrypted_text+=newstring[i]

    return encrypted_text



    
