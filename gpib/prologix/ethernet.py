from gpib.base import GPIBBase, GPIBTimeout
import socket
import time

class PrologixEthernetGPIB(GPIBBase):
	"Allows the use of the Prologix Ethernet GPIB Interface"

	_PORT = 1234		#ethernet interface always uses this port number
	_ESC = '\x1B'
	_READ_DELAY = .05

	def __init__(self, hostname, timeout=1):
		GPIBBase.__init__(self)
		self.host = hostname
		self.timeout = timeout
		self.socket = socket.socket(socket.AF_INET,
									socket.SOCK_STREAM,
									socket.IPPROTO_TCP)
		self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
		
		self.socket.settimeout(self.timeout)

	def open(self):
		# Open attempt to connect to the Ethernert GPIB Interface
		self.socket.connect( (self.host, self._PORT) )
		# perform the house keeping initialisation
		self._setup()


	def close(self):
		self.socket.close()

	def select(self, addr):
		self._send('++addr %i' % int(addr))

	def interface_clear(self):
		self._send('++ifc')

	def selected_device_clear(self):
		self._send('++clr')

	def write(self, cmd):
		self._send(self._escape(cmd))
		time.sleep(self._READ_DELAY) # A delay is needed between writes and reads
		
	def read(self, num_bytes=1024):
		self._send('++read eoi')
		try:
			return self._recv(num_bytes).strip(' \t\n\r')
		except socket.timeout:
			raise GPIBTimeout()

	def readeol(self, num_bytes=1024):
		self._send('++read 10')	# read to LF character
		try:
			return self._recv(num_bytes).strip(' \t\n\r')
		except socket.timeout:
			raise GPIBTimeout()

	def query(self, cmd, buffer_size=1024*1024):
		self.write(self._escape(cmd))
		return self.read(buffer_size)


	#
	# Internal implementation
	#
	def _escape(self, command):
		command = command.replace(self._ESC, self._ESC + self._ESC)
		command = command.replace('+', self._ESC + '+')
		command = command.replace('\n', self._ESC + '\n')
		command = command.replace('\r', self._ESC + '\r')
		return command


	def _send(self, value):
		encoded_value = ('%s\n' % value).encode('ascii')
		self.socket.sendall(encoded_value)
		

	def _recv(self, byte_num):
		value = self.socket.recv(byte_num)
		value = value[:-1]		# remove trailing null
		return value.decode('ascii')

	def _setup(self):
		#  First, disable configuration saving to prevent spamming the EEPROM
		self._send('++savecfg 0')

		# Controller Mode
		self._send('++mode 1')

		# Disable auto read, we will manage this
		self._send('++auto 0')

		# set GPIB timeout
		self._send('++read_tmo_ms 3000')

		#
		self._send('++eos 3')


