def find_causal(arg_list, pipeline, sensitivity = None):
    arg_pairs = []
    for i in range(0, len(arg_list)-1):
        pair = {}
        pair['text'] = arg_list[i]
        pair['text_pair'] = arg_list[i+1]
        arg_pairs.append(pair)
    
    predictions = pipeline(arg_pairs)
    
    predicted_class = []
    for pred in predictions:
        pred_dic = {}
        pred_dic[pred[0]['label']] = pred[0]['score']
        pred_dic[pred[1]['label']] = pred[1]['score']
        pred_dic[pred[2]['label']] = pred[2]['score']  
        
        if sensitivity == None:
            predicted_class.append(max(pred_dic, key=pred_dic.get))
        else:
            if pred_dic['not causal'] < sensitivity:
                pred_dic.pop('not causal')
                predicted_class.append(max(pred_dic, key=pred_dic.get))
            else:
                predicted_class.append(max(pred_dic, key=pred_dic.get))
    
    sent_dict = {'reason':[], 'result':[]}
    for index, elem in enumerate(predicted_class):
        if elem == 'reason':
            sent_dict['reason'].append(index)
            sent_dict['reason'].append(index+1)
        elif elem == 'result':
            sent_dict['result'].append(index)
            sent_dict['result'].append(index+1)
            
    sent_dict['reason'] = list(set(sent_dict['reason']))
    sent_dict['result'] = list(set(sent_dict['result']))
    
    return sent_dict
