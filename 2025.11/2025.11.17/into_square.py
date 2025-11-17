import re

def patch_annotations(input_path, output_path):
    # 读入PDF原文
    with open(input_path, 'rb') as f:
        pdf = f.read()
    # 解码成字符串（严格模式下可能需更复杂的二进制处理，但一般无难度）
    text = pdf.decode("latin1") # PDF常用latin1编码

    # 替换所有 "/Subtype /Text" 为 "/Subtype /Square\n  /C [0 0 0]"
    text = re.sub(
        r'/Subtype\s*/Text\b',
        '/Subtype /Square\n  /C [0 0 0]', # 新增黑色
        text
    )

    # 写出新PDF
    with open(output_path, 'wb') as f:
        f.write(text.encode("latin1"))

if __name__ == "__main__":
    patch_annotations('114514.pdf', 'new.pdf')
    print("批量替换完成，已输出为 new.pdf")