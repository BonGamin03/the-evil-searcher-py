#from domain.document import Document
from domain.skiplist import SkipList
#from infrastructure.document_processor import DocumentProcessor
# text="El perro corrio en dirrecion contraria para moder el gato"
# doc=Document(1,"Perro","Casa","dasdas",text)
# process=DocumentProcessor()
# lista=process.process_document(doc)
# print(lista)
    # Posting list del término "python" → doc IDs que lo contienen
sl_python = SkipList()
for doc_id in [1, 3, 5, 7, 9, 11, 20, 25, 30]:
    sl_python.insert(doc_id)

# Posting list del término "programming" → doc IDs que lo contienen
sl_programming = SkipList()
for doc_id in [2, 3, 5, 8, 11, 15, 20, 28, 30]:
    sl_programming.insert(doc_id)

print("\nPosting list 'python':")
print(sl_python)
print("\nValores:", sl_python.to_list())

print("\nPosting list 'programming':")
print(sl_programming)
print("\nValores:", sl_programming.to_list())

# Consulta AND: documentos que contienen AMBAS palabras
intersection = sl_python.intersect(sl_programming)
print("\n── Consulta AND: 'python' ∩ 'programming' ──")
print("Documentos relevantes:", intersection.to_list())
# Esperado: [3, 5, 11, 20, 30]

# Búsqueda individual
print("\n── Búsquedas individuales en 'python' ──")
for val in [5, 6, 11]:
    found = sl_python.search(sl_python.head, val)
    print(f"  search({val}) → {found}")

# Eliminación
print("\n── Eliminar doc_id=5 de 'python' ──")
 
print("Después de eliminar 5:", sl_python.to_list())

 

