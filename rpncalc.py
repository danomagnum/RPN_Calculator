import inspect
import copy

def add(interp, a, b):
	return [Value(a.val + b.val)]
def sub(interp, a, b):
	return [Value(a.val - b.val)]
def mult(interp, a, b):
	return [Value(a.val * b.val)]
def div(interp, a, b):
	return [Value(b.val / a.val)]
def convert_int(interp, a):
	return [Value(int(a.val))]
def convert_float(interp, a):
	return [Value(float(a))]
def modulus(interp, a,b):
	return [Value(a.val % b.val)]
def swap(interp, a,b):
	return (a, b)
def assign(interp, var, val):
	result = var.reassign(interp,val)
	if result is not None:
		return [result]
	else:
		interp.message('cannot assign')
		raise CantAssign()
		
def remove(interp, a):
	return None
def show_vars(interp):
	for value in interp.variables.itervalues():
		interp.message(str(value))
def test(interp):
	pass
def comment(interp, a, b):
	b.comment = a.name
	interp.variables.pop(a.name)
	return [b]

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
		raise CantExecute()


ops = {'+': add,
       '-': sub,
       '*': mult,
       '/': div,
       '%': modulus,
       'int': convert_int,
       'float': convert_float,
       'swap': swap,
       '=': assign,
       '`': remove,
       '?': show_vars,
       'test': test,
       '\'': comment,
       '==': equal,
       '>': greater,
       '<': less,
       '>=': gequal,
       '<=': lequal,
       '!': call}

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
		pass
	def __str__(self):
		
		if self.name is None:
			name = 'lambda'
		else:
			name = self.name
		return '#' + name + '#'

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
	def __init__(self, builtin_functions=None, stack=None, parent=None):
		if builtin_functions is None:
			builtin_functions = []

		self.builtin_functions = builtin_functions
		self.builtin_functions['{'] = self.conditional_start
		self.builtin_functions['}'] = self.conditional_end
		self.builtin_functions['#'] = self.function_def

		if stack is None:
			stack = []
		self.stack = stack

		self.operatorlist = self.builtin_functions.keys()
		self.operatorlist.sort( key=lambda a: len(a), reverse=True)

		self.variables = {}

		self.backup_stack = None
		self.backup_vars = None

		self.messages = []

		self.ignore_conds = 0

		self.function_stack = None

		self.parent = parent

	def conditional_start(self):
		if self.ignore_conds == 0:
			if self.pop()[0].val != 1:
				self.ignore_conds += 1
				self.message('Conditon False (nest level ' + str(self.ignore_conds) + ')')
			else:
				self.message('Conditon True')
		else:
			self.ignore_conds += 1
			self.message('Condition Not Evaluated (nest level ' + str(self.ignore_conds) + ')')
	

	def child_done(self, child):
		self.stack += child.stack

	def conditional_end(self):
		self.ignore_conds -= 1
		if self.ignore_conds < 0:
			self.ignore_conds = 0

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
				if count > (len(self.stack) + len(self.parent.stack)):
					raise NotEnoughOperands
				else:
					for x in xrange(len(self.stack)):
						vals.append(self.stack.pop())
					vals += self.parent.pop(count - len(self.stack) - 1)
			else:
				raise NotEnoughOperands
		else:
			for x in xrange(count):
				vals.append(self.stack.pop())
		return vals

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


	def function_def(self):
		if self.function_stack is None:
			#start recording function
			self.function_stack = []
		else:
			#finish recording function
			f = Function(stack = self.function_stack)
			self.function_stack = None
			self.push(f)

	def call(self, function):
		i = Interpreter(self.builtin_functions,parent=self)
		for x in function.stack:
			i.parse(x)
		for item in i.stack:
			if hasattr(item, 'name'):
				if item.name not in self.variables.keys():
					# was a local variable
					if type(item) is Variable:
						item = Value(item.val, item.comment)
						pass
					elif type(item) is Function:
						item.name = None # make it a lambda

			self.push(item)


	def parse(self, input_string, root = False):
		if input_string == '':
			return

		if root:
			self.backup()
			self.messages = []

		try:
			# first split the input up into multiple components if there are any and parse them in order

			if ' ' in input_string:
				for subparse in input_string.split(' '):
					self.parse(subparse)
				return
			else:
				# handle the flow control items
				for symbol in ('{', '}', '#'):
					if symbol in input_string:
						if symbol == '#':
							self.function_def()
						elif symbol == '{':
							self.conditional_start()
						elif symbol == '}':
							self.conditional_end()
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

					if not self.ignore_conds:
						self.push(Value(val))
					return
				except:
				#the input is not just a value so lets see if it is a function
					if input_string in self.operatorlist:
						if not self.ignore_conds:
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
						for funcname in self.operatorlist:
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
							self.push(self.get_var(input_string))

		except NotEnoughOperands:
			if root:
				self.message('Not Enough Operands - Stack Unchanged')
				self.restore()
				return
			else:
				raise
		except:
			if root:
				self.message('Unknown Error - Stack Unchanged')
				self.restore()
			raise

	def new_var(self, name):
		var = Variable(name)
		self.variables[name] = var
		return var
	
	def get_var(self, name):
		if name not in self.variables.keys():
			if self.parent is not None:
				if name in self.parent.variables.keys():
					return self.parent.get_var(name)
			return self.new_var(name)
		else:
			return self.variables[name]

		
