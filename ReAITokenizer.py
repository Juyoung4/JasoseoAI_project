from transformers import ElectraTokenizer, PreTrainedTokenizerFast

class ReAITokenizer:
    def __init__(self, 
                 CLASSIFIER_MODEL_NAME='monologg/koelectra-base-v3-discriminator',
                 CLASSIFIER_MAX_SEQ_LENGTH = 512,
                 RECOMMEND_MODEL_NAME="taeminlee/kogpt2"):
        
        # classifier tokenizer setting
        self.CLASSIFIER_MODEL_NAME = CLASSIFIER_MODEL_NAME
        self.CLASSIFIER_MAX_SEQ_LENGTH = CLASSIFIER_MAX_SEQ_LENGTH
        # Call classifier tokenizer
        self.classifier_tokenizer = ElectraTokenizer.from_pretrained(self.CLASSIFIER_MODEL_NAME)
        print("Complete Loding Classifier Model Tokenizer")
        
        # Recommend tokenizer setting
        self.RECOMMEND_MODEL_NAME = RECOMMEND_MODEL_NAME
        # Call recommend tokenizer
        self.recommend_tokenizer = PreTrainedTokenizerFast.from_pretrained(RECOMMEND_MODEL_NAME)
        print("Complete Loding Recommed Model Tokenizer")
        
        ##########
        #########
        
    def __call__(self):
        pass
    
    def classifier_encode(self, ModleInput):
        '''Encoding for Sentence classifier Model input
        '''
        encoded_dict = self.classifier_tokenizer(ModleInput,
                                 padding=True,
                                 truncation=True,
                                 max_length=self.CLASSIFIER_MAX_SEQ_LENGTH,
                                 return_tensors='tf')
        
        predict_input = (encoded_dict['input_ids'],
                         encoded_dict['attention_mask'],
                         encoded_dict['token_type_ids'])
        
        return predict_input
    
    def recommend_encode(self, ModleInput):
        '''Encoding for Sentence recommend Model input
        '''
        input_ids = self.recommend_tokenizer.encode(ModleInput, 
                                                   return_tensors='tf',
                                                   add_special_tokens=False)
    
        return input_ids
    
    def keyword_encode(self, ModleInput):
        '''Tokenize for Keyword Model
        '''
        pass

    def classifier_decode(self):
        pass
    
    def recommend_decode(self, output_idx):
        result = self.recommend_tokenizer.decode(output_idx)
        result = result.replace('<s>','').replace('</s>','')
        
        return result
    
    def keyword_decode(self):
        pass