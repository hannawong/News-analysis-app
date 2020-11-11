# coding = unicode

# re_funcs 含有正则表达式的内容 exclude from sonarqube

import re

punctuationPattern = r',|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+'
# '|，|。|、|；|【|】|·|！| |…|（|）|‘|’|“|”'
#  'utf-8' codec can't decode byte 0xa3 in position 1 中文逗号、中文句号、中文顿号、中文分号等 都有问题 ？？


def punc_clauseList(oriText: str):
	return re.split(punctuationPattern, oriText)

