import rpncalc
#import readline
import Tkinter as tk
import sys
import os
import math
import pkgutil
import settings

STACK = 0
GRAPH_XY = 1
GRAPH_X = 2

mode = STACK

loaded_plugins = {}
#load the plugins
def load_all_modules_from_dir(dirname):
	for importer, package_name, _ in pkgutil.iter_modules([dirname]):
		full_package_name = '%s.%s' % (dirname, package_name)
		if full_package_name not in sys.modules:
			module = importer.find_module(package_name).load_module(full_package_name)
			yield module


for module in load_all_modules_from_dir('plugins'):
	loaded_plugins.update(module.register())

function_list = rpncalc.ops.copy()
function_list.update(loaded_plugins)

if settings.allow_inline_breaks:
	interp = rpncalc.Interpreter(function_list, rpncalc.inline_break)
else:
	interp = rpncalc.Interpreter(function_list, {})


class ShutErDownBoys(Exception):
	pass

class BadPythonCommand(Exception):
	pass


history = []
history_position = 0

historyfile = open('history', 'r')
history = historyfile.readlines()

def editor_validator(keystroke):
	#raise Exception('ERRORRRRR: ' + str(keystroke))
	message = str(keystroke)
	tbox.do_command(keystroke)

def import_file(filename):
	f = open(filename)
	commands = f.read()
	f.close()
	for command in commands.split('\n'):
		if len(command) > 0:
			if command[0] == "#":
				continue
			parse(command)

def parse(input_string):
	global mode
	if input_string[0] == ':': # interface commands start with a colon
		input_string = input_string[1:]
		text = input_string.split()
		if text[0] == 'import':
			import_file(os.path.join(functions_directory, text[1]))

		elif text[0] == 'export':
			f = open(os.path.join(settings.functions_directory, text[1]), 'w+')
			commands = interp.stack[-1].stack
			for cmd in commands:
				f.write(cmd)
				f.write('\n')
			f.close()
		elif text[0] == 'quit':
			raise ShutErDownBoys()
		elif text[0] == '!':
			try:
				command = ''
				for character in input_string[1:]:
					if character == '?':
						command += str(interp.pop()[0].val)
					else:
						command += character
						
				res = eval(command)
				interp.parse(str(res))
			except Exception as e:
				raise BadPythonCommand('Bad Python Command (' + command + ') ' + e.message)
		elif text[0] == 'graph':
			if len(text) > 1:
				if text[1] == 'x':
					mode = GRAPH_X
					interp.message("X Graph Mode")
				elif text[1] == 'xy':
					mode = GRAPH_XY
					interp.message("XY Graph Mode")
			elif mode == GRAPH_XY:
				mode = GRAPH_X
				interp.message("X Graph Mode")
			else:
				mode = GRAPH_XY
				interp.message("XY Graph Mode")
		elif text[0] == 'stack':
			interp.message("Stack Mode")
			mode = STACK

	else:
		interp.parse(input_string, True)

if settings.auto_import_functions:
	for dirpath, dirnames, filenames in os.walk(settings.auto_functions_directory):
		for filename in filenames:
			import_file(os.path.join(settings.auto_functions_directory, filename))

loop = True

class Application(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.pack(fill=tk.BOTH, expand=1)
		self.createWidgets()
		self.inputbox.focus_set()
	def EnterKey(self, event):
		try:
			self.stackbox.delete(0,tk.END)
			entry_text = self.inputbox.get()
			self.inputbox.delete(0,tk.END)

			history.append(entry_text)
			history_position = 0

			parse(entry_text)
			for x in interp.stack[::-1]:
				self.stackbox.insert(0, str(x))
			self.stackbox.see(tk.END)

			for msg in interp.messages:
				self.messagebox.insert(0, str(msg))

		except ShutErDownBoys:
			loop = False
		except KeyboardInterrupt:
			input_string = input_string_pre + input_string_post
			if input_string:
				input_string_post = ''
				input_string_pre = ''
			else:
				loop = False
		except BadPythonCommand as e:
			interp.message(e.message)
		except:
			for x in rpncalc.log:
				print(x)
			raise

	def UpKey(self, event):
		global history_position
		if history_position < len(history):
			history_position += 1
			self.inputbox.delete(0,tk.END)
			self.inputbox.insert(0,str(history[-history_position][:-1]))

	def DownKey(self, event):
		global history_position
		if history_position > 1:
			history_position -= 1
			self.inputbox.delete(0,tk.END)
			self.inputbox.insert(0,str(history[-history_position][:-1]))
		elif history_position == 1:
			self.inputbox.delete(0,tk.END)

	def CtrlC(self, event):
		entry_text = self.inputbox.get()
		if entry_text:
			self.inputbox.delete(0,tk.END)
		else:
			self.quit()


	def createWidgets(self):
		self.stackframe = tk.Frame(self)
		self.stackframe.pack(fill=tk.BOTH, expand=1)

		self.stackscroll = tk.Scrollbar(self.stackframe, orient=tk.VERTICAL)

		self.stackbox = tk.Listbox(self.stackframe, yscrollcommand=self.stackscroll.set, width=30)
		self.stackscroll.config(command=self.stackbox.yview)
		self.stackscroll.pack(side=tk.RIGHT, fill=tk.Y)
		self.stackbox.pack(fill=tk.BOTH, expand=1)

		self.inputbox = tk.Entry(self)
		self.inputbox.pack(fill=tk.X, expand=0)
		self.inputbox.bind('<Return>', self.EnterKey)
		self.inputbox.bind('<KP_Enter>', self.EnterKey)
		self.inputbox.bind('<Up>', self.UpKey)
		self.inputbox.bind('<Down>', self.DownKey)
		self.inputbox.bind('<Control-c>', self.CtrlC)


		self.messageframe = tk.Frame(self)
		self.messageframe.pack(fill=tk.X, expand=0)
		self.messagescrolly = tk.Scrollbar(self.messageframe, orient=tk.VERTICAL)

		self.messagebox = tk.Listbox(self.messageframe, yscrollcommand=self.messagescrolly.set, height=3)

		self.messagescrolly.config(command=self.messagebox.yview)
		self.messagescrolly.pack(side=tk.RIGHT, fill=tk.Y)

		self.messagebox.pack(fill=tk.X, expand=0)

app = Application()
app.master.title('Python RPN Calculator')
app.mainloop()

'''
			elif event == curses.KEY_UP:
				if history_position < len(history):
					history_position += 1
					input_string_post = ''
					input_string_pre = history[-history_position]
			elif event == curses.KEY_DOWN:
				if history_position > 1:
					history_position -= 1
					input_string_post = ''
					input_string_pre = history[-history_position]
				if history_position == 1:
					input_string_post = ''
					input_string_pre = ''
'''

for v in interp.stack:
	print(v)

if settings.history > 0:
	historyfile = open('history', 'w')
	history_to_log = history
	if len(history) > settings.history:
		history_to_log = history[-settings.history:]
	for historyitem in history_to_log:
		historyfile.write(('%s\n' % historyitem.strip()))
	historyfile.close()


sys.exit(0)
