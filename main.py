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

# Sender field for email
sender = "example@gmail.com"

# Establish the connection on a specific port
ser = serial.Serial('/dev/ttyACM1', 9600) 

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
			qty = input('Enter quantity of ' + itemnames[itemid]+ ': ')
			self.billqty.update({itemid: qty})

			# Decide whether or not to add another item 
			ch = input('\nEnter y to add another item, any other key to proceed billing: ')

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
	with open("Customers.txt") as custfile:
		for line in custfile: 
			tokens = line.split()
			emails.update({tokens[0]:tokens[1]})
	
	choice = 'y'
	while choice == 'y':

		todo = input('1. Generate bills\n2. Add items to stock\n3. Exit\nEnter choice: ')

		# Generate bills 
		if todo == '1':

			# Store item details from stock in dictionaries
			with open("Items.txt") as itemfile:
				for line in itemfile:
					tokens = line.split()
					itemnames.update({tokens[0]:tokens[1]})
					prices.update({tokens[0]:tokens[2]})

			c = 'y'
			# This program can generate a 100 bills in a run
			while c == 'y':
				# Generate a bill id
				b = random.randint(1,101)

				# Get the customer id (phone number) - unique.
				cust = input('Enter the customer id: ')  

				# Checking for a new customer
				if cust not in emails.keys():

					print("\n*** New customer information ***\n")
					cust = input('Enter new customer id (cust+idno): ')
					img = qrcode.make(cust)
					img.save(cust+".jpg")
					emailid = input('Enter email of the customer: ')
					with open("Customers.txt", 'a') as custfile:
						custfile.write(cust+" "+emailid+'\n')

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
				c = input('Do you want to generate another bill? y for yes ')
			continue

		# Add items to the stock
		elif todo == '2':
			# 
			add = 'y'
			while add == 'y':
				print("\n$$$ New item information $$$\n")
				item = input('Enter item id: ')
				img = qrcode.make(item)
				img.save("img/item"+item+".jpg")
				name = input('Enter item name: ')
				price = input('Enter item price: ')

				with open("Items.txt", 'a') as itemfile:
					itemfile.write(item+ " "+name+ " "+price+'\n')

				add = input('Do you want to add another item to the stock? y for yes ')


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
