#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   test1.py
@Time    :   2021/06/04 10:33:43
@Author  :   Wang Bohan
@Contact :   wbhan_cn@qq.com
@Desc    :   生成Dress预览图
'''

import os
from os.path import abspath, join, splitext
from math import sqrt, floor, ceil
from typing import List, Tuple
from PIL import Image
from tempfile import mkdtemp
from subprocess import call
from shutil import rmtree
from shlex import split
from socket import socket, AF_INET, SOCK_STREAM

# Constant Area
CELL_SIZE = 255
DRESS_REPO = "https://github.com/komeiji-satori/Dress.git"
DRESS_REPO_CN = "https://gitee.com/mirrors/Dress.git"


# Function Area
def china_LAN():
    try:
        me = socket(AF_INET, SOCK_STREAM)
        me.settimeout(3)
        me.connect(("www.google.com", 80))
        return False
    except:
        return True


def clone() -> str:
    tmpdir = mkdtemp()
    repo = DRESS_REPO_CN if china_LAN() else DRESS_REPO
    command = f"git clone {repo} {tmpdir}"
    call(split(command))
    return tmpdir


def extract_image_path(image_dir: str) -> List[str]:
    ret = []
    valid_suffix = [".jpg", ".jpeg", ".png", ".gif", ".webp"]
    for par, dirs, fs in os.walk(image_dir):
        for f in fs:
            if splitext(f)[-1].lower() in valid_suffix:
                ret.append(abspath(join(par, f)))
    return ret


def matrix(total) -> Tuple[int, int, int]:
    # width , length , surplus
    sq = sqrt(total)
    m = ceil(sq)
    n = floor(sq)
    return m, n, (m * n - sq)


def combine(image_dir: str, dst_img: str):
    guys = extract_image_path(image_dir)
    total = len(guys)
    m, n, surplus = matrix(total)
    canvas = Image.new("RGB", (m * CELL_SIZE, n * CELL_SIZE), (255, 255, 255))
    for i in range(m):
        for j in range(n):
            guy = guys[(n * (j - 1) + i - 1)]
            cell = Image.open(guy).resize((CELL_SIZE, CELL_SIZE))
            canvas.paste(cell, (i * CELL_SIZE, j * CELL_SIZE))
            print("正在组合", guy)
    canvas.save(dst_img)


if "__main__" == __name__:
    folder = clone()
    combine(folder, "./guys.jpg")
    rmtree(folder)