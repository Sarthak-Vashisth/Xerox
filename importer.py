import os,subprocess,pytesseract,fuzzywuzzy

from PIL import Image,ImageFilter,ImageEnhance
from send2trash import send2trash

THIS_FOLDER = os.getcwd()
INPUT_FOLDER = os.path.join(THIS_FOLDER, "img")
TMP_FOLDER = os.path.join(THIS_FOLDER, "tmp")
OUTPUT_FOLDER = os.path.join(THIS_FOLDER, "txt")


def prepare_folders():
    """
    :return: void
        Creates necessary folders
    """

    for folder in [
        INPUT_FOLDER, TMP_FOLDER, OUTPUT_FOLDER
    ]:
        if not os.path.exists(folder):
            os.makedirs(folder)


def find_images(folder):
    """
    :param folder: str
        Path to folder to search
    :return: generator of str
        List of images in folder
    """

    for file in os.listdir(folder):
        full_path = os.path.join(folder, file)
        if os.path.isfile(full_path):
            try:
                 file_name,file_extention = os.path.splitext(full_path)
                 if file_extention.upper() == ".pdf".upper():
                     _ = open(full_path)
                 else:
                     _ = Image.open(open(full_path,'rb'))  # if constructor succeeds
                 yield file
            except:
                print("Unable to open ",full_path)


def create_image_obj(input_file):
    file_name, file_extention = os.path.splitext(input_file)
    try:
        if file_extention.upper() == ".png".upper() or file_extention.upper() == ".jpg".upper():
            open_image_obj = Image.open(input_file);
            return open_image_obj;
        else:
            pass;
    except IOError:
        print("Error Opening the File..");




def rotate_and_convert_image(input_file, output_file, angle=0):
    """
    :param input_file: str
        Path to image to rotate
    :param output_file: str
        Path to output image
    :param angle: float
        Angle to rotate
    :return: void
        Rotates image and saves result
    """
    rotation_angle_clockwise = "-" + str(angle);
    file_name , file_extention = os.path.splitext(input_file)
    open_image_obj = create_image_obj(input_file);
    if file_extention.upper() == ".png".upper():
        rgb_image = open_image_obj.convert('RGB')
        rotated_img_obj = rgb_image.rotate(int(rotation_angle_clockwise));
        converted_jpg_file_name = output_file.split(".")[0] + "." + "jpg";
        rotated_img_obj.save(converted_jpg_file_name)
    elif file_extention.upper() == ".jpg".upper():
        rotated_img_obj = open_image_obj.rotate(int(rotation_angle_clockwise));
        rotated_img_obj.save(output_file)
    else:
        pass


def sharpen_image(input_file, output_file):
    """
    :param input_file: str
        Path to image to prettify
    :param output_file: str
        Path to output image
    :return: void
        Prettifies image and saves result
    """

    rotate_and_convert_image(input_file, output_file)  # rotate
    file_name, file_extention = os.path.splitext(input_file)
    if file_extention.upper() == ".pdf".upper():
        pass
    else:
        image_obj_to_sharp = create_image_obj(input_file);
        enhancer = ImageEnhance.Sharpness(image_obj_to_sharp)
        enhancer.enhance(2).save(output_file)
    #image_obj_to_sharp.filter(ImageFilter.SHARPEN);
    # cmd = "convert -auto-level -sharpen 0x4.0 -contrast "
    # cmd += "'" + output_file + "' '" + output_file + "'"
    # print("Running", cmd)
    # os.system(cmd)  # sharpen


def run_tesseract(input_file, output_file):
    """
    :param input_file: str
        Path to image to OCR
    :param output_file: str
        Path to output file
    :return: void
        Runs tesseract on image and saves result
    """

    # cmd = "tesseract -psm 2 "
    # cmd += "\"" + input_file + "\"" +" "+ "\"" + output_file + "\""
    # print("Running", cmd)
    # subprocess.call(cmd)
    # file_name, file_extention = os.path.splitext(input_file)
    # if file_extention.upper() == ".png".upper():
    str_from_img = create_image_obj(input_file);
    text = pytesseract.image_to_string(str_from_img, lang='eng');
    with open(output_file,'w') as output_file1:
        output_file1.write(text.encode('utf-8'))
    # print(text);




def main():
    prepare_folders()
    images = list(find_images(INPUT_FOLDER))
    print("Found the following images in", INPUT_FOLDER)
    print(images)

    for image in images:
        input_path = os.path.join(
            INPUT_FOLDER,
            image
        )
        if image.split(".")[1].upper() == str("png").upper():
            img_name = image.split(".")[0] + "." + "jpg";
            tmp_path = os.path.join(
                TMP_FOLDER,
                img_name
            )
        else:
            tmp_path = os.path.join(
                TMP_FOLDER,
                image
            )
        out_path = os.path.join(
            OUTPUT_FOLDER,
            image + ".out.txt"
        )

        sharpen_image(input_path, tmp_path)
        run_tesseract(tmp_path, out_path)

    print("Removing tmp folder")
    send2trash(TMP_FOLDER)


if __name__ == '__main__':
    main()
