from website.Python_NhanDienBienSoXe import Image_test2


path = "D:/Study/LaptrinhPython/BackendWebsite/website/static/video/"
def get_result(image_list):
    plate_list = list()
    print(image_list)
    for image in image_list:
        filename = path + image
        print(filename)
        plate = list(Image_test2.xuly(filename))
        if len(plate) != 0:
            plate_list.append((image, plate[0].upper()))
        else:
            plate_list.append((image,'0'))
    print(plate_list)
    return plate_list