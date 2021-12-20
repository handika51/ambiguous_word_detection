import string
import re
import fileinput
import time
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from bin.excel_process import WordDataset
import ngram

dataset = WordDataset().getListKata()
listStopword = set (stopwords.words('indonesian'))

token1 =[]

class TextProcessing:
	def __init__(self, file_location):
		
		self.data_input = []
		self.list_kalimat = []		
		# self.list_kata = []
		file = open(file_location, 'r', encoding='utf8')

		for data in file:
			list_word=[]
			self.data_input.append(data)

			#Membersihkan kalimat 
			lower_case_text = data.lower().translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
			no_number_text = re.sub(r"([^a-z\s])", "", lower_case_text)
			words = no_number_text.strip()
			list_token = word_tokenize(words)
			for token in list_token:
				if token not in listStopword:
					list_word.append(token)
					
			
			self.list_kalimat.append(list_word)
		
		
	def showList(self):
		return self.data_input

	def wordProses(self):
		proses_result = []
		ngram_result = self.ngramProses()
		
		if len(ngram_result) > 0 :
			for x in ngram_result:
				list_result = []
				for y in range(len(dataset[x[1]]['sentence'] )):
					list_word = []	
					lower_case_text = dataset[x[1]]['sentence'][y].lower().translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
					no_number_text = re.sub(r"([^a-z\s])", "", lower_case_text)
					words = no_number_text.strip()
					list_token = word_tokenize(words)
					for token in list_token:
						if token not in listStopword:
							list_word.append(token)	
					result = "{:.2%}".format(self.cosineProses(x[0],list_word))
					list_result.append(result)
				
				obj_result = {
					'id_kalimat' : x[2],
					'kata' : dataset[x[1]]['name'],
					'tipe' : dataset[x[1]]['tipe'],
					"arti" : dataset[x[1]]['sense'],
					'result': list_result
				}
				
				proses_result.append(obj_result)
				
			return proses_result		




	def ngramProses(self):
		data_ngram = []
		for kalimat in self.list_kalimat:
			for kata in kalimat:
				for data in dataset:
					similarity_result = ngram.NGram.compare(kata, data['name'], N=2)
					count = similarity_result*100
					if count>40:
						index_list = self.list_kalimat.index(kalimat)
						index_dataset = dataset.index(data)
						data_ngram.append([kalimat, index_dataset, index_list])
		return data_ngram

	def cosineProses(self, text1, text2):
		x = text1
		y = text2
		
		l1 = [] 
		l2 = []
		xy_vector = x+y
		
		# Create Vector
		for w in xy_vector:
			if w in x: l1.append(1)
			else: l1.append(0)
			if w in y: l2.append(1)
			else: l2.append(0)
		c = 0
		for i in range(len(xy_vector)):
			c += l1[i]*l2[i]
		cosine = c / float((sum(l1)*sum(l2))**0.5)
		return cosine




