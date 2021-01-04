import csv
import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
import logging


def remove_special_chars(text: str) -> str:
    return ''.join(e for e in text if e.isalnum() and (e.isdigit() or e.isupper()))


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', print_end="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        print_end    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end=print_end)
    # Print New Line on Complete
    if iteration == total:
        print()


def save_image_cv2(path, name, image):
    if not os.path.exists(path):
        os.makedirs(path)
    img_path = "{}/{}.jpg".format(path, name)
    cv2.imwrite(img_path, image)
    return img_path


def save_image_plt(path, name, image):
    if not os.path.exists(path):
        os.makedirs(path)
    img_path = "{}/{}.jpg".format(path, name)
    plt.imsave(img_path,
               image,
               )
    return img_path

def init_logger():
    # global logger_name
    # logger_name = "lpr_eng"
    log_format ='%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
    filename='lpr_eng.log'
    logger_name = "lpr_eng"

    logging.basicConfig(level = logging.DEBUG,
                     format = log_format,
                     datefmt = '%m-%d %H:%M',
                     filename = 'lpr_eng.log',
                     filemode = 'w')
    logger = logging.getLogger(logger_name)
    #logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('lpr_eng.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter(log_format)
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    logging.getLogger(logger_name).info("Logger initiated (%s)" % (logger_name))
    return logger
