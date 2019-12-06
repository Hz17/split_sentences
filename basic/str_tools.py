# coding=utf-8

__all__=['text_map']



_WORD_MAP={}
"""
basic map
"""
for x in range(0x20+1):
    _WORD_MAP[chr(x)] = u' '
_WORD_MAP[chr(0x7F)] = u' '

for x in range(8198,8208):
    _WORD_MAP[chr(x)] = u' '
for x in range(8232,8240):
    _WORD_MAP[chr(x)] = u' '
for x in range(8287, 8304):
    _WORD_MAP[chr(x)] = u' '

for x in range(0xFE00, 0xFE0F + 1):
    _WORD_MAP[chr(x)] = u' '
for x in range(65281,65374+1):
    _WORD_MAP[chr(x)]=chr(x-65248)
_WORD_MAP[chr(12288)]=chr(32)

"""
special map
"""
_SPECIAL_MAP=[('“', '"'), ('”', '"'), ('、', ','),('〜', '~'), ('～', '~'), ('－', '-'), ('–', '-'),('\r\n','\n'),
    ('︳', '|'), ('▎', '|'), ('ⅰ', 'i'), ('丨', '|'), ('│', '|'), ('︱', '|'), ('｜', '|'),('／', '/'), ('\n\r', '\n'),
    (chr(173), '-'),(chr(8208), '-'),(chr(8209), '-'),(chr(8210), '-'),(chr(8211), '-'),(chr(8212), '-'),(chr(8213), '-'),
    ('【', ' '), ('】', ' '),(u'·', ' '), (u'●', ' '), (u'•', ' '), (u'→', ' '),('\xa0',' '),(u'￭', ' '),('~','-')
]
for k,v in _SPECIAL_MAP:
    _WORD_MAP[k]=v


_UNICODE_MAP=[(u'\uf0b7', ' '),('\uf0b2',''),('\uf064',''),('\uf0e0',''),('\uf06c',''),('\uf034',''),('\ue6a5',''),('\ue6a3',''),('\ue6a0',''),('\uE77C',''),('\uE76E',''),
     ('\uf077', ' '),('\ue710',''),('\ue711',''),('\ue712',''),('\ue713',''),('\ue723',''),('\ue793',''),('\uf06c', ' '),('\uf0d8', ' '), ('\uf020', ' '),('\uFEFF',''),
    ('\uF0FC',''),('\uF0FC',''),('\uE755',''),('\uE6D2',''),('\uE63C',''),('\uE734',''),('\uF074',''),('\uE622',''),('\uF241',''),('\uE71B',''),('\uF148',''),('\uE973',''),
    ('\uE96E',''),('\uE96A',''),('\uE97D',''),('\uE805',''),('\uE70D',''),('\uF258',''),('\uE7BB',''),('\uE806',''),('\uE930',''),('\uE739',''),('\uF0A4',''),('\uE6A4',''),
    ('\uE69E',''),('\uF06E',''),('\uF075',''),('\uF0B7',''),('\u009F',''),('\uF0B7',''),('\uF076',''),('\uF09F',''),('\uF0A8',''),('\uE69F',''),('\uF097',''),('\uF0A1','')
]
for k, v in _UNICODE_MAP:
    _WORD_MAP[k.encode("utf-8").decode("unicode_escape")]=v


_HTML_MAP=[('&#34;','"'),('&quot;','"'),('&#38;','&'),('&amp;','&'),('&#60;','<'),('&lt;','<'),('&#62;','>'),('&gt;','>'),
    ('&#160;',' '),('&nbsp;',' '),('&#193;','Á'),('&Aacute;','Á'),('&#194;','Â'),('&circ;','Â'),('&#195;','Ã'),('&Atilde;','Ã'),
    ('&#196;','Ä'),('&Auml','Ä'),('&#197;','Å'),('&ring;','Å'),('&#198;','Æ'),('&AElig;','Æ'),('&#199;','Ç'),('&Ccedil;','Ç'),
    ('&#200;','È'),('&Egrave;','È'),('&#201;','É'),('&Eacute;','É'),('&#202;','Ê'),('&Ecirc;','Ê'),('&#203;','Ë'),('&Euml;','Ë'),
    ('&#204;','Ì'),('&Igrave;','Ì'),('&#205;','Í'),('&Iacute;','Í'),('&#206;','Î'),('&Icirc;','Î'),('&#207;','Ï'),('&Iuml;','Ï'),
    ('&#208;','Ð'),('&ETH;','Ð'),('&#209;','Ñ'),('&Ntilde;','Ñ'),('&#210;','Ò'),('&Ograve;','Ò'),('&#211;','Ó'),('&Oacute;','Ó'),
    ('&#212;','Ô'),('&Ocirc;','Ô'),('&#213;','Õ'),('&Otilde;','Õ'),('&#214;','Ö'),('&Ouml;','Ö'),('&#215;','&times;'),
    ('&times;','&times;'),('&#216;','Ø'),('&Oslash;','Ø'),('&#217;','Ù'),('&Ugrave;','Ù'),('&#218;','Ú'),('&Uacute;','Ú'),
    ('&#219;','Û'),('&Ucirc;','Û'),('&#220;','Ü'),('&Uuml;','Ü'),('&#221;','Ý'),('&Yacute;','Ý'),('&#222;','Þ'),('&THORN;','Þ'),
    ('&#223;','ß'),('&szlig;','ß'),('&#224;','à'),('&agrave;','à'),('&#161;','?'),('&iexcl;','?'),('&#162;','￠'),('&cent;','￠'),
    ('&#163;','￡'),('&pound;','￡'),('&#164;','¤'),('&curren;','¤'),('&#165;','￥'),('&yen;','￥'),('&#166;','|'),('&brvbar;','|'),
    ('&#167;','§'),('&sect;','§'),('&#168;','¨'),('&uml;','¨'),('&#169;','©'),('&copy;','©'),('&#170;','a'),('&ordf;','a'),('&#171;','?'),
    ('&laquo;','?'),('&#172;','?'),('&not;','?'),('&#173;','/x7f'),('&shy;','/x7f'),('&#174;','®'),('&reg;','®'),('&#175;','ˉ'),
    ('&macr;','ˉ'),('&#176;','°'),('&deg;','°'),('&#177;','±'),('&plusmn;','±'),('&#178;','2'),('&sup2;','2'),('&#179;','3'),
    ('&sup3;','3'),('&#180;','′'),('&acute;','′'),('&#181;','μ'),('&micro;','μ'),('&#182;','?'),('&para;','?'),('&#183;','·'),
    ('&middot;','·'),('&#184;','?'),('&cedil;','?'),('&#185;','1'),('&sup1;','1'),('&#186;','o'),('&ordm;','o'),('&#187;','?'),
    ('&raquo;','?'),('&#188;','?'),('&frac14;','?'),('&#189;','?'),('&frac12;','?'),('&#190;','?'),('&frac34;','?'),('&#191;','?'),
    ('&iquest;','?'),('&#192;','À'),('&Agrave;','À'),('&#225;','á'),('&aacute;','á'),('&#226','â'),('&acirc;','â'),('&#227;','ã'),
    ('&atilde;','ã'),('&#228;','ä'),('&auml;','ä'),('&#229;','å'),('&aring;','å'),('&#230;','æ'),('&aelig;','æ'),('&#231;','ç'),('&ccedil;','ç'),
    ('&#232;','è'),('&egrave;','è'),('&#233;','é'),('&eacute;','é'),('&#234;','ê'),('&ecirc;','ê'),('&#235;','ë'),('&euml;','ë'),
    ('&#236;','ì'),('&igrave;','ì'),('&#237;','í'),('&iacute;','í'),('&#238;','î'),('&icirc;','î'),('&#239;','ï'),('&iuml;','ï'),
    ('&#240;','ð'),('&ieth;','ð'),('&#241;','ñ'),('&ntilde;','ñ'),('&#242;','ò'),('&ograve;','ò'),('&#243;','ó'),('&oacute;','ó'),
    ('&#244;','ô'),('&ocirc;','ô'),('&#245;','õ'),('&otilde;','õ'),('&#246;','ö'),('&ouml;','ö'),('&#247;','÷'),('&divide;','÷'),
    ('&#248;','ø'),('&oslash;','ø'),('&#249;','ù'),('&ugrave;','ù'),('&#250;','ú'),('&uacute;','ú'),('&#251;','û'),('&ucirc;','û'),
    ('&#252;','ü'),('&uuml;','ü'),('&#253;','ý'),('&yacute;','ý'),('&#254;','þ'),('&thorn;','þ'),('&#255;','ÿ'),('&yuml;','ÿ')
]
for k,v in _HTML_MAP:
    _WORD_MAP[k]=v


"""
file map
"""
import os
py_dir = os.path.split(os.path.realpath(__file__))[0]
with open(os.path.abspath(os.path.join(py_dir, 'word.map.properties')), encoding='utf-8') as fd:
    for line in fd:
        line = line.strip()
        if not line:
            continue
        lines = line.split(u"=", 1)
        if (len(lines)!=2) or (lines[0]==lines[1]):
            continue
        lines=[w.encode("utf-8").decode("unicode_escape") for w in lines]
        _WORD_MAP[lines[0].strip()] = lines[1].strip()

"""
check wordmap and fix it
"""
_TMP={}
for k, v in _WORD_MAP.items():
    if k!=v:_TMP[k]=v
    
#'\n' don't replace,\t replace 4 space empty,notice!!!!!!!!!!
if '\n' in _TMP:
    del _TMP['\n']
_TMP['\t']=' '*4

_WORD_MAP=_TMP
for k, v in _WORD_MAP.items():
    if v in _WORD_MAP:
        _WORD_MAP[k]=_WORD_MAP[v]

_MAX_K=max(len(c) for c in _WORD_MAP.keys()) 


"""
end
"""


def text_map(content):
    """
    按照最短覆盖进行进行替换，尽量替换最长的字符串
    """
    words_length = len(content)
    cut_word_list=[]
    while words_length>0:
        max_cut_length = min(words_length, _MAX_K) 
        for i in range(max_cut_length, 0, -1):
            new_word ="".join(content[words_length-i: words_length])
            if new_word in _WORD_MAP: 
                cut_word_list.append(_WORD_MAP[new_word]) 
                words_length = words_length - i 
                break
            elif i == 1:
                cut_word_list.append(new_word) 
                words_length-=1
    cut_word_list.reverse()
    return "".join(cut_word_list)
    