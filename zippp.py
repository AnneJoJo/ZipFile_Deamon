#
# Create your script here.
#
"""
Author:Jingting
Version: python 3.6
Summary: Given the directory ,email and threshold size, the program can zip the required files into zipfile and
automatically sent report with files to the specific email address.
Reference: stackoverflow
Notation: 
1.The format of output for email is a little different. You need type local emails password to sent the report
the variable password is in the 'sent_email()'.
2. This program may not work on Linix system, because I only run it on the Windows
3. The program still follows the daemon way, and exit by sigterm kill (use Ctrl+c)
4. The commandline input for this progam is 
    compress_stuff.py  -n absolute path -e ####@gmail.com -s 500


"""
import argparse
import threading
import zipfile
import datetime
import random
import os
import sys
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import signal
import time
import collections


class Killer:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True


class FileCompression:
    def __init__(self, directory, ename, thresholdSize):
        """

        :param directory: str
        :param ename: str
        :param thresholdSize: float 
        """
        self.directory = directory
        self.ename = ename
        self.thresholdSize = thresholdSize

    def generate_zip_name(self):
        """
        Return the name of each zip files
        :return: str
        """
        tail = random.randint(0, 9999)
        zipFilename = "final_zip" + str(tail) + ".zip"
        return zipFilename

    def get_file_size(self, filePath):
        """
        Return the size of the file in KB
        :param filePath: 
        :return: float
        """
        fsize = os.path.getsize(filePath)
        return round(fsize, 2) / 1024

    def get_allFiles_path(self, directory):
        """
        To get each files through the directory
        :param directory: 
        :return: file_path: list
        """
        print(datetime.datetime.now())
        print("-Examing file in dir...")
        fpaths = []
        for root, directories, files in os.walk(directory):
            for filename in files:
                path = os.path.join(root, filename)
                fpaths.append(path)
        return fpaths

    def zip_all_files(self):
        """
        Filter the files we need and zip all files
        Return the compression info with the files'names
        :return: zippFilemap: dict {zipname:[saving space,compression ratio}
        """

        filter_paths = []
        directory = self.directory

        thresholdSize = self.thresholdSize

        zipFilemap = collections.defaultdict(list)
        file_paths = self.get_allFiles_path(directory)
        print("Compressed Files:\n")

        for file_name in file_paths:
            file_size = self.get_file_size(file_name)
            if "jpg" in file_name or ".zip" in file_name:
                print(datetime.datetime.now())
                print("skip the" + file_name)
                continue

            if file_size >= thresholdSize:
                print(file_name, file_size)
                filter_paths.append([file_name, file_size])
        print('Start to zip files')

        for file, fsize in filter_paths:
            tmpzipname = self.generate_zip_name()
            print(tmpzipname)
            zip = zipfile.ZipFile(tmpzipname, 'w', zipfile.ZIP_DEFLATED)
            zip.write(file)

            zipFilesize = self.get_file_size(tmpzipname)

            zipFilemap[tmpzipname] = [fsize - zipFilesize, fsize / zipFilesize]

        zip.close()

        print(str(datetime.datetime.now()) + ": All files have been zipped successfully!")
        return zipFilemap

    def generate_report(self, zippedFiles):
        """
        This function is used for generate report with zip list information
        If the compression ratio is too low, report will show the related information

        :param zippedFiles: dictionary {}
        :return: filenotes: str
        """
        ratio = 1.09
        total_saving = 0
        filenotes = ""
        lowRatioNote = ""
        for each, space in zippedFiles.items():
            filenotes += "{} saved {} KB than original".format(each, space[0]) + "\n"
            total_saving += space[0]
            if space[1] <= ratio:
                lowRatioNote += "{} has a too low compression ratio".format(each) + "\n"

        print(str(datetime.datetime.now()) + ": Would have compressed total of" + str(total_saving))
        filenotes += "The total disk saving is {}".format(total_saving) + "\n"
        filenotes += lowRatioNote
        return filenotes

    def sent_report(self, zipped):
        """
        Thr zipFile is under the same directory as script
        :param zipped: dictionary {}
        :return: Void
        """

        # the zipFile is under the same directory as script

        subject = "Report"
        tmp_message = self.generate_report(zipped)
        body = "This is an email with attachment zipFiles sent from Python\n" + tmp_message
        port = 587  # For starttls
        smtp_server = "smtp.gmail.com"
        sender_email = "####@gmail.com"  # local email server
        receiver_email = self.ename  # the email address sent to

        password = "######"  # local email password need setting up
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email

        # Add body message to email
        message.attach(MIMEText(body, "plain"))
        # Open the file in binary mode
        for zipname in zipped.keys():
            try:
                with open(zipname, "rb") as attachment:

                    # Email client can usually download this automatically as attachment
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())

                # Encode file in ASCII characters
                encoders.encode_base64(part)

                # Add header as key/value pair to attachment part
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {zipname}",
                )

                message.attach(part)
            except:
                print("sorry the file can not be attached!")
        text = message.as_string()
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)
            print(str(datetime.datetime.now()) + ":Your zipFile has been sent!")


def steps():
    killer = Killer()

    while not killer.kill_now:
        time.sleep(10)
        # if killer.kill_now:
        #     break
        print(str(datetime.datetime.now()) + ": The program start ...")
        try:
            parser = argparse.ArgumentParser(description="The directory, email and threshold size")
            parser.add_argument('-d','--noop',type = str, required = True,help ="The directory of the File ex:d://folder/")
            parser.add_argument('-e','--email',type = str,required = True, help = "The email address you want to send")
            parser.add_argument('-s','--size',type = float, required = True,help = "The threshold Size for files (KB)")
            args = parser.parse_args()
            start = time.time()
            compress = FileCompression(args.noop, args.email, args.size)
            zips = compress.zip_all_files()
            compress.sent_report(zips)
            print(datetime.datetime.now())
            print(":The program has been accomplised in {}".format(time.time() - start))
        except SystemExit:
            exmessage = sys.exc_info()[1]

            print(exmessage)


th = threading.Thread(target=steps())
th.daemon = True
th.start()






