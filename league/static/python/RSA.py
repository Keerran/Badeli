from random import randint

import string


def lcm(x, y):
	"""This function takes two
	integers and returns the L.C.M."""

	# choose the greater number
	if x > y:
		greater = x
	else:
		greater = y

	while True:
		if (greater % x == 0) and (greater % y == 0):
			value = greater
			break
		greater += 1

	return value


def is_prime(a):
	return all(a % i for i in range(2, a))


def get_prime(l):
	found = False
	while not found:
		no = randint(2, l)
		if is_prime(no):
			found = True
	return no


def generate():
	generated = True
	while generated:

		p = get_prime(100)
		q = get_prime(100)

		n = p * q

		z = lcm((p - 1), (q - 1))

		e = get_prime(100)

		for nums in range(2, z):
			if (nums * e) % z == 1 % z:
				d = nums
				if d == e:
					break
				else:
					generated = False
					break

	public_key = [n, e]

	private_key = [n, d]

	final = public_key + private_key

	return final


def encrypt(x, k):
	com = k.index(",")

	n = k[:com]
	e = k[com + 2:]
	print(n)
	print(e)

	alpha = string.printable
	final_num = ""
	for letters in x:
		final_num = final_num + str(int(alpha.index(letters) + 10) ** int(e) % int(n)) + str(n)
	encrypted = hex(int(final_num))
	return encrypted[:-1]


def decrypt(x, k):
	com = k.index(",")

	n = k[:com]
	d = k[com + 2:]

	x = int(x, 16)
	x = str(x)
	alpha = string.printable
	final_words = ""
	num_val = ""
	while x != "":
		nums = x[0]

		if str(n) in x:

			if x[:len(str(n))] == str(n):

				final_words = final_words + alpha[((int(num_val) ** int(d)) % int(n)) - 10]
				num_val = ""
				x = x[len(str(n)):]

			else:
				num_val = num_val + nums
				x = x[1:]

	decrypted = final_words
	return decrypted


"""
RSA_G = (generate())
RSA_G_PRIV=""
RSA_G_PUB =""
c=1
for vals in RSA_G:
	if c ==1:
		RSA_G_PRIV=RSA_G_PRIV+str(vals)+", "
		
	elif c==2:
		RSA_G_PRIV = RSA_G_PRIV + str(vals)
	elif c==3:
		RSA_G_PUB=RSA_G_PUB+str(vals)+", "
	else:
		RSA_G_PUB= RSA_G_PUB + str(vals)
	c+=1
password = "password"
print("Pub is" +RSA_G_PUB)
print("Priv is" + RSA_G_PRIV)
encryptedPassword = (encrypt(password, RSA_G_PUB))
print("encrypted pass is" + encryptedPassword)
"""
