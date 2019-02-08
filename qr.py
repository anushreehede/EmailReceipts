import qrcode

itemnames = {'1':'soap', '2':'toothpaste', '3': 'chocolate', '4': 'deodorant', '5':'pencil'}

for item in itemnames.keys():
	img = qrcode.make(item)
	img.save("img/item"+item+".jpg")
