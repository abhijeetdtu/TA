import pathlib
import os
import datetime
import hashlib
import pandas as pd
import shutil
import glob
import pdfkit
from xhtml2pdf import pisa

class GenerateCerts:

    def __init__(self,details_f="student_details.csv"
                    ,tmpl_f="cert_tmpl.html"
                    , secret_key="secret"
                    , signatory = "Dr ABC"):
        pf = pathlib.Path(__file__).resolve().absolute().parent
        if not os.path.exists(tmpl_f):
            tmpl_f = os.path.abspath(os.path.join(pf ,tmpl_f))
        if not os.path.exists(details_f):
            details_f = os.path.abspath(os.path.join(pf ,details_f))

        self.details_f = details_f
        self.tmpl_f = tmpl_f

        self.trash_o = self.prepare_output_dir(pf)

        self.secret_key = secret_key
        self.signatory = signatory

    def prepare_output_dir(self , parent_path):
        odir = os.path.join(parent_path ,"outputs")
        if not os.path.exists(odir):
            os.mkdir(odir)

        for ftype in ["png" , "css"]:
            for file in glob.glob(os.path.join(parent_path , f"*.{ftype}")):
                shutil.copy(file, odir)
        return os.path.abspath(os.path.join(odir ,"o--{HASH}.html"))

    def get_template(self):
        try:
            return getattr(self, "tmpl")
        except:
            self.tmpl = open(self.tmpl_f).read()
        return self.tmpl

    def generate_certs(self):
        df = pd.read_csv(self.details_f)

        class CertDetails:

            SNAME = "sname"
            BCAMP = "bootcamp"

            def __init__(self,sname , camp_name):
                self.SNAME = sname
                self.BCAMP = camp_name

        def per_row(row):
            cd = CertDetails(row[CertDetails.SNAME] , row[CertDetails.BCAMP] )
            self.generate_cert(cd)

        df.apply(lambda row: per_row(row), axis=1)

    def html_to_pdf(self,html,ofile):
        result_file = open(ofile, "w+b")

        # convert HTML to PDF
        pisa.CreatePDF(
                html,                # the HTML to convert
                dest=result_file)           # file handle to recieve result

        # close output file
        result_file.close()

    def generate_cert(self,certDetails):
        tmpl = self.get_template()
        ft = tmpl.format(**{
            "STUDENT_NAME": certDetails.SNAME,
            "BOOTCAMP_NAME": certDetails.BCAMP,
            "SIGNATORY" : self.signatory,
            "DATE" : datetime.date.today().strftime("%m-%d-%Y")
        })

        hash= hashlib.md5((ft + self.secret_key).encode()).hexdigest()
        ft = ft.format(**{"HASH" : hash})
        oname = self.trash_o.format(**{"HASH" : hash})
        with open(oname , "w") as fo:
            fo.write(ft)
            fo.close()

        #self.html_to_pdf(ft,oname.replace(".html" , ".pdf"))
        pdfkit.from_file(oname, oname.replace(".html" , ".pdf") , options={
            "enable-local-file-access":None,
            "disable-smart-shrinking":None,
            "orientation" : "landscape",
            "viewport-size" :"1920x1080"
        })


if __name__ == "__main__":
    GenerateCerts().generate_certs()
