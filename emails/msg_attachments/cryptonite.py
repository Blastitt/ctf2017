#!/usr/bin/env python

# Copyright (c) 1999 TotallyIneptSecurity, Inc
# Author: juanvallejo
#
# Cryptonite is state-of-the-art cryptographic
# software used for encoding private GPG keys
# in a secure and safe manner that allows them
# to be sent seamlessly and carelessly over
# email messages to your local, friendly sysadmin.
#
# This program receives a <private_key> and a
# <public_key> and "obfuscates" the <private key>
# by "encrypting" it with the <public_key>.

import base64
import os.path
import sys

def print_usage():
    print ("usage: cryptonite <private_key | base64_encoded_cypher> "
          "<public_key> [--help, --decode]")


def print_help():
    print ("This program encodes and decodes private GPG keys.\n"
           "To encode a private key, specify the path to both\n"
           "the private key as well as a public key to use\n"
           "to \"encode\" the private key.\n\n"
           "To decode an already-encoded private key, simply\n"
           "provide a path to the base64-encoded cypher text, \n"
           "as well as the public key that was used to encode\n"
           "it, as well as the --decode flag with the command.")

def main():
    mode_decode = False

    for arg in sys.argv:
        if arg in ["--help", "-h"]:
            print_help()
            print "\n"
            print_usage()
            exit(0)

        if arg == "--decode":
            mode_decode = True

    # read commandline arguments
    if len(sys.argv) < 3:
        print "error: not enough arguments"
        print_usage()
        exit(1)
    
    private_key_path = sys.argv[1]
    public_key_path  = sys.argv[2]

    # ensure both files exist
    if not os.path.exists(private_key_path):
        print "error: file '{}' does not exist".format(private_key_path)
        exit(1)

    if not os.path.exists(public_key_path):
        print "error: file '{}' does not exist".format(public_key_path)
        exit(1)

    # check for empty files
    if not os.path.getsize(private_key_path):
        print "error: empty <private_key> file: '{}'".format(private_key_path)
        exit(1)

    if not os.path.getsize(public_key_path):
        print "error: empty <public_key> file: '{}'".format(public_key_path)
        exit(1)
    
    # read both files specified by the user
    try:
        f_private_key = open(private_key_path, "r")
        f_public_key  = open(public_key_path, "r")
    except IOError as e:
        print "error: cannot open file: {}".format(str(e))
        exit(1)

    # TODO: implement --decode logic
    # ensure multiple of 3 for base64 encoding to work
    max_buffer_size = 1026
    encode_buffer = ""
    while True:
        privkey_chunk = f_private_key.read(max_buffer_size)
        pubkey_chunk = f_public_key.read(max_buffer_size)

        if not privkey_chunk:
            break
        
        if not pubkey_chunk:
            # keep re-reading pubkey file until both privkey
            # and pubkey files have been read in their entirety.
            # This is needed since we only care to read the
            # privkey file in its entirety; wrapping it with
            # the pubkey file more than once if necessary.
            f_public_key.seek(0)
            pubkey_chunk = f_public_key.read(max_buffer_size)
        
        must_encode = privkey_chunk
        while len(must_encode):
            bytes_read = 0
            for xc, nc in zip(must_encode, pubkey_chunk):
                bytes_read += 1
                encode_buffer += chr(ord(xc) ^ ord(nc))

                # encode and print
                if len(encode_buffer) % max_buffer_size == 0:
                    encoded_chunk = base64.b64encode(encode_buffer)
                    sys.stdout.write(encoded_chunk)
                    encode_buffer = ""

            must_encode = must_encode[bytes_read:]

        sys.stdout.flush()

    # flush out anything remaining in the encode_buffer
    if encode_buffer:
        encoded_chunk = base64.b64encode(encode_buffer)
        sys.stdout.write(encoded_chunk)

    sys.stdout.flush()

    f_private_key.close()
    f_public_key.close()    
    

if __name__ == '__main__':
    main()

