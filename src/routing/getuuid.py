from textProcessing import processing
from sockets import websocket

# test case
textfromjune = 'hey june can you get me some cheese'
def inituuidTable():
	table = {}
	table['june'] = '12345'
	table['kevin'] = '234556'
	table['james'] = '345667'
	table['john'] = '4566789'
	return table

uuidTable = inituuidTable()

processor = processing.ProcessText()
recipientName , message = processor.getNameandMessage(textfromjune)

uuid = uuidTable[recipientName]
print(uuid)



