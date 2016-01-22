import unittest
import rpncalc


class BasicMath(unittest.TestCase):
	def setUp(self):
		self.interp = rpncalc.Interpreter(rpncalc.ops, rpncalc.inline_break)
		self.x0 = 2
		self.x1 = 3
		self.interp.parse('%i %i' %(self.x0, self.x1))
	def test_start(self):
		self.assertEqual(self.interp.stack, [rpncalc.Value(self.x0), rpncalc.Value(self.x1)])

	def test_add(self):
		self.interp.parse('+')
		result = self.x0 + self.x1
		self.assertEqual(self.interp.stack, [rpncalc.Value(result)])

	def test_sub(self):
		self.interp.parse('-')
		result = self.x0 - self.x1
		self.assertEqual(self.interp.stack, [rpncalc.Value(result)])
	
	def test_mult(self):
		self.interp.parse('*')
		result = self.x0 * self.x1
		self.assertEqual(self.interp.stack, [rpncalc.Value(result)])

	def test_div(self):
		self.interp.parse('/')
		result = self.x0 / self.x1
		self.assertEqual(self.interp.stack, [rpncalc.Value(result)])

	def test_mod(self):
		self.interp.parse('%')
		result = self.x0 % self.x1
		self.assertEqual(self.interp.stack, [rpncalc.Value(result)])

	def test_power(self):
		self.interp.parse('^')
		result = self.x0 ** self.x1
		self.assertEqual(self.interp.stack, [rpncalc.Value(result)])
	

class BasicComparisons(unittest.TestCase):
	def setUp(self):
		self.interp = rpncalc.Interpreter(rpncalc.ops, rpncalc.inline_break)
		self.xbase = 53
		self.interp.parse(str(self.xbase))

	def test_start(self):
		self.assertEqual(self.interp.stack, [rpncalc.Value(self.xbase)])

	def test_equal_fail(self):
		self.interp.parse(str(self.xbase*2))
		self.interp.parse('==')
		self.assertEqual(self.interp.stack[-1], rpncalc.Value(0))

	def test_equal_success(self):
		self.interp.parse(str(self.xbase))
		self.interp.parse('==')
		self.assertEqual(self.interp.stack[-1], rpncalc.Value(1))

	def test_lessequal_greater_fail(self):
		self.interp.parse(str(self.xbase*2))
		self.interp.parse('<=')
		self.assertEqual(self.interp.stack[-1], rpncalc.Value(0))

	def test_lessequal_equal_success(self):
		self.interp.parse(str(self.xbase))
		self.interp.parse('<=')
		self.assertEqual(self.interp.stack[-1], rpncalc.Value(1))

	def test_lessequal_less_success(self):
		self.interp.parse(str(self.xbase / 2))
		self.interp.parse('<=')
		self.assertEqual(self.interp.stack[-1], rpncalc.Value(1))

	def test_greaterequal_greater_success(self):
		self.interp.parse(str(self.xbase*2))
		self.interp.parse('>=')
		self.assertEqual(self.interp.stack[-1], rpncalc.Value(1))

	def test_greaterequal_equal_success(self):
		self.interp.parse(str(self.xbase))
		self.interp.parse('>=')
		self.assertEqual(self.interp.stack[-1], rpncalc.Value(1))

	def test_greaterequal_less_fail(self):
		self.interp.parse(str(self.xbase / 2))
		self.interp.parse('>=')
		self.assertEqual(self.interp.stack[-1], rpncalc.Value(0))


	def test_less_greater_fail(self):
		self.interp.parse(str(self.xbase*2))
		self.interp.parse('<')
		self.assertEqual(self.interp.stack[-1], rpncalc.Value(0))

	def test_less_equal_fail(self):
		self.interp.parse(str(self.xbase))
		self.interp.parse('<')
		self.assertEqual(self.interp.stack[-1], rpncalc.Value(0))

	def test_less_less_success(self):
		self.interp.parse(str(self.xbase / 2))
		self.interp.parse('<')
		self.assertEqual(self.interp.stack[-1], rpncalc.Value(1))

	def test_greater_greater_success(self):
		self.interp.parse(str(self.xbase*2))
		self.interp.parse('>')
		self.assertEqual(self.interp.stack[-1], rpncalc.Value(1))

	def test_greater_equal_fail(self):
		self.interp.parse(str(self.xbase))
		self.interp.parse('>')
		self.assertEqual(self.interp.stack[-1], rpncalc.Value(0))

	def test_greater_less_fail(self):
		self.interp.parse(str(self.xbase / 2))
		self.interp.parse('>')
		self.assertEqual(self.interp.stack[-1], rpncalc.Value(0))

class Bulk(unittest.TestCase):
	def setUp(self):
		self.interp = rpncalc.Interpreter(rpncalc.ops, rpncalc.inline_break)

	def test_start(self):
		self.assertEqual(self.interp.stack, [])

	def check(self, test, result):
		self.interp.parse(test)
		self.assertEqual(self.interp.stack, [rpncalc.Value(result)])

	def test_one(self):
		self.interp.parse('5 1 2 + 4 * + 3 -')
		print self.interp.stack
		result = 14
		self.assertEqual(self.interp.stack, [rpncalc.Value(result)])


bulk_tests = [('5 1 2 + 4 * + 3 -', 14),
              ('3 1 2 + *', 9),
              ('4 2 5 * + 1 3 2 * + /', 2),
	      ('9 5 3 + 2 4 ^ - +', 1),
	      ('6 4 5 + * 25 2 3 + / -', 49)]

test_id = 0
for test in bulk_tests:
	test_id += 1
	setattr(Bulk, "test_" + str(test_id), lambda self: self.check(test[0], test[1]))



if __name__ == '__main__':
	unittest.main()
