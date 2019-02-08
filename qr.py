import qrcode

itemnames = {'1':'soap', '2':'toothpaste', '3': 'chocolate', '4': 'deodorant', '5':'pencil'}

for item in itemnames.keys():
	img = qrcode.make(item)
<<<<<<< HEAD
	img.save("img/item"+item+".jpg")
=======
	img.save("item"+item+".jpg")
>>>>>>> d2256ef13c32e3a69cd0a2add21e148f6f4a35cd
