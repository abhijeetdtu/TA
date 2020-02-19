import matplotlib.pyplot as plt
import base64
from io import BytesIO


def ToHTMLImg(img):
    tmpfile = BytesIO()
    #fig.savefig(tmpfile, format='png')
    img.save(tmpfile,format="png")
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    #encoded = base64.b64encode(img)
    return '<img src=\'data:image/png;base64,{}\'>'.format(encoded)

def ToHTML(title ,sentences , img):
    template = """
        <div class="row">
            {}
        </div>
        <div class="row">
            <div class="col-md-5">
                {}
            </div>
            <div class="col-md-7">
                {}
            </div>
        </div>
    """
    ul = f"""
    <ul>
        {"".join(["<li>{}</li>".format(i) for i in sentences])}
    </ul>
    """
    return template.format(title , ul , img)
