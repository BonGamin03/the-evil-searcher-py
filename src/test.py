from domain.document import Document
from infrastructure.document_processor import DocumentProcessor
text="El perro corrio en dirrecion contraria para moder el gato"
doc=Document(1,"Perro","Casa","dasdas",text)
process=DocumentProcessor()
lista=process.process_document(doc)
print(lista)

