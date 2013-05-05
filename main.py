# -*- coding: utf8 -*-
import numpy as np, sys, os, cPickle as pickle, random
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

def make_word(messages, word, max_length):
	random.shuffle(messages)
	for time, author, body in messages:
		if len(body) > max_length:
			continue
		try:
			idx = body.decode('utf-8').index(word)
			return time, author, body, idx
		except ValueError:
			continue
	return None, None, None, None

max_length = 50
messages = load_message('var/raw.txt', 'var/msg.db')
if messages is not None:
	# stat_day(messages)
	sentence = '泪如雨下在你的发，冲化了最美的年华。'
	for word in sentence.decode('utf-8'):
		result = make_word(messages, word, max_length)
		time, author, body, idx = result
		if time is not None:
			sentence_for_word = ''.join(['  '] * (max_length-idx) + [body])
			print sentence_for_word
		else:
			print word
