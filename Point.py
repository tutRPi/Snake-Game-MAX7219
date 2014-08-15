#!/usr/bin/env python
# ---------------------------------------------------------
# Filename: Points.py
# ---------------------------------------------------------
# 2D Point Class with elementary functions
#
# v1.0
# F.Stern 2014
# ---------------------------------------------------------

class Point(object):
	__slots__ = ('x', 'y')  # Coordinates
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y
	def __setattr__(self, attr, value):
		object.__setattr__(self, attr, float(value))
	def __getitem__(self, index):
		return self.__getattribute__(self.__slots__[index])
	def __setitem__(self, index, value):
		self.__setattr__(self.__slots__[index], value)  # converted to float automatically by __setattr__
	def __eq__(self, other):
		return (isinstance(other, self.__class__)
			and self.x == other.x and self.y == other.y)
	def __ne__(self, other):
		return not self.__eq__(other)
	def __add__(self, other):
		if isinstance(other, self.__class__):
			return Point(self.x + other.x, self.y + other.y)
		else:
			raise TypeError('unsupported operand type(s) for +')        
	def __len__(self):
		return 2
	def __iter__(self):
		return iter([self.x, self.y])
	def __str__(self):
		return "(%f, %f)" % (self.x, self.y)
	def __repr__(self):
		return "<Point %s>" % self