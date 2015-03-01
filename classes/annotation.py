class Annotation:
    def __init__(self, text):
        text = text.strip()
        if not text:
            raise Exception('Empty Annotation')
        self.text = text
    
    def __str__(self):
        return '<annotation>' + self.text + '</annotation>'

    def __eq__(self, other):
        return other.__class__ is Annotation and self.text == other.text