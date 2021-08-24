import re
from kss import split_sentences

class Preprocessor:
    def __init__(self, reCompiler_dic=None, noToken_dic=None):
        '''@Parm
        reCompiler: 소문자, 소제목 제거하는 정규표현식
        noToken_dic: 버트사전에 없는 특수문자 처리하는 dictionary
        '''
        
        self.split_sentences = split_sentences
        self.reCompiler_dic = self.my_compiler()
        self.smallSubjectCompilers = self.reCompiler_dic['small_subject']
        self.bracketCompiler = self.reCompiler_dic['small_bracket']
        self.noBertToken_dic = self.my_noToken_dic()
        
    def __call__(self, text):
        pass
        
    def make_Classifier_input(self, text):
        textRemoveSmallSubject = self.preprocessing_Classifier(text)
        paragraphList = self.split_sentence(textRemoveSmallSubject)
        
        Modelinput = []
        for paragraph in paragraphList:
            for i, sentence in enumerate(paragraph[:-1]):
                nextSentence = paragraph[i+1]
                Modelinput.append([sentence, nextSentence])
                
        return Modelinput
        
    def make_Recomend_input(self, text, sentence=True):
        if sentence:
            # text가 문장일 때
            textRemoveSmallBracket = self.preprocessing_Recomend(text)
            return textRemoveSmallBracket
            
        else:
            # text가 문단일 때
            textRemoveSmallBracket = self.preprocessing_Recomend(text)
            paragraphList = self.split_sentence(textRemoveSmallSubject)
            ################ 구현하기 #################
            ################ 구현하기 #################
            ################ 구현하기 #################
        
        
    def preprocessing_Classifier(self, text):
        textRemoveSpecialToken = self.process_specialToken(text)
        textRemoveSmallBracket = self.process_smallBrackets(textRemoveSpecialToken)
        textRemoveSmallSubject = self.process_smallSubject(textRemoveSmallBracket)
        
        return textRemoveSmallSubject
    
    def preprocessing_Recomend(self, text):
        textRemoveSpecialToken = self.process_specialToken(text)
        textRemoveSmallBracket = self.process_smallBrackets(textRemoveSpecialToken)
        
        return textRemoveSmallBracket
    
    ######################################################################
    ############## 전처리에 필요한 기본 변수를 생성하는 함수 ##############
    ######################################################################
    
    def my_compiler(self):
        import re
        myCompiler_dic = {}
        # 소제목 분류하는 정규표현식
        smallSubjectCompilers = []
        smallSubjectCompilers.append(re.compile('(^▶▶[^\n(◀◀)]+◀◀$)'))
        smallSubjectCompilers.append(re.compile('(^◆[^\n(◆)]+◆$)'))
        smallSubjectCompilers.append(re.compile('(^<[^\n(>)]+>$)'))
        smallSubjectCompilers.append(re.compile('(^\'[^\n\']+\'$)'))
        smallSubjectCompilers.append(re.compile('(^\"[^\n\"]+\"$)'))
        smallSubjectCompilers.append(re.compile('(^\[[^\n\]]+\]$)'))
        smallSubjectCompilers.append(re.compile('(^“[^\n(”)]+”$)'))
        smallSubjectCompilers.append(re.compile('(^‘[^\n’]+’$)'))
        smallSubjectCompilers.append(re.compile('(^`[^\n`]+`$)'))
        
        #  소괄호 분류하는 정규표현식
        bracketCompiler = re.compile("\([^\)]*\)")
        
        myCompiler_dic['small_subject'] = smallSubjectCompilers
        myCompiler_dic['small_bracket'] = bracketCompiler
        
        return myCompiler_dic
    
    def my_noToken_dic(self):
        # 버트에서 안쓰이는 특수문자 처리
        noBertToken_dic = {}
        noBertToken_dic['⓵'] = '1'
        noBertToken_dic['♬'] = '' # 제거
        noBertToken_dic['➂'] = '3'
        noBertToken_dic['\U000f0853'] = '' # 제거
        noBertToken_dic['⓷'] = '3'
        noBertToken_dic['₃'] = '3'
        noBertToken_dic['¸'] = ''
        noBertToken_dic['Å'] = 'A'
        noBertToken_dic['♪'] = ''
        noBertToken_dic['\u200b'] = '' # 제거
        noBertToken_dic['＃'] = '#'
        noBertToken_dic['➀'] = '1'
        noBertToken_dic['➁'] = '2'
        noBertToken_dic['∞'] = '무한'
        noBertToken_dic['⓶'] = '2'
        noBertToken_dic['＇'] = ''
        noBertToken_dic['Ω'] = 'o'
        noBertToken_dic['⓸'] = '4'
        noBertToken_dic['\uf09e'] = '' # 제거
        noBertToken_dic['˙'] = '‧'
        noBertToken_dic['\U000f0852'] ='' # 제거
        noBertToken_dic['ᄁ'] = '까'
        
        return noBertToken_dic
    
    ######################################################################
    ########################### 전처리하는 함수 ##########################
    ######################################################################
    
    def process_specialToken(self, text):
        '''Delete no used token in KoELECTRA
        @parm:
            text: 처리하고싶은 글
        @return
            text: KoELECTRA에 없는 특수문자가 제거 및 변경된 글
        '''
        for specialToken in self.noBertToken_dic.keys():
            text = text.replace(specialToken, self.noBertToken_dic[specialToken])

        return text
    
    def process_smallBrackets(self, text):
        '''Delete small brackets in text
        @parm:
            text: 처리하고싶은 글
        @return
            text: 소괄호가 제거된 글
        '''
        text = self.bracketCompiler.sub('', text)

        return text
    
    def process_smallSubject(self, text):
        '''Delete small subject in text
        @parm:
            text: 처리하고싶은 글
        @return
            소제목이 제거된 글
        '''
        textTemp = [] 

        # 엔터구분으로 단락 분리
        splitedByEnter = text.split('\n')
        splitedByEnter = [sentenceByEnter.strip() for sentenceByEnter in splitedByEnter if len(sentenceByEnter) > 0]

        for paragraph in splitedByEnter:
            for compiler in self.smallSubjectCompilers:
                paragraph = compiler.sub("", paragraph)
            textTemp.append(paragraph)


        return "\n".join(textTemp)
    
    def split_sentence(self, text):
        '''Splite sentence and paragraph
        @parm:
            text: 처리하고싶은 글
        @return
            sentencesTemp: 단락별로 문장분류된 이차원 배열
        '''
        # 엔터구분으로 단락 분리
        splitedByEnter = text.split('\n')
        splitedByEnter = [sentenceByEnter.strip() for sentenceByEnter in splitedByEnter if len(sentenceByEnter) > 0]

        # 단락별로 문장 분리
        sentencesTemp = []
        for sentenceByEnter in splitedByEnter:
            sentencesTemp.append(self.split_sentences(sentenceByEnter))

        return sentencesTemp