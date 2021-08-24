import numpy as np
import tensorflow as tf
from transformers import TFElectraModel, TFGPT2LMHeadModel

class ReAIModel:
    def __init__(self, 
                 CLASSIFIER_MODEL_PATH='4.models/Classifier/weights.h5',
                 BERT_MODEL_NAME='monologg/koelectra-base-v3-discriminator',
                 CLASSIFIER_MAX_SEQ_LEN=512,
                 RECOMEND_MODEL_PATH='4.models/Recomend/',
                 GPT_MODEL_NAME="taeminlee/kogpt2",
                 RECOMEND_MAX_SEQ_LEN=40):
        
        # 문장 분류 모델 변수 설정.
        self.BERT_MODEL_NAME = BERT_MODEL_NAME
        self.CLASSIFIER_MODEL_PATH = CLASSIFIER_MODEL_PATH
        self.CLASSIFIER_MAX_SEQ_LEN = CLASSIFIER_MAX_SEQ_LEN
        # 문장 분류 모델 선언
        self.ClassifierModel = TFBertClassifier(model_name=self.BERT_MODEL_NAME,
                                           dir_path='bert_ckpt',
                                           num_class=2)
        # 모델 초기화 및 가중치 불러오기
        self.initial_classifierModel()
        print("Complete Loding Classifier Model")
        
        # 문장 추천 모델 설정
        self.GPT_MODEL_NAME = GPT_MODEL_NAME
        self.RECOMEND_MODEL_PATH = RECOMEND_MODEL_PATH # 모델 파일 경로
        self.RECOMEND_MAX_SEQ_LEN = RECOMEND_MAX_SEQ_LEN
        # 문장 추천 모델 선언
        self.RecomendModel = TFGPT2LMHeadModel.from_pretrained(self.RECOMEND_MODEL_PATH)
        print("Complete Loding sentenceRecomend Model")
        
    def initial_classifierModel(self):
        # inputs 와 같은 shape의 array 생성
        input_shape = np.zeros(self.CLASSIFIER_MAX_SEQ_LEN)
        shapeTemp = tf.convert_to_tensor(input_shape.reshape(-1, self.CLASSIFIER_MAX_SEQ_LEN), dtype=np.int32)
        initInputs = (shapeTemp, shapeTemp, shapeTemp)
        
        # Model 가중치 활성화
        self.ClassifierModel(initInputs)
        # Model weight 불러오기
        self.ClassifierModel.load_weights(self.CLASSIFIER_MODEL_PATH)
        
    
    def run_classifier(self, inputs):
        '''Run Sentence classifier
        '''
        result = []
        predictions = self.ClassifierModel(inputs)
        for predict in predictions:
            result.append(np.array(predict).argmax())
            
        return result
    
    def run_recomend(self, input_ids):
        '''Run sentence recomend
        '''
        output = self.RecomendModel.generate(input_ids=input_ids,
                                             max_length=self.RECOMEND_MAX_SEQ_LEN,
                                             pad_token_id=3,
                                             do_sample=True)
        
        return output[0]
    
    def run_keyword(self):
        pass
    
    def get_classifierModel(self):
        return self.ClassifierModel
    
    


class TFBertClassifier(tf.keras.Model):
    def __init__(self, model_name, dir_path, num_class):
        super(TFBertClassifier, self).__init__()
        
        self.bert = TFElectraModel.from_pretrained(model_name, cache_dir=dir_path)
        self.dropout = tf.keras.layers.Dropout(self.bert.config.hidden_dropout_prob)
        self.classifier = tf.keras.layers.Dense(num_class,
                                                kernel_initializer=tf.keras.initializers.TruncatedNormal(self.bert.config.initializer_range),
                                                name='classifier')
    
    def call(self, inputs, attention_mask=None, token_type_ids=None, training=False):
        # BERT모델 적용
        outputs = self.bert(inputs)
        
        # BERT결과 값으로 Fine tuning하기 위한 벡터로 변환
        pooled_output = outputs.last_hidden_state # [batch_size, sequence_length, hidden]
        pooled_output = pooled_output[:, 0, :]    # take <s> token (equiv. to [CLS]) [batch_size, hidden]
        
        # Fine tuning
        pooled_output = self.dropout(pooled_output, training=training)
        logits = self.classifier(pooled_output)
        
        return logits