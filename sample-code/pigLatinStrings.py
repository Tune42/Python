def pig_it(text):
  say = ""
  words = text.split(" ")
  for word in words:
    if word.isalpha():
      word = word[1:] + word[0] + "ay"
    say += word + " "
  return say[:-1]

print(pig_it('Pig latin is cool')) # igPay atinlay siay oolcay
print(pig_it('Hello world !'))   # elloHay orldway !