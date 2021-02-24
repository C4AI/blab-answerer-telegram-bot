from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler, MessageHandler, Filters
import random
from os import listdir
from os.path import isfile, join

updater = Updater(token='XXXXXX', use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def poll_random_file(corpus_path):
	corpus_files = [f for f in listdir(corpus_path) if isfile(join(corpus_path, f))]
	ind = random.randint(0, len(corpus_files)-1)
	return corpus_files[ind]

def poll_random_sentence(file_path):
	sentences = []
	ind = 0
	with open(file_path, 'r') as file:
		for line in file:
			sentences.append(line)
	print(file_path, len(sentences))
	if(len(sentences) > 0):
		ind = random.randint(0, len(sentences)-1)
		return sentences[ind], ind
	else:
		return "", ind

def get_sentences(n=1):
	corpus_path = 'base/'
	sentences = []
	for i in range(n):
		file_name = poll_random_file(corpus_path)
		sentence = "Paragraph about {}\n=> ".format(file_name.split('.')[0].replace('_' , ' '))
		rnd_sentence, paragraph_ind = poll_random_sentence(corpus_path+file_name)
		sentence = sentence + rnd_sentence
		sentences.append([sentence, file_name, paragraph_ind])
	return sentences

def get_sentence():
	return get_sentences(n=1)[0]

def start(update, context):
	global ANSWERS
	global QUESTIONS
	global POLLED_SENTENCE_POS
	user = update.message.from_user
	ANSWERS[user.id] = []
	QUESTIONS[user.id] = []
	startup_texts = []
	with open('startup.txt', 'r') as startup_file:
		for line in startup_file:
			startup_texts.append(line)
	for text in startup_texts:
		context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='Markdown')
	sentence = get_sentence()
	POLLED_SENTENCE_POS[user.id] = sentence[1:]
	context.bot.send_message(chat_id=update.effective_chat.id, text=sentence[0], parse_mode='Markdown')

def poll(update, context):
	global ANSWERS
	global QUESTIONS
	global POLLED_SENTENCE_POS
	user = update.message.from_user
	ANSWERS[user.id] = []
	QUESTIONS[user.id] = []
	#n_polls = 1
	#if(len(context.args) > 0):
	#	try:
	#		n_polls = int(context.args[0])
	#	except:
	#		pass
	sentence = get_sentence()
	POLLED_SENTENCE_POS[user.id] = sentence[1:]
	print(sentence[0])
	context.bot.send_message(chat_id=update.effective_chat.id, text=sentence[0])#, parse_mode='Markdown')

def question(update, context):
	global ANSWERS
	global QUESTIONS
	global POLLED_SENTENCE_POS
	qa_path = 'qa_data/'
	user = update.message.from_user
	text = ""
	if(len(context.args) > 0):
		for word in context.args:
			text = text + str(word) + " "
		QUESTIONS[user.id].append(text)
		if len(ANSWERS[user.id]) > 0:
			to_save_question = QUESTIONS[user.id][0]
			to_save_answer = ANSWERS[user.id][0]
			ANSWERS[user.id] = ANSWERS[user.id][1:]
			QUESTIONS[user.id] = QUESTIONS[user.id][1:]
			context.bot.send_message(chat_id=update.effective_chat.id, text="Great, storing Q: {}, A: {}, File: {}, Paragraph N: {:d}.".format(to_save_question, to_save_answer, POLLED_SENTENCE_POS[user.id][0], POLLED_SENTENCE_POS[user.id][1]))
			with open(qa_path+str(user.id)+'.csv', 'a+') as file:
				file.write("[" + to_save_question + '],[' +  to_save_answer + '],' + POLLED_SENTENCE_POS[user.id][0] + ',' + str(POLLED_SENTENCE_POS[user.id][1]) + '\n')
		else:
			context.bot.send_message(chat_id=update.effective_chat.id, text="Wating for a /a (answer) entry to store.")
	else:
		context.bot.send_message(chat_id=update.effective_chat.id, text="You need to add some text to the /q statement. Ex.: /q What is your name?")

def answer(update, context):
	global ANSWERS
	global QUESTIONS
	global POLLED_SENTENCE_POS
	qa_path = 'qa_data/'
	user = update.message.from_user
	text = ""
	if(len(context.args) > 0):
		for word in context.args:
			text = text + str(word) + " "
		ANSWERS[user.id].append(text)
		if len(QUESTIONS[user.id]) > 0:
			to_save_question = QUESTIONS[user.id][0]
			to_save_answer = ANSWERS[user.id][0]
			ANSWERS[user.id] = ANSWERS[user.id][1:]
			QUESTIONS[user.id] = QUESTIONS[user.id][1:]
			context.bot.send_message(chat_id=update.effective_chat.id, text="Great, storing Q: {}, A: {}, File: {}, Paragraph N: {:d}.".format(to_save_question, to_save_answer, POLLED_SENTENCE_POS[user.id][0], POLLED_SENTENCE_POS[user.id][1]))
			with open(qa_path+str(user.id)+'.csv', 'a+') as file:
				file.write("[" + to_save_question + '],[' +  to_save_answer + '],' + POLLED_SENTENCE_POS[user.id][0] + ',' + str(POLLED_SENTENCE_POS[user.id][1]) + '\n')
		else:
			context.bot.send_message(chat_id=update.effective_chat.id, text="Wating for a /q (question) entry to store.")
	else:
		context.bot.send_message(chat_id=update.effective_chat.id, text="You need to add some text to the /a statement. Ex.: /a Yes.")

def helph(update, context):
	help_texts = []
	with open('help.txt', 'r') as help_file:
		for line in help_file:
			help_texts.append(line)
	for text in help_texts:
		context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='Markdown')

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


QUESTIONS = {}
ANSWERS = {}
POLLED_SENTENCE_POS = {}

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

help_handler = CommandHandler('help', helph)
dispatcher.add_handler(help_handler)

poll_handler = CommandHandler('poll', poll)
dispatcher.add_handler(poll_handler)

question_handler = CommandHandler('q', question, pass_args=True)
dispatcher.add_handler(question_handler)

answer_handler = CommandHandler('a', answer, pass_args=True)
dispatcher.add_handler(answer_handler)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()
