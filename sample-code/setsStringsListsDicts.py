def longest(s1, s2):
    return ''.join(list(dict.fromkeys([letter for letter in sorted(s1+s2)])))
            
            
    #"".join(sorted(set(a1 + a2)))
    
    
    
    # uniqueLetters = []
    # for letter in s1+s2:
    #     if letter not in uniqueLetters:
    #         uniqueLetters.append(letter)
    # uniqueLetters.sort()
    # return ''.join(uniqueLetters)
            


a = "xyaabbbccccdefww"
b = "xxxxyyyyabklmopq"
print(longest(a, b)) # "abcdefklmopqwxy"
a = "abcdefghijklmnopqrstuvwxyz"
print(longest(a, a)) # "abcdefghijklmnopqrstuvwxyz"
print(longest("aretheyhere", "yestheyarehere")) # "aehrsty")
print(longest("loopingisfunbutdangerous", "lessdangerousthancoding")) # "abcdefghilnoprstu")
print(longest("inmanylanguages", "theresapairoffunctions")) # "acefghilmnoprstuy")