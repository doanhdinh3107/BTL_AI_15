# path = '/video/'
path = "D:/Study/LaptrinhPython/BackendWebsite/website/static/video/"
from website.Python_NhanDienXeViPham import detect_violation
def get_image(filename):
    file = path + filename
    name = filename[:len(filename)-4]
    return detect_violation.recognize(file,name)