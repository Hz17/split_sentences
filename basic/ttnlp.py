#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Jun 6, 2019
对title与desc进行处理的基本工具
@author: enxu
'''

import basic.str_tools as str_tools
import re


def _type_char(ch):
    if not ch.strip():
        return 0
    if u'a' <= ch <= u'z' or u'A' <= ch <= u'Z' or u'0' <= ch <= u'9':
        return 1
    if u'\u4e00' <= ch <= u'\u9fbf':
        return 2
    return -1


def len_cjk(strc):
    num = 0
    pt = 0
    for ch in strc:
        t = _type_char(ch)
        if t != pt:
            if t != 0:num += 1
        else: 
            if t == 2:num += 1
        pt = t
    return num


def sub_cjk(strc, len_cjk):
    num = 0
    pt = 0
    for i, ch in enumerate(strc):
        t = _type_char(ch)
        if t != pt:
            if t != 0:num += 1
        else: 
            if t == 2:num += 1
        pt = t
        if num >= len_cjk:
            return strc[0:i + 1]
    return strc


def _basic_cut(sentence):
    result = []
    buf = []
    bt = -1
    for w in sentence:
        t = _type_char(w)
        if buf and bt != t:
            result.append("".join(buf))
            buf = []
            bt = -1
        if t == 2:
            result.append(w)
            continue
        buf.append(w)
        bt = t
        
    if buf:
        result.append("".join(buf))
    return result


SPECIAL_WORDS = set([u"c#", u".net", u"c++"])
MAX_SPECIAL_WORDS_CJKLEN = max(len_cjk(w) for w in SPECIAL_WORDS)

"""
标题切分
"""


def split_title(sentence):
    sentence = _basic_cut(str_tools.text_map(sentence).lower())
    words_length = len(sentence)
    cut_word_list = []
    while words_length > 0:
        max_cut_length = min(words_length, MAX_SPECIAL_WORDS_CJKLEN) 
        for i in range(max_cut_length, 0, -1):
            new_word = "".join(sentence[words_length - i: words_length])
            if new_word in SPECIAL_WORDS: 
                cut_word_list.append(new_word) 
                words_length = words_length - i 
                break
            elif i == 1:
                cut_word_list.append(new_word) 
                words_length -= 1
    cut_word_list.reverse()
    return cut_word_list


MIN_DESC_CJKLEN = 8
MAX_DESC_CJKLEN = 48
RE_SUB = [
    (re.compile("\d{5,}"), ""),
    (re.compile("&.{3,6};"), ""),
    (re.compile("\\\\n|<br/>|<[\\\\]?/p>"), "\n"),
    (re.compile("<[^<>]+>"), ""),
    (re.compile(u"(www|http(s)?)\s*[:,：.][\x00-\xff]+"), ""),
    (re.compile("[\n\r]+"), "\n"),
    (re.compile(u"[ \u00A0\u0020\u3000]{3,}"), "\t"),
    (re.compile(u"[ \u00A0\u0020\u3000]{1,2"), " "),
    (re.compile(u"\t+"), "\t"),
    (re.compile("\n\s+"), "\n")
]
ORDER_CHARS = re.compile(u"[\s,):.]+")
ORDER_GROUP = [
        ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "十一", "十二", "十三", "十四", "十五"],
        ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"],
        ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15"],
        ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r"],
]

SPECIL_ORDER_RE = re.compile(u"[ø▶◎★➢◆♦⚫▲■>◼ ●*]+")
PART_RE = re.compile("[;。\n]+")

S_HEAD_RE = re.compile("^([\s\-,+]+|[一二三四五六七八九十0-9a-z]{1,2}[\s,):.]+)")
S_TAIL_RE = re.compile("[\s,():.|]+$")


def _strip_ht(strs):
    m = S_HEAD_RE.search(strs)
    if m:
        strs = strs[len(m.group(0)):]
    m = S_TAIL_RE.search(strs)
    if m:
        strs = strs[:-len(m.group(0))]

    c = strs.find(":")
    if c > 2:
        head = strs[:c]
        x = len_cjk(head)
        if 1 < x and x < 8:
            strs = strs[c + 1:]
    return strs


def _part_split(strs):
    ls = []
    pre = ""
    for li in strs.split(","):
        m = len_cjk(li)
        if m >= MAX_DESC_CJKLEN:
            if pre:
                ls.append(pre)
                pre = ""
            ls.append(sub_cjk(li, MAX_DESC_CJKLEN))
            continue

        new_pre = li
        if pre:
            new_pre = pre + "," + li
        if len_cjk(new_pre) >= MAX_DESC_CJKLEN:
            if pre:
                ls.append(pre)
                pre = ""
            pre = li
            continue

        pre = new_pre

    if pre:
        ls.append(pre)
    return ls


def _order_split(strs):
    for orders in ORDER_GROUP:
        ords = []
        st = 0
        n = 0
        while n < len(orders):
            if st + 2 >= len(strs):
                break
            idx = strs.find(orders[n], st)
            if idx < st:
                break
            if idx + len(orders[n]) >= len(strs) or (not ORDER_CHARS.match(strs[idx + len(orders[n])])):
                st += 2
                continue
            ords.append(idx)
            n += 1
            st = idx + 8
        if len(ords) > 2:
            if ords[0] > 0:
                ords.insert(0, 0)
            if ords[-1] < len(strs) - 1:
                ords.append(len(strs))
            return [strs[ords[j]:ords[j + 1]] for j in range(len(ords) - 1)]
    sls = SPECIL_ORDER_RE.split(strs)
    if len(sls) > 2:
        return sls
    return [strs]


def split_desc(desc):
    desc = str_tools.text_map(desc).lower()
    for (reg, substr) in RE_SUB:
        desc, _ = reg.subn(substr, desc)
    
    new_s = []
    for w in _order_split(desc):
        new_s.extend(_order_split(w.strip()))
    desc = []
    for w in new_s:
        desc.extend(PART_RE.split(w.strip()))
    out = []
    counts = []
    for w in desc:
        w = _strip_ht(w)
        for pt in _part_split(w):
            if len_cjk(pt) >= MIN_DESC_CJKLEN:
                out.append(pt)
            else:
                out.append(pt)
                counts.append(len(out)-1)
    if len(out) <= 1 and len(counts) == 0:
        return out
    if len(out) <= 1 and len(counts) != 0:
        return []
    for i, count in enumerate(counts):
        count -= i
        if count == len(out) - 1:
            if len(out[count]) + len(out[count - 1]) <= MAX_DESC_CJKLEN:
                out[count - 1] = out[count - 1] + ',' + out[count]
                out.pop(count)
            else:
                out.pop(count)
        elif count == 0:
            if len(out[count]) + len(out[count + 1]) <= MAX_DESC_CJKLEN:
                out[count + 1] = out[count] + ',' + out[count + 1]
                out.pop(count)
            else:
                out.pop(count)
        else:
            if len(out[count - 1]) < len(out[count + 1]):
                if len(out[count - 1]) + len(out[count]) <= MAX_DESC_CJKLEN:
                    out[count - 1] = out[count - 1] + ',' + out[count]
                    out.pop(count)
                else:
                    out.pop(count)
            else:
                if len(out[count + 1]) + len(out[count]) <= MAX_DESC_CJKLEN:
                    out[count + 1] = out[count] + ',' + out[count + 1]
                    out.pop(count)
                else:
                    out.pop(count)
    return out
  
  
import os
py_dir = os.path.split(os.path.realpath(__file__))[0]
DESC_STOP = set([u" ", u"\n", u"\r", u"\t"])
with open(os.path.abspath(os.path.join(py_dir, 'desc_stopwords.txt')), encoding="utf-8") as fd:
    for line in fd:
        line = line.strip()
        if not line:
            continue
        DESC_STOP.add(line)

WORD_MAP = {",":"</s>", "/":"</s>", ":":"</s>", "|":"</s>", "-":"</s>", "(":"</s>", ")":"</s>", "\\":"</s>"}
for k in WORD_MAP.keys():
    if k in DESC_STOP:
        DESC_STOP.remove(k)
  
import numpy as np

"""
量化切好的标题
"""
def title2vec(vec_dict, title_tokens, out_title_len, min_rate=0.5):
    vecs = [0] * out_title_len
    rlen = 0
    for t in title_tokens:
        if rlen >= out_title_len:
            break
        t = WORD_MAP.get(t, t)
        v = vec_dict.embeding(t)
        if v is not None:
            vecs[rlen] = v
            rlen += 1
    if rlen * 1.0 / len(title_tokens) <= min_rate:
        return [], 0#ensure the info is fully
    return vecs, rlen

"""
量化切好的描述
"""


def desc2vec(vec_dict, desc_tokens, out_line_len, min_line_len=3):
    vsize = vec_dict.wv_size()
    vecs = []
    lens = []
    for line in desc_tokens:
        lvecs = np.zeros((out_line_len, vsize), dtype=np.float32)
        rlen = 0
        for w in line:
            if rlen > out_line_len:
                break
            w = WORD_MAP.get(w, w)
            if w in DESC_STOP:
                continue
            v = vec_dict.embeding(w)
            if v is not None:
                lvecs[rlen] = v
                rlen += 1
        if rlen >= min_line_len:
            vecs.append(lvecs)# ensure the info could use
            lens.append(rlen)
    return vecs, lens

