import os
import uuid

def unique_filename(filename):

    ext = filename.split(".")[-1]

    return f"{uuid.uuid4()}.{ext}"