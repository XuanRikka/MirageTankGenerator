from arclet.alconna import Alconna, Args, Option, store_true, CommandMeta
import numpy as np
import cv2

from pathlib import Path
from sys import exit
import sys
import os

from utils import *

alc = Alconna(
    "MirageTankGenerator",
    Args["inner_path", str],
    Args["outer_path", str],
    Option("--inner-light", Args["inner_light", float], default=1.0, help_text="表图亮度调节系数，必须在0-1之间，默认为1.0"),
    Option("--outer-light", Args["outer_light", float], default=0.3, help_text="里图亮度调节系数，必须在0-1之间，默认为0.3"),
    Option("--output|-o", Args["output_path", str], default="./output.png",
           help_text="输出文件路径，只能为webp/png/bmp"),
    Option("--cpu-num|-c", Args["cpu_num", str], default=os.cpu_count(),
           help_text="OpenCV使用CPU多线程的核心数，设置为0则禁用多线程"),
    Option("--disable-opencl|-d-ocl", default=False, action=store_true, help_text="是否禁用OpenCV使用OpenCL"),
    Option("--interp", Args["interp", ["lanczos4", "cubic", "linear", "nearest"]], default="cubic",
           help_text="放大时使用的算法，缩小时无效，默认为cubic"),
    Option("--use-outer", default=False, action=store_true, help_text="输出的图片使用表图的分辨率，默认使用里图的分辨率"),
    CommandMeta(
        description="把两张图片合成为一张幻影坦克",
        usage="inner_path为里图路径，outer_path为表图路径",
        example="MirageTankGenerator.exe aaa.png bbb.png"
    )
)

if __name__ == "__main__":
    args = ["MirageTankGenerator"] + sys.argv[1:]
    parse = alc.parse(args)
    if not parse.matched:
        print(alc.get_help())
        exit()

    if not parse.query("disable-opencl"):
        cv2.ocl.setUseOpenCL(True)
    cv2.setNumThreads(parse.query("cpu-num").args["cpu_num"])

    inner_path = Path(parse.query("inner_path"))
    outer_path = Path(parse.query("outer_path"))

    inner_light = parse.query("inner_light")
    outer_light = parse.query("outer_light")
    if (0 > inner_light > 1) or (0 > outer_light > 1):
        print("inner-light/outer-light的数值必须是在0-1之间的浮点数")

    if not inner_path.is_file():
        print("表图文件不存在或者路径不是一个文件")
    elif not outer_path.is_file():
        print("里图文件不存在或者路径不是一个文件")

    alpha = parse.query("alpha")
    output_path = Path(parse.query("output_path"))
    if output_path.suffix not in {".webp", ".bmp", ".png"}:
        print("输出文件格式不支持")
        exit(0)

    interp = parse.query("interp")
    inner_img = read_img(inner_path)
    outer_img = read_img(outer_path)
    use_outer = parse.query("use-outer").value
    print("图片读取成功")
    inner_img, outer_img = check_img_size(inner_img, outer_img, interp, use_outer=use_outer)
    print(f"缩放成功，使用{'表图' if use_outer else '里图'}作为基准分辨率")

    img = create_phantom_tank(inner_img, outer_img, inner_light, outer_light)
    print("幻影坦克合成成功")
    save_img(output_path, img)
    print("图片已经保存至", str(output_path))
