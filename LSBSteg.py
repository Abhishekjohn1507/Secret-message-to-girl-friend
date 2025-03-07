#!/usr/bin/env python3
# coding: UTF-8

"""
LSBSteg.py - Least Significant Bit (LSB) Steganography

Usage:
  LSBSteg.py encode -i <input> -o <output> -f <file>
  LSBSteg.py decode -i <input> -o <output>

Options:
  -h, --help                Show this help
  --version                 Show the version
  -f,--file=<file>          File to hide
  -i,--in=<input>           Input image (carrier)
  -o,--out=<output>         Output image (or extracted file)
"""

import cv2
import docopt
import numpy as np


class SteganographyException(Exception):
    pass


class LSBSteg:
    def __init__(self, im):
        if im is None:
            raise SteganographyException("Error: Unable to load image. Check file path.")

        self.image = im
        self.height, self.width, self.nbchannels = im.shape
        self.size = self.width * self.height

        self.maskONEValues = [1, 2, 4, 8, 16, 32, 64, 128]
        self.maskONE = self.maskONEValues.pop(0)

        self.maskZEROValues = [254, 253, 251, 247, 239, 223, 191, 127]
        self.maskZERO = self.maskZEROValues.pop(0)

        self.curwidth = 0
        self.curheight = 0
        self.curchan = 0

    def put_binary_value(self, bits):
        """Embeds binary bits into the image."""
        for c in bits:
            val = list(self.image[self.curheight, self.curwidth])
            if int(c) == 1:
                val[self.curchan] = int(val[self.curchan]) | self.maskONE
            else:
                val[self.curchan] = int(val[self.curchan]) & self.maskZERO

            self.image[self.curheight, self.curwidth] = tuple(val)
            self.next_slot()

    def next_slot(self):
        """Moves to the next available bit position in the image."""
        if self.curchan == self.nbchannels - 1:
            self.curchan = 0
            if self.curwidth == self.width - 1:
                self.curwidth = 0
                if self.curheight == self.height - 1:
                    self.curheight = 0
                    if self.maskONE == 128:
                        raise SteganographyException("No available slot remaining (image filled)")
                    else:
                        self.maskONE = self.maskONEValues.pop(0)
                        self.maskZERO = self.maskZEROValues.pop(0)
                else:
                    self.curheight += 1
            else:
                self.curwidth += 1
        else:
            self.curchan += 1

    def read_bit(self):
        """Reads a single bit from the image."""
        val = self.image[self.curheight, self.curwidth][self.curchan]
        val = int(val) & self.maskONE
        self.next_slot()
        return "1" if val > 0 else "0"

    def read_bits(self, nb):
        """Reads multiple bits from the image."""
        return "".join(self.read_bit() for _ in range(nb))

    def byteValue(self, val):
        """Converts an integer value to an 8-bit binary string."""
        return self.binary_value(val, 8)

    def binary_value(self, val, bitsize):
        """Returns the binary representation of an integer."""
        binval = bin(val)[2:].zfill(bitsize)
        if len(binval) > bitsize:
            raise SteganographyException("Binary value larger than the expected size")
        return binval

    def encode_binary(self, data):
        """Encodes binary data into the image."""
        l = len(data)
        if self.width * self.height * self.nbchannels < l + 64:
            raise SteganographyException("Carrier image not big enough to hold the data")
        self.put_binary_value(self.binary_value(l, 64))
        for byte in data:
            byte = byte if isinstance(byte, int) else ord(byte)
            self.put_binary_value(self.byteValue(byte))
        return self.image

    def decode_binary(self):
        """Decodes binary data from the image."""
        l = int(self.read_bits(64), 2)
        output = bytearray(int(self.read_bits(8), 2) for _ in range(l))
        return output


def main():
    args = docopt.docopt(__doc__, version="0.2")
    in_f = args["--in"]
    out_f = args["--out"]

    # Load the input image
    in_img = cv2.imread(in_f)
    if in_img is None:
        print("Error: Could not read the input image.")
        return

    steg = LSBSteg(in_img)
    lossy_formats = {"jpeg", "jpg"}

    if args['encode']:
        # Handle lossy format conversion
        if "." in out_f:
            out_f_name, out_ext = out_f.rsplit(".", 1)
        else:
            out_f_name, out_ext = out_f, "png"

        if out_ext.lower() in lossy_formats:
            out_f = f"{out_f_name}.png"
            print("Output file changed to", out_f)

        try:
            with open(args["--file"], "rb") as f:
                data = f.read()
            res = steg.encode_binary(data)
            cv2.imwrite(out_f, res)
            print("Encoding successful! Output saved to:", out_f)
        except Exception as e:
            print("Error encoding data:", str(e))

    elif args["decode"]:
        try:
            raw = steg.decode_binary()
            with open(out_f, "wb") as f:
                f.write(raw)
            print("Decoding successful! Output saved to:", out_f)
        except Exception as e:
            print("Error decoding data:", str(e))


if __name__ == "__main__":
    main()
