list_key = ['name', 'lastname','sex','age']
list_value = ['Uladzislau','Charches','man', 29]
# condition
if len(list_key) > len(list_value):
      while len(list_key)>len(list_value):
        list_value.append('None')
# print
print(dict(zip(list_key,list_value)))