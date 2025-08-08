import numpy as np
import cv2

from typing import Literal
from pathlib import Path
from sys import exit


def create_phantom_tank(inner: np.ndarray, outer: np.ndarray,
                        inner_light: float, outer_light: float) -> np.ndarray:
    """
    生成幻影坦克

    参数:
        inner (np.ndarray): 白色背景时看到的图像
        outer (np.ndarray): 黑色背景时看到的图像
        inner_light (float): 表图亮度调节系数
        outer_light (float): 里图亮度调节系数

    返回:
        np.ndarray: 幻影坦克图像
    """
    wgray = cv2.cvtColor(outer, cv2.COLOR_BGR2GRAY).astype(np.float32)
    bgray = cv2.cvtColor(inner, cv2.COLOR_BGR2GRAY).astype(np.float32)

    wgray = np.clip(wgray * inner_light, 0, 255)
    bgray = np.clip(bgray * outer_light, 0, 255)

    alpha = 1.0 - wgray / 255 + bgray / 255
    color = np.where(alpha > 0, bgray / alpha, 255)

    result = np.zeros((*inner.shape[:2], 4), dtype=np.uint8)
    result[:, :, :3] = np.clip(color, 0, 255)[:, :, np.newaxis]
    result[:, :, 3] = np.clip(alpha * 255, 0, 255)

    return result


def check_img_size(inner: np.ndarray, outer: np.ndarray, interp: Literal["lanczos4", "cubic", "linear", "nearest"],
                   use_outer: bool) -> tuple[np.ndarray, np.ndarray]:
    """
    检查两张图片的分辨率是否相同并统一分辨率

    参数: 
        inner (np.ndarray): 里图
        outer (np.ndarray): 表图
        interp (str): 缩放算法（仅在放大时使用）
        use_outer (bool): True表示使用outer的分辨率（调整inner），False表示使用inner的分辨率（调整outer）

    返回: 
        tuple[np.ndarray, np.ndarray]: 统一分辨率完毕的图片，第一个为里图
    """
    interp_dict = {"lanczos4": cv2.INTER_LANCZOS4, "cubic": cv2.INTER_CUBIC, "linear": cv2.INTER_LINEAR,
                   "nearest": cv2.INTER_NEAREST}

    if use_outer:
        target_height, target_width = outer.shape[:2]
        inner_height, inner_width = inner.shape[:2]

        if (inner_height, inner_width) != (target_height, target_width):
            if inner_height > target_height or inner_width > target_width:
                interpolation = cv2.INTER_AREA
            else:
                interpolation = interp_dict[interp]
            inner = cv2.resize(inner, (target_width, target_height), interpolation=interpolation)
    else:
        target_height, target_width = inner.shape[:2]
        outer_height, outer_width = outer.shape[:2]

        if (outer_height, outer_width) != (target_height, target_width):
            if outer_height > target_height or outer_width > target_width:
                interpolation = cv2.INTER_AREA
            else:
                interpolation = interp_dict[interp]
            outer = cv2.resize(outer, (target_width, target_height), interpolation=interpolation)

    return inner, outer


def read_img(path: Path) -> np.ndarray:
    """
    读取并解码一个图片
    
    参数: 
        path (pathlib.Path): 需要读取并解码的图片文件路径

    返回:
        np.ndarray: 读取并解码完毕的图片
    """
    data = path.open("rb").read()
    data = np.frombuffer(data, dtype="uint8")
    try:
        data = cv2.imdecode(data, cv2.IMREAD_COLOR)
    except Exception as error:
        print(f"解码图片{path.resolve()}时出现错误！{error}")
        exit(-1)
    return data


def save_img(path: Path, data: np.ndarray):
    file = path.open("wb")
    suffix = path.suffix

    if suffix in {".jpg", ".jpeg", ".jpe"}:
        encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), 100]
    elif suffix == ".png":
        encode_params = [int(cv2.IMWRITE_PNG_COMPRESSION), 9]
    elif suffix == ".webp":
        encode_params = [int(cv2.IMWRITE_WEBP_QUALITY), 100]
    else:
        encode_params = []

    try:
        success, img = cv2.imencode(suffix, data, encode_params)
    except Exception as error:
        print(f"编码图片时出现错误！{error}")
        exit(-1)
    if not success:
        print("编码图片时出现错误！")
        exit(-1)
    path.parent.mkdir(parents=True, exist_ok=True)
    file.write(img.tobytes())