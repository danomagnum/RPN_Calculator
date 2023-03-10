import errors

DISPLAY_BIN = 2
DISPLAY_DEC = 10
DISPLAY_OCT = 8
DISPLAY_HEX = 16
DISPLAY_ASCII = 128
DISPLAY_COMMA = 256


def space_every(binstring, spacing=4, char=' ', prefix_len = 2, pad=True, padchar='0'):
	# add spaces every 4 bits in a binary string
	newstring = binstring 
	if len(binstring) > (spacing + prefix_len):
		newstring = space_every(binstring[:-spacing]) + char + binstring[-spacing:]
	elif len(binstring) < (spacing + prefix_len):
		if pad:
			l = len(binstring) - prefix_len
			newstring = binstring[:prefix_len] + padchar * (spacing - l) + binstring[prefix_len:]

	return newstring



class Function(object):
	def __init__(self, name=None, stack = None, comment = ''):
		self.name = name
		if stack is None:
			self.stack = []
		else:
			self.stack = stack
		self.comment = comment
	
	def reassign(self, interp, val):
		if type(val) == Variable:
			var = Variable(self.name, val.val)
			interp.variables[self.name] = var
			return var
		elif type(val) == Value:
			var = Variable(self.name, val.val)
			interp.variables[self.name] = var
			return var
		elif type(val) == Function:
			self.stack = val.stack
			interp.variables[self.name] = self 
			return self 
		elif type(val) == NULL:
			var = Variable(self.name, NULL())
			interp.variables[self.name] = var
			return var
	def __str__(self):
		name = ''
		in_str = False
		for x in self.stack:
			if str(x) == "'":
				in_str = not in_str
			if in_str:
				name += str(x)
			else:
				name += str(x) + " "
		name = '[ ' + name + ']'

		if self.name is not None:
			name += ' ' + self.name + ' = '

		if self.comment:
			name += ' ' + self.comment + '"'
		return name

	def __len__(self):
		if self.stack is None:
			return 0
		else:
			return len(self.stack)

	def __eq__(self, other):
		if type(other) != Function:
			return False
		return other.stack == self.stack

	def get_index(self, index):
		if index < len(self.stack):
			return self.stack[index]
		elif (-1 * index) <= len(self.stack):
			return self.stack[index]
		else:
			raise errors.OutOfBounds("Cannot acess data outside of bounds")

	def get_var(self, varname):
		for item in self.stack:
			if isinstance(item, Variable):
				if item.name == varname:
					return item
			elif isinstance(item, Function):
				if item.name == varname:
					return item

		raise errors.VarNotFound("Variable " + varname + " was not found")
	

	
	def pop(self, count = 1):
		return self.stack.pop()
		vals = []
		for x in range(count):
			vals.append(Value(self.stack.pop()))
		return vals
	

class Variable(object):
	def __init__(self, name, val=0, comment='', mode=DISPLAY_DEC) :
		self.name = name
		self.val = val
		self.comment = comment
		self.mode = mode
	def reassign(self, interp, val):
		if type(val) == Variable:
			self.val = val.val
			return self
		elif type(val) == Value:
			self.val = val.val
			return self
		elif type(val) == Function:
			f = Function(self.name, val.stack, self.comment)
			interp.variables[self.name] = f
			return f
		elif type(val) == NULL:
			var = Variable(self.name, NULL())
			interp.variables[self.name] = var
			return var

	def __str__(self) :
		string = ''
		if self.mode == DISPLAY_DEC:
			string += str(self.val)
		elif self.mode == DISPLAY_COMMA:
			string += "{:,.2f}".format(self.val)
		elif self.mode == DISPLAY_HEX:
			string += "Ox%X" % int(self.val)
		elif self.mode == DISPLAY_OCT:
			string += "0o%o" % int(self.val)
		elif self.mode == DISPLAY_BIN:
			string = space_every(str(bin(int(self.val))))
			#string += str(bin(int(self.val)))
		elif self.mode == DISPLAY_ASCII:
			string += str(repr(chr(int(self.val))))
		string += ' ' + str(self.name) + ' = '
		if self.comment:
			string += ' ' + self.comment + '"'
		return string
	def __eq__(self, other):
		return self.val == other.val
	def __ne__(self, other):
		return self.val != other.val

	def __len__(self):
		if self.val is not None:
			return len(self.val)
		else:
			return 1

	def get_index(self, index):
		return self.val.get_index(index)

class NULL(object):
	def __init__(self, comment=''):
		self.comment = comment
	def __str__(self) :
		return 'NULL'
	def __len__(self):
		return NULL()
	def get_index(self, index):
		return NULL()

class Value(object):
	def __init__(self, val=0, comment='', mode=DISPLAY_DEC) :
		self.val = val
		self.comment = comment
		self.mode = mode
	def reassign(self, interp, val):
		return None
	def __str__(self) :

		if self.mode == DISPLAY_DEC:
			string = str(self.val)
		elif self.mode == DISPLAY_COMMA:
			string = "{:,.2f}".format(self.val)
		elif self.mode == DISPLAY_HEX:
			#string = "Ox%X" % self.val
			string = '0x{:02x}'.format(int(self.val))
		elif self.mode == DISPLAY_OCT:
			string = "0o%o" % self.val
		elif self.mode == DISPLAY_BIN:
			string = space_every(str(bin(int(self.val))))
			#string = str(bin(int(self.val)))
		elif self.mode == DISPLAY_ASCII:
			string = str(repr(chr(self.val)))

		if self.comment:
			string += ' ' + self.comment + '"'
		return string
	def __eq__(self, other):
		return self.val == other.val
	def __ne__(self, other):
		return self.val != other.val
	def __len__(self):
		return 1

	def get_index(self, index):
		if index == 0:
			return self
		else:
			raise errors.OutOfBounds("Cannot acess past '0' on scalar")


class Operator(object):
	def __init__(self, val=None, comment='') :
		self.val = val
		self.comment = comment
	def __str__(self) :

		string = str(self.val)
		return string
	def __len__(self):
		return 1

	def get_index(self, index):
		if index == 0:
			return self
		else:
			raise errors.OutOfBounds("Cannot acess past '0' on Operator")



class Variable_Placeholder(object):
	def __init__(self, val=None, comment='') :
		self.val = val
		self.comment = comment
	def __str__(self) :

		string = str(self.val)
		return string
	def __len__(self):
		return 1

	def get_index(self, index):
		if index == 0:
			return self
		else:
			raise errors.OutOfBounds("Cannot acess past '0' on Operator")


class Flow_Control(object):
	def __init__(self, val=None, comment='') :
		self.val = val
		self.comment = comment
	def __str__(self) :

		string = str(self.val)
		return string
	def __len__(self):
		return 1

	def get_index(self, index):
		if index == 0:
			return self
		else:
			raise errors.OutOfBounds("Cannot acess past '0' on Operator")


