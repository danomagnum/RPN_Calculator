import inspect
import readline
import copy
import curses
import sys

screen = curses.initscr()
screen.keypad(1)
YMAX, XMAX = screen.getmaxyx()

stackbox = curses.newwin(YMAX-5,XMAX -1,1,1)
inputbox = curses.newwin(3,XMAX -1,YMAX-5,1)
msgbox   = curses.newwin(3,XMAX -1,YMAX-3,1)

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
	return (interp,a, b)
def assign(interp, var, val):
	var.val = val.val
	return [var]
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
def quit(interp):
	raise ShutErDownBoys()

ops = {'+': add,
       '-': sub,
       '*': mult,
       '/': div,
       '%': modulus,
       'int': convert_int,
       'float': convert_float,
       'swap': swap,
       '=': assign,
       '!': remove,
       '?': show_vars,
       'test': test,
       '\'': comment,
       'quit;': quit}

class NotEnoughOperands(Exception):
	pass

class ShutErDownBoys(Exception):
	pass

class Variable(object):
	def __init__(self, name, val=0, comment='') :
		self.name = name
		self.val = val
		self.comment = comment
	def __str__(self) :
		string = str(self.name) + ' = ' + str(self.val)
		if self.comment:
			string += '  (' + self.comment + ')'
		return string


class Value(object):
	def __init__(self, val=0, comment='') :
		self.val = val
		self.comment = comment
	def __str__(self) :
		string = str(self.val)
		if self.comment:
			string += '  (' + self.comment + ')'
		return string

class Interpreter(object):
	def __init__(self, functions=None, stack=None):
		if functions is None:
			functions = []
		self.functions = functions
		if stack is None:
			stack = []
		self.stack = stack

		self.operatorlist = self.functions.keys()
		self.operatorlist.sort( key=lambda a: len(a), reverse=True)

		self.variables = {}

		self.backup_stack = None
		self.backup_vars = None

		self.messages = []

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
		if count > len(self.stack):
			raise NotEnoughOperands
		vals = []
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
					try:
						func = self.functions[input_string]
						argcount = len(inspect.getargspec(func).args) - 1
						args = [self] + self.pop(argcount)
						result = func(*args)
						if result is not None:
							for val in result:
								self.push(val)
						return
					except KeyError:
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
						if input_string[0] not in '0123456789.':
							if input_string not in self.variables.keys():
								self.new_var(input_string)
							self.push(self.variables[input_string])
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
	

i = Interpreter(ops)

def show_stack(scr):
	pass

try:
	while True:
		inputbox.clear()
		inputbox.box()

		stackbox.erase()
		stackbox.box()

		msgbox.clear()
		msgbox.box()

		max_stack = min(len(i.stack), YMAX-5)
		if max_stack >= 0:
			for row in xrange(1,max_stack + 1):
				stackbox.addstr(YMAX- 6 - row, 2, str(i.stack[-row]))
		if i.messages:
			msgbox.addstr(1, 2, i.messages[0])

		screen.clear()
		inputbox.overlay(screen)
		stackbox.overlay(screen)
		msgbox.overlay(screen)
		screen.refresh()
		text_input = inputbox.getstr(1,1,38)
		i.parse(text_input, True)

except ShutErDownBoys:
	pass
except KeyboardInterrupt:
	pass
except:
	curses.endwin()
	raise

curses.endwin()
if len(i.stack) > 0:
	print i.stack[-1]
sys.exit(0)
