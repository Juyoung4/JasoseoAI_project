from ReAIPreprocessor import Preprocessor
from ReAITokenizer import ReAITokenizer
from ReAIModel import ReAIModel
# 전처리
pre = Preprocessor()
# 토크나이저
token = ReAITokenizer()
#모델
model = ReAIModel()

text = '캡스톤 수업에서 자동 요약 뉴스 서비스 프로젝트를 수행한 경험이 있습니다. \
    해당 프로젝트에서 seq2seq 모델을 이용한 자동 요약 해드라인 추출 구현을 맡았습니다.  \
        이에 새로운 기회가 있을 때 이를 도전하지 않았습니다. \
            저희 팀은 1등을 목표로 하였기에 좋은 성능을 지닌 모델을 개발하는 것을 목표로 삼았습니다. \
                그런데 개발 도중 전처리 과정에서 형태소 분석기를 사용하다 보니, 입력 크기가 방대해 급격한 학습 성능 및 속도 감소가 발생한다는 문제점을 발견했습니다. \
                    이를 해결하기 위해 먼저 데이터를 한 글자씩 잘라 모델 학습을 진행한 결과, 모델 정확도는 20%로 낮은 성능을 도출했습니다. \
                        그래서 다른 방ㅇ법으로 60만 개의 기사를 2만개의 크기로 나누어 형태소 분류한 후, 각 기사에서 빈도수가 높은 30만 개의 단어를 기반으로 학습했습니다. \
                            그러나 이 방법은 테스트 데이터에서 20%의 정확도로 과적합과 학습 속도가 느리다는 문제가 있었습니다. \
                                마지막으로 학부 논문들을 마지막으로 학부 논문들을 재분석하고 팀원들과 회의를 진행하여 체계적으로 설계한 데이터 전처리 과정으로 단어를 3글자까지만 잘라 모델을 훈련했습니다. \
                                    그 결과 모델의 정확도는 약 79%로 속도 면에서도 가장 좋은 결과를 도출해낼 수 있었습니다. \
                                        목표 달성을 위해서 포기하지 않고 최선을 다하여 결국 좋은 성능을 지닌 모델을 배포할 수 있었으며, 팀원 모두 맡은 파트를 완벽하게 구현함으로써 최종 시연에서 투표 결과 1등이라는 성과를 얻을 수 있었습니다.'
lastSentence = '마지막으로 학부 논문들을 재분석하고 팀원들과 회의를 진행하여 체계적으로 설계한 데이터 전처리 과정으로 단어를 3글자까지만 잘라 모델을 훈련했습니다.'

inputTextClassifier = pre.make_Classifier_input(text)
inputTextRecomend = pre.make_Recomend_input(lastSentence)

ClassifierModel_input = token.classifier_encode(inputTextClassifier)
RecomendModel_input = token.recomend_encode(inputTextRecomend)

Classifier_output = model.run_classifier(ClassifierModel_input)
Recomend_output = model.run_recomend(RecomendModel_input)


print(Classifier_output) # -> 원본문장과 매칭하는 알고리즘 구현
print(token.recomend_decode(Recomend_output))