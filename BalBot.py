

#Gyro Read
#Tyler Conley
#CANT FIND MY GLASSES STUDIO


import smbus
import odrive

class mpu6050:

	#Global Variables
	GMS2 = 9.88665    #to calculate m/s^2
	address = None
	bus = None

	#Scale Modifiers
	AccScale_2G = 16384.0
	AccScale_4G = 8192.0
	AccScale_8G = 4096
	AccScale_16G = 2048

	GScale_250DEG =131.0
	GScale_500DEG = 65.5
	GScale_1000DEG = 32.8
	GScale_2000DEG = 16.4

	#Serial Bus Range of possible Addresses
	AccRange_2G = 0x00
	AccRange_4G = 0x08
	AccRange_8G = 0x10
	AccRange_16G = 0x18

	GRange_250DEG =0x00
	GRange_500DEG = 0x08
	GRange_1000DEG = 0x10
	GRange_2000DEG = 0x18

	#MPU6050 Registers
	PowMan1 = 0x6B
	PowMan2 = 0x6C

	AccX = 0x3B
	AccY = 0x3D
	AccZ =0x3F

	Temp = 0x41

	GX = 0x43
	GY = 0x45
	GZ = 0x47

	AccConfig = 0x1C
	GConfig = 0x1B

	def __init__(self, address, bus=1):
		self.address = address
		self.bus =smbus.SMBus(bus)
		#wakes up the MPU6050 because default is sleep mode
		self.bus.write_byte_data(self.address, self.PowMan1, 0x00)

	#I2C communication

	def read_i2c_word(self, register):
		#read data from the registers
		high = self.bus.read_byte_data(self.address, register)
		low = self.bus.read_byte_data(self.address, register + 1)

		value = (high << 8) + low

		if(value >= 0x8000):
			return -((65535 - value) + 1)
		else:
			return value

	#MPU6050 Methods???
	#def get_temp(self):
	#	raw_temp = self.read_i2c_word(self.Temp)
	#	actual_temp = (raw_temp / 340.0) + 36.53
	#	return actual_temp

	#Acceleration Range?
	def set_accel_range(self, accel_range):
		#set to 0x00 to clear attribute value
		self.bus.write_byte_data(self.address, self.AccConfig, 0x00)
		#write the new range to tha AccConfig Register
		self.bus.write_byte_data(self.address, self.AccConfig, accel_range)

	def read_accel_range(self, raw = False):
		#Reads the range the accelerometer is set to
		#if True it will set to value from AccConfig
		#if False it will return an integer: -1, 2, 4, 8 or 16
		#if it returns -1 something went wrong
		raw_data = self.bus.read_byte_data(self.address, self.AccConfig)

		if raw is True:
			return raw_data
		elif raw_data == self.AccRange_2G:
			return 2
		elif raw_data == self.AccRange_4G:
			return 4
		elif raw_data == self.AccRange_8G:
			return 8
		elif raw_data == self.AccRange_16:
			return 16

	#retrieves the gyro X Y and Z values
	def get_accel_data(self, g = False):
		#if g is true data is returned in G's (gravitational force)
		#if g is fales data is returned in m/s^2
		x = self.read_i2c_word(self.AccX)
		y = self.read_i2c_word(self.AccY)
		z = self.read_i2c_word(self.AccZ)

		accel_scale_modifier = None
		accel_range = self.read_accel_range(True)

		#checks for value on each possible register
		#then assigns the data found to the acceleration modifier variable
		if accel_range == self.AccRange_2G:
			accel_scale_modifier = self.AccScale_2G
		elif accel_range == self.AccRange_4G:
			accel_scale_modifier = self.AccScale_4G
		elif accel_range == self.AccRange_8G:
			accel_scale_modifier = self.AccScale_8G
		elif accel_range == self.AccRange_16G:
			accel_scale_modifier = self.AccScale_16G
		else:
			print("Not in range  -->  accel_scale_modifier set to self.AccScale_2G")
			accel_scale_modifier = self.AccScale_2G


	#ACCELERATION VALUES
		#scale X accelerometer data and assign to variable x
		x = x / accel_scale_modifier
		#scale Y accelerometer data and assign to variable y
		y = y / accel_scale_modifier
		#scale Z accelerometer data and assign to cariable z
		z = z / accel_scale_modifier

		#if data is in G's
		if g is True:
			return {'x': x, 'y': y, 'z': z}
		#if data is in m/s^2
		if g is False:
			x = x * self.GMS2
			y = y * self.GMS2
			z = z * self.GMS2
			return {'x': x, 'y': y, 'z': z}

	#sets range of gyro
	def set_gyro_range(self, gyro_range):
		#clears register first
		self.bus.write_byte_data(self.address, self.GConfig, 0x00)
		#writes the new range to the GConfig register
		self.bus.write_byte_data(self.address, self.GConfig, gyro_range)

	def read_gyro_range(self, raw = False):
		#reads in the range of the gyro
		raw_data = self.bus.read_byte_data(self.address, self.GConfig)

		#if raw pulls back any data
		if raw is True:
			return raw_data
		#if no data pulled back check possible range configurations in degrees
		elif raw is False:
			if raw_data == self.GRange_250DEG:
				return 250
			elif raw_data == self.GRange_500DEG:
				return 500
			elif raw_data == self.GRange_1000DEG:
				return 1000
			elif raw_data == self.GRange_2000DEG:
				#something went wrong
				return -1

	#retreives Gyro X Y and Z values and reads values in a dictionary
	def get_gyro_data(self):
		x = self.read_i2c_word(self.GX)
		y = self.read_i2c_word(self.GY)
		z = self.read_i2c_word(self.GZ)

		gyro_scale_modifier = None
		gyro_range = self.read_gyro_range(True)

		if gyro_range == self.GRange_250DEG:
			gyro_scale_modifier = self.GScale_250DEG
		elif gyro_range == self.GRange_500DEG:
			gyro_scale_modifier = self.GScale_500DEG
		elif gyro_range == self.GRange_1000DEG:
			gyro_scale_modifier = self.GScale_100DEG
		elif gyro_range == self.GRange_2000DEG:
			gyro_scale_modifier = self.GScale_2000DEG
		else:
			print("Not in range = gyro_scale_modifier set to self.GScale_250DEG")
			gyro_scale_modifier = self.GScale_250DEG

		#scale gyro data and assign values to x y and z
		x = x / gyro_scale_modifier
		y = y / gyro_scale_modifier
		z = z / gyro_scale_modifier

		return{'x': x, 'y': y, 'z': z}
		#return ('x': x, 'y': y, 'z': z)

	#reads and returns all available data
	def get_all_data(self):
		temp = self.get_temp()
		accel = self.get_accel_data()
		gyro = self.get_gyro_data()

		return(accel, gyro, temp)

i = 1
while i > 0:
	if __name__ == "__main__":
		mpu = mpu6050(0x68)
		print('\n')
		accel_data = mpu.get_accel_data()
		gyro_data = mpu.get_gyro_data()

		#HERE'S THE DATA !!! =======================================
		print("AX ", accel_data['x'], "  GX ", gyro_data['x'])
		print("AY ", accel_data['y'], " GY ", gyro_data['y'])
		print("AZ ", accel_data['z'], " GZ ", gyro_data['z'])
		print('\n')
		#HERE'S THE DATA !!! ======================================



	#PLACE ODRIVE CONTROL CODE HERE WITHIN THE WHILE LOOP THAT'S READING THE SENSOR !!! ==================
	


	#PLACE ODRIVE CONTROL CODE HERE WITHIN THE WHILE LOOP THAT'S READING THE SENSOR !!! ==================