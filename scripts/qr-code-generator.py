#!/usr/bin/env python3

from datetime import datetime
import qrcode

def create_qr_code_from_file(filename: str, output_path: str):
  with open(filename, 'r', encoding='utf-8') as file:
    contents = file.read()

    qr_object = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_L,
        box_size=4,
        border=1,
    )
    qr_object.add_data(contents)
    qr_object.make(fit=True)

    img = qr_object.make_image(fill_color="black", back_color="white").convert("RGBA")
    img.save(output_path)
    print(output_path)

def create_qr_code_from_string(text: str, output_path: str):
  qr = qrcode.QRCode(
      version=1,
      error_correction=qrcode.constants.ERROR_CORRECT_M,
      box_size=10,
      border=1,
  )

  qr.add_data(text)
  qr.make(fit=True)

  img = qr.make_image(fill_color="black", back_color="white")
  img.save(output_path)

  print(output_path)

if __name__ == "__main__":
  create_qr_code_from_string(
    text="https://pilateswithfilomena.com/parq",
    output_path="misc/parq.png"
  )
  create_qr_code_from_string(
    text="https://pilateswithfilomena.com",
    output_path="misc/pilateswithfilomena.png"
  )
  create_qr_code_from_file(
    filename="misc/card.vcf",
    output_path="misc/vcard.png"
  )
