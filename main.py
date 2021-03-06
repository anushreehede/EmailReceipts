# For email sending API
import mail
# For generating random numbers
import random
# For generating QR codes
import qrcode
# For removing text file
import os
# For reading serial input from QR code scanner
import serial
# For using a database
import MySQLdb as mariadb

# Sender field for email
sender = "example@gmail.com"

# Establish the connection on a specific port
# ser = serial.Serial('/dev/ttyACM1', 9600) 

# Establish a connection to the database
host='localhost'
user='root'
password='xxx'
database='email_receipts'
mariadb_connection = mariadb.connect(host, user, password, database)
cursor = mariadb_connection.cursor()

# Common dictionaries for any bill

# Dictionary mapping item id to item name
itemnames = {}

# Dictionary mapping item id to item price
prices = {}

# Customers and their mail ids
emails = {}

# Bill class
class Bill:

	# Bill class variables
	billid = ''
	billqty = {} # dictionary mapping item id to quantity of that item in that bill 
	custid = ''

	# Bill class constructor
	def __init__(self, billid, custid):
		self.billid = billid
		self.billqty = {}
		self.custid = custid

	# Method to add items to billqty 
	def addItems(self):
		print('#### Billing id: ' + self.billid+ ' ####')
		ch = 'y'
		while ch == 'y':
			# Scanning process 
			# Get the unique item id for the purchased item from the serial cable, using the app, Bluetooth and Arduino
			itemid = ser.readline().decode('utf-8')[:-2]
			print('You are buying: ' + itemnames[itemid])

			# Entering quantity for item and storing the pair in bill qty
			qty = raw_input('Enter quantity of ' + itemnames[itemid]+ ': ')
			self.billqty.update({itemid: qty})

			# Decide whether or not to add another item 
			ch = raw_input('\nEnter y to add another item, any other key to proceed billing: ')

	# Method to calculate the total bill from billqty
	# Generate receipts. Print to console, store in file, email to customer.
	def calculateBill(self):

		# Open receipts file to store
		with open('Receipts.txt', 'a') as the_file:
			bill = "\t\t\t ANUSHREE'S (EMAIL-BASED) RETAIL INVOICE"
			bill += ('\n\n******** Bill: '+ self.billid+ ' ********\n')
			the_file.write('\n******** Bill: '+ self.billid+ ' ********\n')

			# Calculation of total bill and storing in file
			total = 0
			for item in self.billqty.keys():
				value = int(self.billqty[item]) * int(prices[item])
				the_file.write('\t'+ itemnames[item]+ ': '+ self.billqty[item] + ' * ' + str(prices[item]) + ' = ' + str(value)+'\n')
				bill += ('\t'+ itemnames[item]+ ': '+ self.billqty[item] + ' * ' + prices[item] + ' = ' + str(value)+'\n')
				total += value
			bill += ('\nTotal: ' + str(total)+ '\n')
			bill += '\n\n\t\t\t THANK YOU! VISIT AGAIN!\n'
			the_file.write('\nTotal: ' + str(total)+ '\n')

			# Printing the receipt to console
			print(bill)

			# Sending the receipt to the email id of the current bill's customer 
			to = emails[self.custid]
			subject = "Customer id: "+self.custid+ " for bill id: "+self.billid
			msgPlain = bill
			mail.SendMessage(sender, to, subject, msgPlain)

def main():
	# Remove any old receipts
	if os.path.isfile("Receipts.txt"): 
				os.remove("Receipts.txt")

	# Get all the current customer emails in the dictionary
	# with open("Customers.txt") as custfile:
	# 	for line in custfile: 
	# 		tokens = line.split()
	# 		emails.update({tokens[0]:tokens[1]})
	cursor.execute("SELECT * FROM customer")
	for phone, cust_name, email in cursor:
		emails.update({phone: (cust_name, email)})
	
	choice = 'y'
	while choice == 'y':

		todo = raw_input('1. Generate bills\n2. Add items to stock\n3. Exit\nEnter choice: ')

		# Generate bills 
		if todo == '1':

			# Store item details from stock in dictionaries
			cursor.execute("SELECT * FROM items")
			for item_id, item_name, price in cursor:
				itemnames.update({item_id:item_name})
				prices.update({item_id:price})

			# with open("Items.txt") as itemfile:
			# 	for line in itemfile:
			# 		tokens = line.split()
			# 		itemnames.update({tokens[0]:tokens[1]})
			# 		prices.update({tokens[0]:tokens[2]})

			c = 'y'
			# This program can generate a 100 bills in a run
			while c == 'y':
				# Generate a bill id
				b = random.randint(1,101)

				# Get the customer id (phone number) - unique.
				cust = raw_input('Enter the customer phone number: ')  

				# Checking for a new customer
				if cust not in emails.keys():

					print("\n*** New customer information ***\n")
					cust = raw_input('Enter phone number: ')
					c_name = raw_input('Enter name: ')
					emailid = raw_input('Enter email of the customer: ')
					# with open("Customers.txt", 'a') as custfile:
					# 	custfile.write(cust+" "+c_name+" "+emailid+'\n')
					cursor.execute("INSERT INTO customer (phone,cust_name,email) VALUES (%s,%s,%s)", (cust, c_name, emailid))
					mariadb_connection.commit()
					
					emails.update({cust: (c_name, emailid)})

				# Generate a bill with a bill id for a particular customer
				bill = Bill(str(b), cust) 
				
				# Add items to this bill
				bill.addItems()

				# Calculate the total bill 
				# Print receipt to console
				# Store receipt in a file
				# Email receipt to customer
				bill.calculateBill()

				# Decide whether or not to generate next bill
				c = raw_input('Do you want to generate another bill? y for yes ')
			continue

		# Add items to the stock
		elif todo == '2':
			# 
			add = 'y'
			while add == 'y':
				print("\n$$$ New item information $$$\n")
				item = raw_input('Enter item id: ')
				img = qrcode.make(item)
				img.save("img/item"+item+".jpg")
				name = raw_input('Enter item name: ')
				price = raw_input('Enter item price: ')

				# with open("Items.txt", 'a') as itemfile:
				# 	itemfile.write(item+ " "+name+ " "+price+'\n')

				cursor.execute("INSERT INTO items (item_id,item_name,price) VALUES (%s,%s,%s)", (item, name, price))
				mariadb_connection.commit()

				add = raw_input('Do you want to add another item to the stock? y for yes ')


			continue
		# Exit
		elif todo == '3':
			print("That's all for now folks!") # Try to ensure bill ids don't clash (IMP)
			break

		# Default
		else:
			print('Press 1, 2 or 3 to proceed. \n')
			continue
		
if __name__ == '__main__':
    main()
