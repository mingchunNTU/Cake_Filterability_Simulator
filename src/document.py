class document():
	"""
	Module related to document manipulation
	"""
	def list_to_sentence(self,string_list):
		"""
		Comebine the list element into one sentence
		
		:param string_list: list to be combined
		:type string_list: string 
		"""
		
		output=""
		for i in range(len(string_list)):
			output=output+string_list[i]+" "
		output=output+"\n"
		return output
		
	def read_document(self,file):
		"""
		Read the document to be modified
		
		:param file: document file name
		:type file: string
		"""
		
		tmp1=open(file,'r',encoding='utf-8')
		self.document=[]
		for i in tmp1:
			self.document.append(i)
		tmp1.close()
	
	def substitute(self,string_old,string_new):
		"""
		Substitue the target string in the document with new string
		
		:param string_old: target string
		:type string_old: string
		:param string_new: new string
		:type string_new: string
		"""
		
		for i in range(len(self.document)):
			tmp1=self.document[i].split()
			for j in range(len(tmp1)):
				if tmp1[j]==string_old:
					tmp1.pop(j)
					tmp1.insert(j,string_new)
					tmp2=self.list_to_sentence(tmp1)
					self.document.pop(i)
					self.document.insert(i,tmp2)
				if tmp1[j]==("-"+string_old):
					tmp1.pop(j)
					tmp1.insert(j,("-"+string_new))
					tmp2=self.list_to_sentence(tmp1)
					self.document.pop(i)
					self.document.insert(i,tmp2) 
	def output_document(self,sentence_list,file):
		"""
		Export a list of sentence as one file
		
		:param sentence_list: list of sentence
		:type sentence_list: list
		:param file: exported file name
		:type file: string
		"""
		
		tmp1=open(file,'w',encoding='utf-8')
		tmp1.write(''.join(sentence_list))
		tmp1.close()
		
	def output_document_modified(self,file):
		"""
		Export the modified document
		:param file: exported file name
		:type file: string
		"""
		self.output_document(self.document,file)

