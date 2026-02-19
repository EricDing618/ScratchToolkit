import json
import zipfile
import tempfile
import os
import shutil


def minify_sb3(sb3_path, json_filename='project.json'):
    """
    瘦身 .sb3 文件：将内部的 project.json 压缩为紧凑格式（去除空格和换行），
    其他文件原样保留，且尽可能保留原始 ZIP 属性（时间戳、压缩方式等）。
    返回 (原文件大小, 新文件大小) 字节数。
    """
    original_size = os.path.getsize(sb3_path)

    # 创建临时文件（自动清理）
    with tempfile.NamedTemporaryFile(delete=False, suffix='.sb3') as tmp_file:
        temp_path = tmp_file.name

    try:
        with zipfile.ZipFile(sb3_path, 'r') as orig_zip:
            with zipfile.ZipFile(temp_path, 'w', zipfile.ZIP_DEFLATED) as new_zip:
                for item in orig_zip.infolist():
                    # 读取原始数据（字节）
                    data = orig_zip.read(item.filename)

                    # 如果是目标 JSON 文件，则重新序列化为紧凑格式
                    if item.filename == json_filename:
                        # 尝试解码（常见编码为 utf-8，但也可尝试 gbk）
                        try:
                            obj = json.loads(data.decode('utf-8'))
                        except UnicodeDecodeError:
                            obj = json.loads(data.decode('gbk'))
                        # 紧凑序列化：去除空格、换行，保留非 ASCII 字符
                        minified = json.dumps(obj, separators=(',', ':'), ensure_ascii=False)
                        data = minified.encode('utf-8')

                    # 写入新 ZIP，使用原文件的 ZipInfo 以保留属性（时间戳、压缩方式等）
                    # 注意：从 orig_zip 获取完整的 ZipInfo，不要直接用 item，因为 item 可能缺少 extra 字段
                    info = orig_zip.getinfo(item.filename)
                    new_zip.writestr(info, data)

        # 用新文件替换原文件（跨盘符安全）
        shutil.move(temp_path, sb3_path)
        new_size = os.path.getsize(sb3_path)
        return original_size, new_size
    finally:
        # 清理临时文件（如果 move 失败可能还存在）
        if os.path.exists(temp_path):
            os.remove(temp_path)

def execute(fp):
    try:
        old, new = minify_sb3(fp)
        print(f"原大小: {old} 字节 ({old/1024:.2f} KB)")
        print(f"新大小: {new} 字节 ({new/1024:.2f} KB)")
        print(f"减少了: {old - new} 字节 ({(old - new)/old*100:.2f}%)")
    except FileNotFoundError:
        print("文件不存在")
    except Exception as e:
        print(f"处理出错: {e}")

if __name__=='__main__':
    execute(r'D:\gitclone\ScratchToolkit\tests\sb3files\mu.sb3')