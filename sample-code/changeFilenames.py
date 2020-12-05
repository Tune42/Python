filenames = ["program.c", "stdio.hpp", "sample.hpp", "a.out", "math.hpp", "hpp.out"]
newfilenames = []

for index, filename in enumerate(filenames):
  newFileName = ""
  x = 0
  if ".hpp" in filename:
    x = filename.find(".hpp")
    newFileName = filename[:x+2]
  else:
    newFileName = filename
  newfilenames.append((filename, newFileName))

print (newfilenames) # Should be [('program.c', 'program.c'), ('stdio.hpp', 'stdio.h'), ('sample.hpp', 'sample.h'), ('a.out', 'a.out'), ('math.hpp', 'math.h'), ('hpp.out', 'hpp.out')]