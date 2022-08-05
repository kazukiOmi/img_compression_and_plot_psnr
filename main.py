import numpy as np
import cv2
import pillow_heif
from PIL import Image
import os.path as osp
import matplotlib.pyplot as plt
import argparse
import time


def psnr(img_1, img_2, data_range=255):
    mse = np.mean((img_1.astype(float) - img_2.astype(float)) ** 2)
    return 10 * np.log10((data_range ** 2) / mse)


def imgEncodeDecode(in_img, ch, quality, ext):
    img = cv2.imread(in_img)

    if ext == "png":
        encode_param = [int(cv2.IMWRITE_PNG_COMPRESSION), quality]
        result, encimg = cv2.imencode('.png', img, encode_param)
    elif ext == "jpg":
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        result, encimg = cv2.imencode('.jpg', img, encode_param)

    decimg = cv2.imdecode(encimg, ch)

    return decimg


def bmp_to_heif(img_path):
    img = Image.open(img_path)

    q_list = [i+5 for i in range(0, 100, 10)]
    heif_file = pillow_heif.from_pillow(img)
    for i in q_list:
        heif_file.save(img_path.split(
            ".")[0]+"_q" + str(i) + ".heif", quality=i)

    org_img = cv2.imread(img_path)

    bpp_list = []
    psnr_list = []
    for i in q_list:
        cmp_img = pillow_heif.open_heif(
            img_path.split(".")[0]+"_q" + str(i) + ".heif")
        cmp_img = np.asarray(cmp_img)
        h, w, _ = cmp_img.shape
        bpp = 8 * osp.getsize(img_path.split(".")[0] +
                              "_q" + str(i) + ".heif") / (h*w)
        bpp_list.append(bpp)
        psnr_list.append(psnr(org_img, cmp_img))
    print(bpp_list)
    print(psnr_list)
    return bpp_list, psnr_list


def bmp_to_jpg(img_path):
    org_img = Image.open(img_path)

    q_list = [i+5 for i in range(0, 100, 10)]
    for i in q_list:
        org_img.save(img_path.split(
            ".")[0]+"_q" + str(i) + ".jpg", quality=i)
        # cv2.imwrite("img/Lenna_q"+str(i)+".jpg",
        #             imgEncodeDecode("./img/Lenna.bmp", 3, i, ext="jpg"))

    org_img = cv2.imread(img_path)
    bpp_list = []
    psnr_list = []
    for i in q_list:
        cmp_img = cv2.imread(img_path.split(".")[0]+"_q" + str(i) + ".jpg")
        h, w, _ = cmp_img.shape
        bpp = 8 * osp.getsize(img_path.split(".")
                              [0]+"_q" + str(i) + ".jpg") / (h*w)
        bpp_list.append(bpp)
        psnr_list.append(psnr(org_img, cmp_img))
    print(bpp_list)
    print(psnr_list)
    return bpp_list, psnr_list


def bmp_to_webp(img_path):
    org_img = Image.open(img_path)

    q_list = [i+5 for i in range(0, 100, 10)]
    for i in q_list:
        org_img.save(img_path.split(".")[0]+"_q" + str(i) + ".webp", quality=i)
        # cv2.imwrite("img/Lenna_q"+str(i)+".png",
        #             imgEncodeDecode("./img/Lenna.bmp", 3, i, ext="png"))

    org_img = cv2.imread(img_path)
    bpp_list = []
    psnr_list = []
    for i in q_list:
        cmp_img = cv2.imread(img_path.split(".")[0]+"_q" + str(i) + ".webp")
        h, w, _ = cmp_img.shape
        bpp = 8 * osp.getsize(img_path.split(".")
                              [0]+"_q" + str(i) + ".webp") / (h*w)
        bpp_list.append(bpp)
        psnr_list.append(psnr(org_img, cmp_img))
    print(bpp_list)
    print(psnr_list)
    return bpp_list, psnr_list


def bmp_to_png(img_path):
    org_img = Image.open(img_path)

    q_list = [i for i in range(10)]
    for i in q_list:
        start_time = time.time()
        for j in range(100):
            org_img.save("./img/Lenna_q" + str(i) + ".png", quality=i)
        end_time = time.time()
        print(f"quality:{i}, time:{end_time-start_time}")
        # cv2.imwrite("img/Lenna_q"+str(i)+".png",
        #             imgEncodeDecode("./img/Lenna.bmp", 3, i, ext="png"))

    # org_img = cv2.imread("./img/Lenna.bmp")
    # for i in q_list:
    #     cmp_img = cv2.imread("./img/Lenna_q" + str(i) + ".png")
    #     print(psnr(org_img, cmp_img))


def plot_psnr(org_img_path):
    heif_bpp_list, heif_psnr_list = bmp_to_heif(org_img_path)
    jpg_bpp_list, jpg_psnr_list = bmp_to_jpg(org_img_path)
    webp_bpp_list, webp_psnr_list = bmp_to_webp(org_img_path)

    plt.plot(heif_bpp_list, heif_psnr_list, label="heif")
    plt.plot(jpg_bpp_list, jpg_psnr_list, label="jpg")
    plt.plot(webp_bpp_list, webp_psnr_list, label="webp")
    plt.xlabel("bit per pixel")
    plt.ylabel("PSNR")
    plt.legend()
    plt.savefig(org_img_path.split(".")[0] + "_PSNR.pdf")


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--img_path", type=str, default="img/Lenna.bmp",
                        choices=["img/Lenna.bmp", "img/Mandrill.bmp", "img/ra0cc3d11t.TIF", "img/rbcf87a55t.TIF"])
    return parser.parse_args()


args = get_arguments()
plot_psnr(args.img_path)
# bmp_to_png(args.img_path)
