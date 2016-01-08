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
inputbox.keypad(1)


interp = rpncalc.Interpreter(rpncalc.ops)


class ShutErDownBoys(Exception):
	pass


input_string_pre  = ''
input_string_post = ''
history = []
history_position = 0

inputbox.box()
stackbox.box()
msgbox.box()
inputbox.overlay(screen)
stackbox.overlay(screen)
msgbox.overlay(screen)
screen.refresh()





try:
	while True:
		inputbox.clear()
		inputbox.box()

		stackbox.erase()
		stackbox.box()

		msgbox.clear()
		msgbox.box()
		inputbox.addstr(1, 2, input_string_pre)
		inputbox.addstr(1, 2 + len(input_string_pre), input_string_post)

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


		event = inputbox.getch(1, 2 + len(input_string_pre))

		if event == 13:
			event = curses.KEY_ENTER
		if event == 10:
			event = curses.KEY_ENTER
		elif event == 8:
			event = curses.KEY_BACKSPACE
		elif event == 127:
			event = curses.KEY_DC

		if event <= 255:
			input_string_pre += chr(event)
		else:
			if event == curses.KEY_BACKSPACE:
				if len(input_string_pre) > 0:
					input_string_pre = input_string_pre[:-1]
			elif event == curses.KEY_DC:
				if len(input_string_post) > 0:
					input_string_post = input_string_post[1:]
			elif event == curses.KEY_LEFT:
				if len(input_string_pre) > 0:
					input_string_post = input_string_pre[-1] + input_string_post
					input_string_pre = input_string_pre[:-1]
			elif event == curses.KEY_RIGHT:
				if len(input_string_post) > 0:
					input_string_pre = input_string_pre + input_string_post[0]
					input_string_post = input_string_post[1:]
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
			elif event == curses.KEY_ENTER:
				input_string = input_string_pre + input_string_post
				if input_string != '':
					history.append(input_string)
					history_position = 0
					input_string_post = ''
					input_string_pre = ''

					if input_string[0] == ':': # interface commands start with a colon
						input_string = input_string[1:]
						text = input_string.split()
						if text[0] == 'import':
							f = open('functions/' + text[1])
							commands = f.read()
							f.close()
							commands = ' '.join(commands.split())
							rpncalc.log.append(commands)
							interp.parse(commands)

					else:
						interp.parse(input_string, True)


		inputbox.overlay(screen)
		stackbox.overlay(screen)
		msgbox.overlay(screen)
		screen.refresh()



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
