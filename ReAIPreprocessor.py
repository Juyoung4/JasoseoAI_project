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
        paragraphList, sentencePos_dict = self.split_sentence(text)
        preprocessedParagraphList = []
        
        for i, paragraph in enumerate(paragraphList):
            paragraphTemp = []
            for j, sentence in enumerate(paragraph):
                preprecessedSentence = self.preprocessing_Classifier(sentence[1])
                if preprecessedSentence != '':
                    paragraphTemp.append((sentence[0], preprecessedSentence))
                    
            if paragraphTemp != []:
                preprocessedParagraphList.append(paragraphTemp)
        
                
        Modelinput = []
        SentenceNumInfo = []
        for preprocessedParagraph in preprocessedParagraphList:
            for i, sentence in enumerate(preprocessedParagraph[:-1]):
                nextSentence = preprocessedParagraph[i+1]
                Modelinput.append([sentence[1], nextSentence[1]])
                SentenceNumInfo.append([sentence[0], nextSentence[0]])
                
        return Modelinput, SentenceNumInfo, sentencePos_dict
        
    def make_Recommend_input(self, text, sentence=True):
        if sentence:
            # text가 문장일 때
            textRemoveSmallBracket = self.preprocessing_Recommend(text)
            return textRemoveSmallBracket
            
        else:
            # text가 문단일 때
            textRemoveSmallBracket = self.preprocessing_Recommend(text)
            paragraphList, _ = self.split_sentence(textRemoveSmallSubject)
            ################ 구현하기 #################
            ################ 구현하기 #################
            ################ 구현하기 #################
        
        
    def preprocessing_Classifier(self, text):
        textRemoveSpecialToken = self.process_specialToken(text)
        textRemoveSmallBracket = self.process_smallBrackets(textRemoveSpecialToken)
        textRemoveSmallSubject = self.process_smallSubject(textRemoveSmallBracket)
        
        return textRemoveSmallSubject
    
    def preprocessing_Recommend(self, text):
        textRemoveSpecialToken = self.process_specialToken(text)
        textRemoveSmallBracket = self.process_smallBrackets(textRemoveSpecialToken)
        
        return textRemoveSmallBracket
    
    ######################################################################
    ############## 전처리에 필요한 기본 변수를 생성하는 함수 ##############
    ######################################################################
    
    def my_compiler(self):
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
        paragraphs = text.split('\n')
        paragraphs = [paragraph.strip() for paragraph in paragraphs if len(paragraph) > 0]

        for paragraph in paragraphs:
            for compiler in self.smallSubjectCompilers:
                paragraph = compiler.sub("", paragraph)
            textTemp.append(paragraph)


        return "\n".join(textTemp)
    
    def split_sentence(self, text):
        '''Splite sentence and paragraph
        @parm:
            text: 처리하고싶은 글
        @return
            paragraphTemp: 단락별로 (문장번호,  문장)인 2차원 배열
        '''
        # 엔터구분으로 단락 분리
        paragraphs = text.split('\n')
        paragraphs = [paragraph.strip() for paragraph in paragraphs if len(paragraph) > 0]

        # 단락별로 문장 분리
        paragraphTemp = []
        num = 0
        for paragraph in paragraphs:
            sentences = self.split_sentences(paragraph)
            sentNum = len(sentences)
            sentences = list(zip(range(num, num + sentNum), sentences))
            num += sentNum
            paragraphTemp.append(sentences)
            
        # 원본 문장에서 문장의 위치를 저장하는 사전 - 어색한 문장 검추 모델 결과의 문장 위치파악에 사용
        sentencePos_dict = {}

        cutter = 0
        for paragraph in paragraphTemp:
            for sentence in paragraph:
                startIdx = ("*"*cutter + text[cutter:]).find(sentence[1])
                endIdx = startIdx+len(sentence[1])
                sentPosIdx = (startIdx, endIdx)

                sentencePos_dict[sentence[0]] = sentPosIdx
                cutter = endIdx
            
        return paragraphTemp, sentencePos_dict