import nltk
from nltk.corpus import stopwords
import collections
import sys
import numpy as np
import wikipedia


text = None

with open('alice.txt', 'r') as f:
    text = f.read()


pure_text = text.replace('\n', ' ').replace('\t', ' ').replace('\\', ' ')



def POS(text):
    tokens = nltk.word_tokenize(text)
    for i in range(len(tokens)):
        if tokens[i].isupper():
            tokens[i] = tokens[i].lower()
    tagged = nltk.pos_tag(tokens)
    return tagged

def extractEntities(ne_chunked):
    data = {}
    for entity in ne_chunked:
        if isinstance(entity, nltk.tree.Tree):
            text = " ".join([word for word, tag in entity.leaves()])
            ent = entity.label()
            data[text] = ent
        else:
            continue
    return data

def parser(tagged_tokens, grammar):
    entity_parse = []
    grammar =  grammar
    cp = nltk.RegexpParser(grammar)
    chunked = cp.parse(tagged_tokens)
    for entity in chunked:
        for subtree in chunked.subtrees(filter=lambda t: t.label() == 'NP'):
            text = " ".join([word for word, tag in subtree.leaves()])
            entity_parse.append(text)
        return entity_parse

def wiki_search(entity_parse):
    multiple_entity = []
    for ent in entity_parse:
        try:
            search = wikipedia.summary(ent, sentences=1)
            search = search[:search.find(',')]
            search_tokens = nltk.pos_tag(nltk.word_tokenize(search))
            gram =  r"""NP: {<VBZ><DT>?<JJ>*<NN>*}"""
            pars_seach = parser(search_tokens, gram)
            if pars_seach:
                print(ent, ' - ', pars_seach[0], '\n')
        except wikipedia.exceptions.DisambiguationError as e:
            multiple_entity.append(ent)
        except wikipedia.exceptions.PageError:
            continue
        except wikipedia.exceptions.HTTPTimeoutError as e:
            continue
    print('Ambiguous Words:')
    for multi_ent in multiple_entity:
        try:
            search = wikipedia.summary(multi_ent)
        except wikipedia.exceptions.DisambiguationError as e:
            print(multi_ent, ':')
            try:
                print(e)
            except:
                continue
            print('\n')
        except wikipedia.exceptions.WikipediaException as e:
            continue
        except wikipedia.exceptions.PageError as e:
            continue

def entity_print(entity, N, all_entity):
    d = dict((x,entity.count(x)) for x in set(entity))
    s = sorted(d.items(), key=lambda x: x[1], reverse=True)
    print(N, " most common entities")
    for i in range(N):
        print(s[i][0] + ": " + str(s[i][1]))
    if all_entity:
        print('\n', "All entities: \n")
        entity_parse = sorted(set(entity))
        for ent in entity_parse:
            print('\n', ent)

tagged = POS(pure_text)

print("Select operation:")
print("1.POS")
print("2.NER_classification")
print("3.NER with custom patterns")
print("4.Wiki search with ne_chunk")
print("5.Wiki search with patterns")

# Take input from the user
choice = input("Enter choice(1/2/3/4/5):")

if choice == '1':
    print('POS selected..')
    for tag in tagged:
        print('\n', tag)
    POS_cout = [row[1] for row in tagged]
    ignore = {'.', ',', "'", '``', ':', "''"}
    POS_cout = collections.Counter(row[1] for row in tagged if row[1] not in ignore)
    print('10 most common parts')
    print(POS_cout.most_common(10))

elif choice == '2':
    print('NER classification selected..')
    print('NER with entity classification (using nltk.ne_chunk)', '\n\n')
    ne_chunked = nltk.ne_chunk(tagged, binary=False)
    ne_chunked_entity = extractEntities(ne_chunked)
    for nce in ne_chunked_entity:
        print('\n', nce, ": ", ne_chunked_entity[nce])

elif choice == '3':
    print('NER with custom patterns selected..')
    print('The rule: "NP: {<DT|PP\$>?<JJ.*>*<NNP.*>}"', '\n\n')
    grammar = "NP: {<DT|PP\$>?<JJ.*>*<NNP.*>}"
    entity_parse = parser(tagged, grammar)
    entity_print(entity_parse, 10, True)

elif choice == '4':
    print('Wiki search with ne_chunk selected..')
    print('detected entity using nltk.ne_chunk and wiki search')
    print('Ambiguous Words', '\n')
    entity_name = []
    ne_chunked = nltk.ne_chunk(tagged, binary=True)
    ne_chunked_entity = extractEntities(ne_chunked)
    for nce in ne_chunked_entity:
        entity_name.append(nce)
    wiki_search(entity_name)

elif choice == '5':
    print('Wiki search with pattern selected..')
    print('detected entity using pattern "NP: {<NNP>*}" and wiki search')
    print('Ambiguous Words', '\n')
    grammar = "NP: {<NNP>*}"
    entity_parse = parser(tagged, grammar)
    entity_print(entity_parse, 10, False)
    entity_parse = sorted(set(entity_parse))
    wiki_search(entity_parse)
else:
   print("Invalid input")


