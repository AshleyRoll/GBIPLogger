"""
The base class for all GPIB interfaces

Derived classes must implement the given methods.
"""

from abc import ABCMeta, abstractmethod

class GPIBBase(metaclass=ABCMeta):
	@abstractmethod
	def open(self):
		"Open and initialise the interface"
		pass
	
	@abstractmethod
	def close(self):
		"Close the interface"
		pass
		
	@abstractmethod
	def select(self, addr):
		"Select the device address to talk to"
		pass
		
	@abstractmethod
	def interface_clear(self):
		"Clear the GPIB interface and release the active device"
		pass
		
	@abstractmethod
	def selected_device_clear(self):
		"Clear / reset the selected device"
		pass
		
	@abstractmethod
	def write(self, cmd):
		"Write a command to the device"
		pass

	@abstractmethod
	def read(self, num_bytes):
		"read a result from the device"
		pass
	
	@abstractmethod
	def readeol(self, num_bytes):
		"read a result from the device until LF"
		pass

	@abstractmethod
	def query(self, cmd, buffer_size):
		"Send a command and read the response"
		pass
		

class GPIBTimeout(Exception):
	"This excpetion is raised if a communication timeout occurs during reading GPIB responses"

