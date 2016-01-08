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
			stack += ['['] + interp.function_stack 
		max_stack = min(len(stack), YMAX-5)
		if max_stack >= 0:
			for row in xrange(1,max_stack + 1):
				stackbox.addstr(YMAX- 6 - row, 2, str(stack[-row]))
		if interp.messages:
			msgbox.addstr(1, 2, '| '.join(interp.messages))

		screen.clear()
		inputbox.overlay(screen)
		stackbox.overlay(screen)
		msgbox.overlay(screen)
		screen.refresh()
		text_input = inputbox.getstr(1,1, XMAX - 1 )
		if text_input[0] == ':': # interface commands start with a colon
			text_input = text_input[1:]
			text = text_input.split()
			if text[0] == 'import':
				f = open('functions/' + text[1])
				commands = f.read()
				f.close()
				commands = ' '.join(commands.split())
				rpncalc.log.append(commands)
				interp.parse(commands)

		else:
			interp.parse(text_input, True)

except ShutErDownBoys:
	pass
except KeyboardInterrupt:
	pass
except:
	curses.endwin()
	for x in rpncalc.log:
		print x
	raise

curses.endwin()
if len(interp.stack) > 0:
	print interp.stack[-1]

for x in rpncalc.log:
	print x

print interp.variables['fib'].stack

sys.exit(0)
