text="""This Gestures, like panning or scrolling, and other events can map directly to animated values using Animated.event(). This is done with a structured map syntax so that values can be extracted from complex event objects. The first level is an array to allow mapping across multiple args, and that array contains nested objects."""


class StringTree:
    def __init__(self,text):
        self.text=text
        self.children=[]
        self.parent=None

    def addChild(self,child):
        child.parent=self
        self.children.append(child)


def searchWord(word,root):
    returnList=[]
    for firstChild in root.children:  
        if  firstChild.text.lower().replace(",","").__contains__(word.lower()):
            returnList.append(firstChild)

    print(len(returnList))                
    if len(returnList) != 0:
        return returnList
    else:
        return None
                    
            

def SplitPragraphs(text):
    root=StringTree(text)
    paragraphs=text.split(".")
    for i in paragraphs:
        root.addChild(StringTree(i))
    return root



root=SplitPragraphs(text)

[print("search",child.text) for child in searchWord("This",root)]
print("cumle:",root.children[0].text)