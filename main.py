#!/usr/bin/env python3

"""
sudo apt-get install libqpdf-dev
"""

import zlib
import argparse

import pikepdf
from pikepdf import Pdf, PdfImage, Name
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import units


class PdfWatermark:
    def __init__(self, pdf_in: str, pdf_out: str, text: str):
        self.pdf_in = pdf_in
        self.pdf_out = pdf_out

        self.pdf_watermark = "wm.pdf"
        self.wm_font_size = 20
        self.wm_text = text
        self.wm_alpha = 0.2

    def apply(self):
        self._create_watermark_pdf()

        with pikepdf.open(self.pdf_in) as pdf_main:
            with pikepdf.open(self.pdf_watermark) as pdf_wm:
                for page in pdf_main.pages:
                    page.add_underlay(pdf_wm.pages[0])
            pdf_main.save(self.pdf_out)

    def _create_watermark_pdf(self):
        c = canvas.Canvas(self.pdf_watermark)
        pdfmetrics.registerFont(
            TTFont('times new roman', 'Times New Roman.ttf'))
        c.setFont('times new roman', self.wm_font_size)

        pw, ph = c._pagesize

        c.setFillGray(0.5, self.wm_alpha)
        c.saveState()
        c.translate(500, 100)
        c.rotate(45)
        c.drawCentredString(pw / 2 - 50, ph - 400, self.wm_text)
        c.restoreState()
        c.save()


def main_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="The PDF file in which will be inserted watermark"
    )
    parser.add_argument(
        "--out",
        type=str,
        required=True,
        help="The PDF file in which will be saved result"
    )
    parser.add_argument(
        "--text",
        type=str,
        required=True,
        help="The text of watermark"
    )
    args = parser.parse_args()

    srv = PdfWatermark(args.input, args.out, args.text)
    srv.apply()


if __name__ == "__main__":
    main_cli()
