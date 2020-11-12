def cipher(plaintext,key):
    newstring=""
    new_text=""
  
    characters = ("abcdefghijklmnopqrstuvwxyz1234567890")
        
    for i in range(0,len(characters)):
        if (i+key) >= len(characters):
            ciphertext = {characters[i]:characters[(i%(len(characters)-key))]}
          
        else:
            ciphertext = {characters[i]:characters[i+key]}

        newstring+=ciphertext[characters[i]]

    for c in range(len(plaintext)):
        for i in range(len(characters)):
            if plaintext[c] ==  characters[i]:
                new_text+=newstring[i]

    return new_text



    
