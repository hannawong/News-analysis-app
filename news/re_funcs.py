# re_funcs 含有正则表达式的内容 exclude from sonarqube

import re


def re_finditer(pattern0, strhtml):
	return re.finditer(pattern0, strhtml)


def re_sub(pattern5, str, body):
	return  re.sub(pattern5, str, body)


fwq_url = 'http://62.234.121.168:30000'
