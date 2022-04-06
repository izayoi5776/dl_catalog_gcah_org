import os

flg1st = True
with open('merged.json', 'w') as f:
  f.write('[\n')
  for root, dis, files in os.walk('json'):
      for file in files:
          if file.endswith('.json'):
              with open(os.path.join(root, file), 'r') as fr:
                  print("merge file=" + file)
                  data = fr.read()
              if flg1st:
                flg1st = False
              else:
                f.write(",\n")
              f.write(data)

  f.write("\n]")
