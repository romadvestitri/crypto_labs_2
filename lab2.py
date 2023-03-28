def read_binary_file(path):
    file_content = ""
    with open(path, "rb") as f:
        file_content = f.read()

    content_code_list = [char for char in file_content]
    return content_code_list

def write_to_binary_file(file_path, content):
    with open(file_path, "wb") as f:
        arr = bytes(content)
        f.write(bytes(content))

def CheckKey(key):
	digits = ['0','1']
	newkey = ''
	for sym in key:
		if sym in digits:
			newkey += sym
	if len(newkey) < 30:
		return None
	else:
		return newkey

def GetLSFR(state, len_file):
	#state = 0b111111111111111111111111111111
	str_bin = ''
	for i in range(len_file):
		shifted = state & 0b100000000000000000000000000000 
		#print(shifted, end = ' ')
		if shifted == 536870912:
			shifted_bin = '1'
		else:
			shifted_bin = '0'

		str_bin += shifted_bin
		

		bit1 = state & 0b100000000000000000000000000000
		bit2 = state & 0b0001
		bit3 = state & 0b100000000000000
		bit4 = state & 0b1000000000000000
		bit1 = bit1 >> 29 
		bit3 = bit3 >> 14
		bit4 = bit4 >> 15
		#print(bin(bit1))
		#print(bin(bit2))
		#print(bin(bit3))
		#print(bin(bit4))
		#print()
		newbit = bit1 ^ bit2 ^ bit3 ^ bit4
		#print(bin(newbit), end = ' ')
		state = (state << 1) | newbit
		#print(bin(state))

	#for i in range(len(str_bin)):
	#	print(str_bin[i], end = '')
	#	if i % 8 == 0 and i != 0:
	#		print(end = ' ')
	
	#print(str_bin)
	converted = int(str_bin, 2)
	print(converted)

	byte_arr = converted.to_bytes(1+((converted.bit_length() + 7) // 8), byteorder = 'big')
	#print(len(byte_arr))

	return str_bin, byte_arr

def Encrypt(path, key):
	lastslash = path.rfind("/")
	partpath = path[0:lastslash] + "/"
	#print(partpath)
	point = path.rfind(".")
	extension = path[point:len(path)]
	filename = path[lastslash+1:point]
	#print(filename)
	if filename.find("encrypted_") != -1:
		filename = "decrypted_" + filename[filename.find("encrypted_")+10:point]
	else:
		filename = "encrypted_"+filename
	new_path = partpath + filename + extension
	contents = read_binary_file(path)
	key = int(key, 2)
	resultLSFR = GetLSFR(key, len(contents)*8)
	crypto_arr = resultLSFR[1]
	print(len(contents))
	print(len(crypto_arr))
	encrypt_content = []

	plaintext = ''
	ciphedtext = ''

	#print('file:')
	for i in range(len(contents)):
		plaintext += bin(contents[i]).lstrip('0b')
		result = contents[i] ^ crypto_arr[i]
		encrypt_content.append(result)
		ciphedtext += bin(result).lstrip('0b')
	write_to_binary_file(new_path, encrypt_content)

	with open('plaintext.txt', "w") as f:
		f.write(plaintext)
	with open('ciphedtext.txt', "w") as f:
		f.write(ciphedtext)
	with open('key.txt', "w") as f:
		f.write(resultLSFR[0])


	return plaintext, ciphedtext, resultLSFR[0]

#Encrypt('/Users/roman/TI/lab2/encrypted_index.html', '000000001111111111111111111111')











