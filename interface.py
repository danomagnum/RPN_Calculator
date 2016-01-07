import rpncalc
import readline
import curses
import sys

screen = curses.initscr()
screen.keypad(1)
YMAX, XMAX = screen.getmaxyx()

stackbox = curses.newwin(YMAX-5,XMAX -1,1,1)
inputbox = curses.newwin(3,XMAX -1,YMAX-5,1)
msgbox   = curses.newwin(3,XMAX -1,YMAX-3,1)


interp = rpncalc.Interpreter(rpncalc.ops)


class ShutErDownBoys(Exception):
	pass

def quit():
	raise ShutErDownBoys
def print_vars():
	pass

commands = {'quit': quit,
            'variables': print_vars}

def parse(string):
	pass

try:
	while True:
		inputbox.clear()
		inputbox.box()

		stackbox.erase()
		stackbox.box()

		msgbox.clear()
		msgbox.box()

		stack = interp.stack[:]
		if interp.function_stack is not None:
			stack += ['#'] + interp.function_stack 
		max_stack = min(len(stack), YMAX-5)
		if max_stack >= 0:
			for row in xrange(1,max_stack + 1):
				stackbox.addstr(YMAX- 6 - row, 2, str(stack[-row]))
		if interp.messages:
			msgbox.addstr(1, 2, interp.messages[0])

		screen.clear()
		inputbox.overlay(screen)
		stackbox.overlay(screen)
		msgbox.overlay(screen)
		screen.refresh()
		text_input = inputbox.getstr(1,1,38)
		if text_input[0] == ':': # interface commands start with a colon
			
			pass
		else:
			interp.parse(text_input, True)

except ShutErDownBoys:
	pass
except KeyboardInterrupt:
	pass
except:
	curses.endwin()
	raise

curses.endwin()
if len(interp.stack) > 0:
	print interp.stack[-1]
sys.exit(0)
