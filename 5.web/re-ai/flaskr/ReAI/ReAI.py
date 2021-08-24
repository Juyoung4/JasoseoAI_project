from .ReAIPreprocessor import Preprocessor
from .ReAITokenizer import ReAITokenizer
from .ReAIModel import ReAIModel
import numpy as np

class ReAI:
    def __init__(self, generateNum=3):
        # 추천 문장 개수
        self.generateNum = generateNum
        
        self.Preprocessor = Preprocessor()
        self.ReAITokenizer = ReAITokenizer()
        self.ReAIModel = ReAIModel()
        
        
        pass

        
    def __call__(self, text):
        pass
    
    
    def run_ClassifierModel(self, text):
        inputTextClassifier, SentenceNumInfo, sentencePos_dict = self.Preprocessor.make_Classifier_input(text)
        ClassifierModel_input = self.ReAITokenizer.classifier_encode(inputTextClassifier)
        Classifier_output = self.ReAIModel.run_classifier(ClassifierModel_input)
        
        #  문장 번호와 결과 값 매칭
        sentState = np.hstack((SentenceNumInfo, np.array(Classifier_output).reshape(-1,1)))
        
        strong, week = self.find_awkward_sentence_position(sentState, sentencePos_dict)
        
        return strong, week
    
    
    def run_RecommendModel(self, sentence):
        inputTextRecommend = self.Preprocessor.make_Recommend_input(sentence)
        RecommendModel_input = self.ReAITokenizer.recommend_encode(inputTextRecommend)
        
        Recommend_outputs = []
        for num in range(self.generateNum):
            Recommend_outputs.append(self.ReAIModel.run_recommend(RecommendModel_input))
        
        genTexts = []
        for output in Recommend_outputs:
            genTexts.append(self.generated_sentence_cutter(output))
        
        return genTexts
    
    
    def run_KeywordModel(self):
        pass
    
    
    def find_awkward_sentence_position(self, sentenceState, sentencePos_dict):
        strong = []
        week = []
        checker = False

        for i, (first, second, state) in enumerate(sentenceState):
            if not state:
                # 이어지는 문장인지 확인
                if i+1 < len(sentenceState) and sentenceState[i+1][0] == second:
                    nextState = sentenceState[i+1][2]

                    # 다음 문장도 어색하다고 판단
                    if not nextState:
                        checker = True
                        strong.append(second)
                    else:
                        if not checker:
                            week.append(second)

                # 떨어진 문장이면 뒤에 문장가 어색한 문장
                else:
                    if not checker:
                        strong.append(second)
                    checker = False

        strongPositions = [(sentencePos_dict[sentNum][0], sentencePos_dict[sentNum][1]) for sentNum in strong]
        weekPositions = [(sentencePos_dict[sentNum][0], sentencePos_dict[sentNum][1]) for sentNum in week]

        return strongPositions, weekPositions
    
    def generated_sentence_cutter(self, encodedText):
        startFlag = False
        
        cuttedTokens = []
        for token in encodedText:
            if token == 0:
                startFlag=True
                continue
                
            if startFlag:
                cuttedTokens.append(token)
                if token == 1:
                    break
                    
        genText = self.ReAITokenizer.recommend_decode(cuttedTokens)
        return genText