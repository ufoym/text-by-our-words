# -*- coding: utf8 -*-
import numpy as np, sys, os, cPickle as pickle
from datetime import datetime

def read_message(fn):
	raw_messages = []
	with open(fn, 'r') as f:
		message = []
		for i, line in enumerate(f.readlines()):
			if i > 7:
				if line == '\n':
					if len(message) > 0:
						raw_messages.append(message)
					message = []
				else:
					message.append(line.strip())

	girl = ['我女人', '525143374','cc','lulu','你说呢？！','丫头']
	boy = ['歪厄姆','u.f.o']

	messages = []
	for message in raw_messages:
		terms = message[0].split()
		if len(terms) < 3:
			continue
		author = None
		if terms[-1] in girl:
			author = 'g'
		elif terms[-1] in boy:
			author = 'b'
		else:
			continue
		time = datetime.strptime('-'.join(terms[:2]), '%Y-%m-%d-%H:%M:%S')
		body = ' '.join(message[1:])
		messages.append((time, author, body))
	return messages


def stat_day(messages):
	import collections
	from pylab import plot_date, show
	date2num = collections.defaultdict(int)
	for time, author, body in messages:
		date2num[time.strftime('%y-%m-%d')] += 1
	dates, nums = [], []
	for k in sorted(date2num.iterkeys()):
		y, m, d = k.split('-')
		dates.append(datetime(int(y), int(m), int(d)))
		nums.append(date2num[k])

	plot_date(dates, nums, 'go')
	show()


def load_message(fn_raw, fn_msg):
	messages = None
	if os.path.exists(fn_msg):
		with open(fn_msg, 'r') as f:
			messages = pickle.load(f)
	else:
		messages = read_message(fn_raw)
		with open(fn_msg, 'w') as f:
			pickle.dump(messages, f)
	return messages

messages = load_message('var/raw.txt', 'var/msg.db')
if messages is not None:
	stat_day(messages)