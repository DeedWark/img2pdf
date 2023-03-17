#!/usr/bin/env python3.11
# Description: Convert from images to PDF (because I'm out of shitty software like Adobe and all)
# Author: DeedWark <github.com/DeedWark>
# Date: 2023-02-28
# Version: 1.0.0
# Pylint score: 10/10

# HOW TO USE:
# pdf.py --images "page1.jpg,page2.jpg,page3.jpg,page4.jpg" --pdf "final.pdf"

""" System modules. """
import argparse
import sys
from PIL import Image

def arg_parser():
    """ Parse all arguments """
    parser = argparse.ArgumentParser(
            description='Images to PDF - Convert multiples images to a single PDF',
            epilog="example: {} --images \"img1.jpg,img2.png,img3.jpeg\" --pdf \"myfile.pdf\"".format(sys.argv[0]))
    parser.add_argument(
            "--images",
            type = str,
            help = "Put your images here (comma separated)",
            metavar = '<images.jpg/png>')
    parser.add_argument(
            "--pdf",
            type = str,
            help = "Name of the PDF file to create",
            metavar = '<filename.pdf>')
    args = parser.parse_args()
    if args.images is None:
        show_help()
        sys.exit(1)

    return args

def show_help():
    """ Show help """
    print(f"""\
Images to PDF - Convert multiples images to a single PDF

[Usage]: img2pdf.py [-h] [--images <images.jpg/png>] [--pdf <filename.pdf>]

[Options] 
         --images,  Put your images here (comma separated)
         --pdf,     Specify the PDF filename (Default: final.pdf)

[Example]
         {sys.argv[0]} --images \"img1.jpg,img2.jpg,img3.jpg\" --pdf \"file.pdf\"
    """)

def img_to_pdf():
    """ Convert all specified images to a single one PDF """

    # PDF File
    if arg_parser().pdf:
        pdf_file = arg_parser().pdf
    else:
        pdf_file = "final.pdf"

    # Detect all args
    raw_img_list = vars(arg_parser())

    # If --images is not empty
    if "images" in raw_img_list.keys():
        # Strip and split ' ' and ','
        raw_img_list["images"] = [image.strip() for image in raw_img_list["images"].split(",")]

        # Init list
        img_to_save = []

        # Get the first image to attach other one to it
        try:
            img_first = Image.open(raw_img_list["images"][0])
        except FileNotFoundError as err:
            print(f"ERROR ({err}) - File Not Found!")
            sys.exit(1)

        # List all images in raw images list "start at 1 (so the second one)"
        for image in raw_img_list["images"][1:]:
            # Open raw image
            img = Image.open(image)
            # Convert image to RGB
            img_converted  = img.convert('RGB')
            # Add convert imge to new list
            img_to_save.append(img_converted)

        # Attach other converted image to the first one and convert to PDF
        img_first.save(pdf_file, save_all=True, append_images=img_to_save)

def main():
    """ MAIN """
    img_to_pdf()

if __name__ == '__main__':
    main()
