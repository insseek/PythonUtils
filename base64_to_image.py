import base64
import imghdr
import io
import os
import time
import uuid


class Base64ToImageFile(object):
    """
    将Base64字符串保存为图片
    """
    ALLOWED_FORMAT = ("jpeg", "jpg", "png", "gif")
    INVALID_FILE_MESSAGE = "Base64解码失败。"
    INVALID_FORMAT_MESSAGE = "图片格式不支持。"

    def decode_base64_str(self, base64_str: str):
        """
        解码Base64数据
        :param base64_str:
        :return:
        """
        base64_data = base64_str
        if ';base64,' in base64_str:
            header, base64_data = base64_str.split(';base64,')
        try:
            image_data = base64.b64decode(base64_data)
        except Exception as e:
            raise ValueError(f"Base64 解码失败: {str(e)}")
        return image_data

    def get_image_format(self, image_data):
        # 使用 imghdr 检测图片格式
        image_format = imghdr.what(None, image_data)
        if not image_format:
            try:
                from PIL import Image
            except ImportError:
                raise ImportError("Pillow没有安装。")
            # 尝试使用 Pillow 验证
            try:
                image = Image.open(io.BytesIO(image_data))
                image_format = image.format.lower()
            except Exception:
                raise ValueError("无法识别图片")
        return image_format

    def save_base64_to_image(self, base64_str, output_dir=None, file_name=None):
        image_data = self.decode_base64_str(base64_str)
        image_format = self.get_image_format(image_data)
        if image_format not in self.ALLOWED_FORMAT:
            raise ValueError(self.INVALID_FORMAT_MESSAGE)

        output_dir = output_dir or os.getcwd()  # 默认当前目录
        os.makedirs(output_dir, exist_ok=True)  # 确保目录存在
        if not file_name:
            # 生成唯一文件名（基于时间戳和随机数）
            file_name = f"img_{int(time.time())}_{uuid.uuid4().hex[:6]}"
        file_name = f"{file_name}.{image_format}"
        output_path = os.path.join(output_dir, file_name)

        try:
            with open(output_path, 'wb') as f:
                f.write(image_data)
        except IOError as e:
            raise IOError(f"图片保存失败: {str(e)}")
