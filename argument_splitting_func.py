def is_verbal_phrase(text, nlp_model):
    doc = nlp_model(text)
    nsubj = 0
    verb_fin = 0
    for token in doc:
        if 'subj' in token.dep_ or (token.dep_=='ROOT' and token.pos_ == 'NOUN'):
            if token.morph.get('PronType'):
                if token.morph.get('PronType')[0] != 'Rel':
                    nsubj += 1
            else:
                nsubj += 1
        if token.pos_ == 'VERB' or token.pos_ == 'AUX':
            if token.morph.get('VerbForm')[0] == 'Fin':
                verb_fin += 1
    if nsubj > 0 and verb_fin > 0:
        return True
    else:
        return False

#####################################################################################################
#####################################################################################################

def remove_abbr_point(text):
    import re
    if 'Gm.b. H' in text:
        text = text.replace('Gm.b. H', 'GmbH')
    if 'Inc.' in text:
        text = text.replace('Inc.', 'Inc ')
    if 'Dr.' in text:
        text = text.replace('Dr.', 'Dr ')
    if 'No.' in text:
        text = text.replace('No.', 'No ')
    if 'Co.' in text:
        text = text.replace('Co.', 'Co ')
    if 'Corp.' in text:
        text = text.replace('Corp.', 'Corp ')
    if 'Mr.' in text:
        text = text.replace('Mr.', 'Mr ')
    if 'Mme.' in text:
        text = text.replace('Mme.', 'Mme ')
    if 'Jr.' in text:
        text = text.replace('Jr.', 'Jr ')
    
    text = re.sub(r'([A-Z])\.', r'\1 ', text)
    text = re.sub(r'([0-9])\.([0-9])', r'\1,\2 ', text)
    
    text = text.replace('  ', ' ')
        
    return text

#####################################################################################################
#####################################################################################################

def remove_list(list_):
    import re
    list_clean = []
    for elem in list_:
        if elem:
            if re.findall(r'[A-Za-z0-9]+', elem):
                list_clean.append(elem)
    return list_clean

#####################################################################################################
#####################################################################################################

def flatten(A):
    rt = []
    for i in A:
        if isinstance(i,list): rt.extend(flatten(i))
        else: rt.append(i)
    return rt

#####################################################################################################
#####################################################################################################

def split_sent_punct(text, puncts, nlp_model):
    if type(text) != list:
        sents = [text]
    else:
        sents = text
    
    for punct in puncts:
        sents_1 = []
        for sent in sents:
            if punct in sent:
                #Split over the punctuation
                sents_2 = sent.split(punct)
                
                #Add the punctuation to the end of the cut sentences
                for i in range(len(sents_2) - 1):
                    sents_2[i] = sents_2[i] + punct
                
                #Remove empty strings
                sents_2 = remove_list(sents_2)
                
                #Iteratively reconstruct verbal phrases from splits
                sents_3 = []
                tentative_sent_ = ''
                for i, sent_3 in enumerate(sents_2):
                    tentative_sent_ = (tentative_sent_ + sent_3).strip()
                    
                    if is_verbal_phrase(tentative_sent_, nlp_model):
                        sents_3.append(tentative_sent_)
                        tentative_sent_ = ''
                    elif i == (len(sents_2) - 1):
                        if len(sents_3) > 0:
                            sents_3[-1] = (sents_3[-1] + ' ' + tentative_sent_).strip()
                        else:
                            sents_3 = [tentative_sent_.strip()]
                    else:
                        continue
                        
                sents_1.append(sents_3)
                
            else:
                sents_1.append(sent)
                
        if any(isinstance(i, list) for i in sents_1):
            sents = flatten(sents_1)
        else:
            sents = sents_1
        
    return sents

#####################################################################################################
#####################################################################################################

def split_sent_connective(text, connective_patterns, nlp_model):
    import re
    if type(text) != list:
        sents = [text]
    else:
        sents = text
        
    for pattern in connective_patterns:
        sents_1 = []
        for sent in sents:
            if re.findall(pattern, sent):
                #Split over the connective pattern
                sents_2 = re.split(pattern, sent)
                
                #Remove empty strings
                sents_2 = remove_list(sents_2)

                #Iteratively reconstruct verbal phrases from splits
                sents_3 = []
                tentative_sent_ = ''
                for i, sent_3 in enumerate(sents_2):
                    tentative_sent_ = (tentative_sent_ + ' ' + sent_3).strip()
                    
                    if is_verbal_phrase(tentative_sent_, nlp_model):
                        sents_3.append(tentative_sent_)
                        tentative_sent_ = ''
                    elif i == (len(sents_2) - 1):
                        if len(sents_3) > 0:
                            sents_3[-1] = (sents_3[-1] + ' ' + tentative_sent_).strip()
                        else:
                            sents_3 = [tentative_sent_.strip()]
                    else:
                        continue
                    
                sents_1.append(sents_3)
                
            else:
                sents_1.append(sent)

        if any(isinstance(i, list) for i in sents_1):
            sents = flatten(sents_1)
        else:
            sents = sents_1

    return sents

#####################################################################################################
#####################################################################################################

def split_argument(text, punct_list, connective_patterns, nlp_model):
    text_ = remove_abbr_point(text)
    text_ = split_sent_punct(text_, punct_list, nlp_model)
    text_ = split_sent_connective(text_, connective_patterns, nlp_model)
    
    return text_

