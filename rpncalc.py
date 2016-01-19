import inspect
import copy

log = []

def add(interp, b, a):
	comment = ''
	if a.comment and b.comment:
		comment = a.comment + '+' + b.comment
	return [Value(a.val + b.val, comment)]
def sub(interp, b, a):
	comment = ''
	if a.comment and b.comment:
		comment = a.comment + '+' + b.comment
	return [Value(a.val - b.val, comment)]
def mult(interp, b, a):
	comment = ''
	if a.comment and b.comment:
		comment = a.comment + '+' + b.comment
	return [Value(a.val * b.val, comment)]
def div(interp, b, a):
	comment = ''
	if a.comment and b.comment:
		comment = a.comment + '+' + b.comment
	return [Value(a.val / b.val, comment)]
def convert_int(interp, a):
	return [Value(int(a.val))]
def convert_float(interp, a):
	return [Value(float(a))]
def modulus(interp, a,b):
	comment = ''
	if a.comment and b.comment:
		comment = a.comment + '+' + b.comment
	return [Value(a.val % b.val, comment)]
def swap(interp, a,b):
	return (a, b)
def assign(interp, var, val):
	result = var.reassign(interp,val)
	if result is not None:
		return [result]
	else:
		raise CantAssign('Cannot Do Assignment')
		
def remove(interp, a):
	return None
def show_vars(interp):
	for value in interp.variables.itervalues():
		interp.message(str(value))
def comment(interp, a, b):
	if hasattr(a, 'name'):
		b.comment = a.name
		interp.variables.pop(a.name)
		return [b]
	else:
		raise CantAssign('Cannot create comment')


def equal(interp, a, b):
	if a.val == b.val:
		return [Value(1)]
	else:
		return [Value(0)]

def lequal(interp, a, b):
	if a.val <= b.val:
		return [Value(1)]
	else:
		return [Value(0)]
def gequal(interp, a, b):
	if a.val >= b.val:
		return [Value(1)]
	else:
		return [Value(0)]
def less(interp, a, b):
	if a.val < b.val:
		return [Value(1)]
	else:
		return [Value(0)]
def greater(interp, a, b):
	if a.val > b.val:
		return [Value(1)]
	else:
		return [Value(0)]

def call(interp, a):
	if type(a) is Function:
		interp.call(a)
	else:
		raise CantExecute('Cannot Execute a Non-Function')

def condition_if(interp, b, a):
	if a.val == 1:
		if type(b) is Function:
			interp.call(b)
		else:
			return [ b ] 

def condition_ifelse(interp, c, b, a):
	if a.val == 1:
		if type(b) is Function:
			interp.call(b)
		else:
			return [ b ]
	else:
		if type(c) is Function:
			interp.call(c)
		else:
			return [ c ]

def duplicate(interp, a):
	return [a, a]

def rotate(interp, a, b, c):
	return [ b, a, c ]

def over (interp, a, b):
	return [b, a, b]

def tuck (interp, a, b):
	return [a, b, a]

def pick(interp, number):
	items = interp.pop(number.val + 1)
	items.reverse()
	return items + [items[0]]

def roll(interp, number):
	items = interp.pop(number.val + 1)
	items.reverse()
	return items[1:] + [items[0]]

def exponent(interp, b, a):
	comment = ''
	if a.comment and b.comment:
		comment = a.comment + '+' + b.comment
	return [Value(a.val ** b.val, comment)]

def size(interp):
	return [Value(interp.stacksize())]

 # default built in functions
ops = {'+': add,
       '-': sub,
       '*': mult,
       '/': div,
       '%': modulus,
       'int': convert_int,
       'float': convert_float,
       'swap': swap,
       'dup': duplicate,
       'rot': rotate,
       'over': over,
       'tuck': tuck,
       'pick': pick,
       'roll': roll,
       '=': assign,
       '`': remove,
       'drop': remove,
       '?': show_vars,
       '\'': comment,
       '==': equal,
       '>': greater,
       '<': less,
       '>=': gequal,
       '<=': lequal,
       '!': call,
       'if': condition_if,
       'ifelse': condition_ifelse,
       '^': exponent,
       'size': size}

 #functions which cannot appear in a variable name. (ex: testsize will be a variable, but test+ will beak into test and +).
inline_break = {'+': add,
                '-': sub,
                '*': mult,
                '/': div,
                '%': modulus,
                '=': assign,
                '`': remove,
                '?': show_vars,
                '\'': comment,
                '==': equal,
                '>': greater,
                '<': less,
                '>=': gequal,
                '<=': lequal,
                '!': call,
                '^': exponent}



class NotEnoughOperands(Exception):
	pass

class CantCloseBlock(Exception):
	pass

class CantAssign(Exception):
	pass

class CantExecute(Exception):
	pass

class Function(object):
	def __init__(self, name=None, stack = None, comment = ''):
		self.name = name
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
	def __str__(self):
		
		if self.name is None:
			name = 'lambda'
		else:
			name = self.name
		return '[' + name + ']'

class Variable(object):
	def __init__(self, name, val=0, comment='') :
		self.name = name
		self.val = val
		self.comment = comment
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

	def __str__(self) :
		string = str(self.name) + ' = ' + str(self.val)
		if self.comment:
			string += '  (' + self.comment + ')'
		return string

class Value(object):
	def __init__(self, val=0, comment='') :
		self.val = val
		self.comment = comment
	def reassign(self, interp, val):
		return None
	def __str__(self) :
		string = str(self.val)
		if self.comment:
			string += '  (' + self.comment + ')'
		return string

class Interpreter(object):
	def __init__(self, builtin_functions=None, inline_break_list=None, stack=None, parent=None):
		if builtin_functions is None:
			builtin_functions = {}

		self.builtin_functions = builtin_functions

		if inline_break_list is None:
			inline_break_list = {}

		self.inline_break_list = inline_break_list

		if stack is None:
			stack = []
		self.stack = stack

		self.operatorlist = self.builtin_functions.keys()
		self.operatorlist = sorted(self.operatorlist, key=lambda a: len(a), reverse=True)

		self.variables = {}

		self.backup_stack = None
		self.backup_vars = None

		self.messages = []

		self.function_stack = None
		self.function_depth = 0

		self.parent = parent

	def __str__(self):
		stackstring = ''
		for x in self.stack:
			stackstring += str(x) + '\n'
		return stackstring
	def message(self, text):
		self.messages.append(text)
	def push(self, value):
		self.stack.append(value)
	def pop(self, count = 1):
		vals = []

		if count > len(self.stack):
			if self.parent is not None:
				if count > self.stacksize():
					raise NotEnoughOperands('Not Enough Operands (Parent checked)')
				else:
					mine = len(self.stack)
					parents = count - mine
					for x in range(mine):
						vals.append(self.stack.pop())
					vals += self.parent.pop(parents)
			else:
				raise NotEnoughOperands('Not Enough Operands (No Parent)')
		else:
			for x in range(count):
				vals.append(self.stack.pop())
		return vals
	
	def stacksize(self, me_only = False):
		count = len(self.stack)
		if not me_only:
			if self.parent is not None:
				count += self.parent.stacksize()
		return count

	def backup(self):
		self.backup_stack = copy.deepcopy(self.stack)
		self.backup_vars = copy.deepcopy(self.variables)

	def backedup(self):
		if self.backup_stack is None:
			return False

		if self.backup_vars is None:
			return False

		return True

	def restore(self, clear_backups = True):
		self.stack = self.backup_stack
		self.variables = self.backup_vars

		if clear_backups:
			self.backup_stack = None
			self.backup_vars = None


	def function_start(self):
		if self.function_stack is None:
			#start recording function
			self.function_stack = []
		else:
			self.function_stack.append('[')

		self.function_depth += 1

	def function_end(self):
		self.function_depth -= 1
		
		if self.function_depth == 0:
			#finish recording function
			f = Function(stack = self.function_stack)
			self.function_stack = None
			self.push(f)
		else:
			self.function_stack.append(']')

	def call(self, function):
		i = Interpreter(self.builtin_functions,self.inline_break_list,parent=self)
		for x in function.stack:
			i.parse(x)
		for item in i.stack:
			if hasattr(item, 'name'):
				if item.name not in self.variables.keys() or item.name[0] == '$':
					# was a local variable
					if type(item) is Variable:
						item = Value(item.val, item.comment)
						pass
					elif type(item) is Function:
						item.name = None # make it a lambda

			self.push(item)


	def parse(self, input_string, root = False):
		self.message(input_string);
		if input_string == '':
			return


		if root:
			self.backup()
			self.messages = []

		try:
			# first split the input up into multiple components if there are any and parse them in order

			if '#' in input_string:
				self.parse( input_string.split('#')[0])
				return

			if ' ' in input_string:
				for subparse in input_string.split(' '):
					self.parse(subparse)
				return
			else:
				# handle the flow control items
				for symbol in ('[', ']'):
					if symbol in input_string:
						if symbol == '[':
							self.function_start()
						elif symbol == ']':
							self.function_end()
						else:
							components = input_string.split(symbol)
							if components[-1] == '':
								components = components[:-1]
							for subparse in components:
								if subparse != '':
									self.parse(subparse)
								self.parse(symbol)
						return

				if self.function_stack is not None:
					self.function_stack.append(input_string)
					return
				

				# check if the input is just a value.
				try:
					val = float(input_string)
					if val.is_integer():
						if '.' not in input_string:
							val = int(val)

					self.push(Value(val))
					return
				except:
				#the input is not just a value so lets see if it is a function
					if input_string in self.operatorlist:
						func = self.builtin_functions[input_string]
						argcount = len(inspect.getargspec(func).args) - 1
						args = [self] + self.pop(argcount)
						result = func(*args)
						if result is not None:
							for val in result:
								self.push(val)
						return



					else:
						#the input string is not just a function shorthand.
						#search through the string and see if there are any functions here.
						for funcname in self.inline_break_list:
							if funcname in input_string:
								components = input_string.split(funcname)
								if components[-1] == '':
									components = components[:-1]
								for subparse in components:
									if subparse != '':
										self.parse(subparse)
									self.parse(funcname)
								return
						#must be a variable
						if input_string[0] not in '0123456789.':
							self.message(input_string)
							self.push(self.get_var(input_string))

		except (NotEnoughOperands, CantAssign, CantCloseBlock, CantExecute) as e:
			if root:
				self.message((e.message) + ' - Stack Unchanged')
				self.restore()
				return
			else:
				raise
		except Exception as e:
			if root:
				self.message(str(e.message) + ' - Stack Unchanged')
				self.restore()
				raise
				return
			raise


	def new_var(self, name):
		var = Variable(name)
		self.variables[name] = var
		return var
	
	def get_var(self, name, create = True):
		if name not in self.variables.keys():
			if name[0] != '$':
				if self.parent is not None:
					var = self.parent.get_var(name, False)
					if var is not None:
						return var
					#if name in self.parent.variables.keys():
						#return self.parent.get_var(name)
			if create:
				return self.new_var(name)
			else:
				return None
		else:
			return self.variables[name]

		
