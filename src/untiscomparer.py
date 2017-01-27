import os.path

src = 'hash.txt'

def hasChanges(actualHash):
    exists = os.path.isfile(src)
    hasChanges = False
    if((not exists) or _loadPreviousHash() != actualHash):
        _saveHash(actualHash)
        hasChanges = True
    return hasChanges

def _saveHash(hashToBeSaved):
    file = open(src, mode='wt', encoding='utf-8')
    file.write(hashToBeSaved)
    file.close()

def _loadPreviousHash():
    file = open(src, mode='rt', encoding='utf-8')
    previousHash = file.read()
    file.close()
    return previousHash