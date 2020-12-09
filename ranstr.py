from essential_generators import DocumentGenerator

gen = DocumentGenerator()

types = ['url','email','phone','word','sentence','paragraph']

def generate(type):
    if type == 'url':
        return gen.url()
    if type == 'email':
        return gen.email()
    if type == 'phone':
        return gen.phone()
    if type == 'slug':
        return gen.slug()
    if type == 'word':
        return gen.word()
    if type == 'sentence':
        return gen.sentence()
    if type == 'paragraph':
        return gen.paragraph()

