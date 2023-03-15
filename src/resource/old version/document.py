
class document():
    
    def list_to_sentence(self,string_list):
        output=""
        for i in range(len(string_list)):
            output=output+string_list[i]+" "
        output=output+"\n"
        return output        
    
    def read_template(self,file):
        tmp1=open(file,'r',encoding='utf-8')
        self.file=[]
        for i in tmp1:
            self.file.append(i)
        tmp1.close()
        
        
    def substitute(self,string_old,string_new):
        for i in range(len(self.file)):
            tmp1=self.file[i].split()
            for j in range(len(tmp1)):
                if tmp1[j]==string_old:
                    tmp1.pop(j)
                    tmp1.insert(j,string_new)
                    tmp2=self.list_to_sentence(tmp1)
                    self.file.pop(i)
                    self.file.insert(i,tmp2)
                if tmp1[j]==("-"+string_old):
                   tmp1.pop(j)
                   tmp1.insert(j,("-"+string_new))
                   tmp2=self.list_to_sentence(tmp1)
                   self.file.pop(i)
                   self.file.insert(i,tmp2) 
        
    def output_document(self,file):
        tmp1=open(file,'w',encoding='utf-8')
        tmp1.write(''.join(self.file))
        tmp1.close()
                        
        
        
        
        
