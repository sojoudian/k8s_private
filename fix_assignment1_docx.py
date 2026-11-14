#!/usr/bin/env python3
"""CLO835 Assignment 1 - repair the handout.

Reads  Assignments/Assignment_1/CLO835_Assignment1.docx
Writes Assignments/Assignment_1/CLO835_Assignment1_v2.docx

A student asked why the Recording list says Pull, then Build, then Push, then
Pull. The first Pull is an error. A student cannot pull an image before the
push creates it. The Blackboard text does not hold the error.

Four repairs:
  1. Delete the first Pull of the Recording list.
  2. Change "3 main parts" to "4 main parts".
  3. Add the Docker Compose part, which the grade table scores at 15 marks.
  4. Add a tag check to the push step, which stops a mis-tagged image.

The source file is never written. Run this file from the project root.
"""

import os
import re
import shutil
import zipfile

SRC = "Assignments/Assignment_1/CLO835_Assignment1.docx"
DST = "Assignments/Assignment_1/CLO835_Assignment1_v2.docx"
PART = "word/document.xml"

# The misplaced step. Paragraph 86 holds the correct pull, after the push.
DELETE_PARA = ("Pull the webapp and MySQL images from Docker Hub onto your "
               "Docker host using docker pull.")

# The fourth part. The grade table scores Docker Compose at 15 marks, but the
# outline names three parts only.
CLONE_AFTER = ("Updating the application, rebuilding the image, pushing it to "
               "Docker Hub, and re-deploying it as a container.")
NEW_PARA = ("Defining the whole stack in a Docker Compose file, and bringing "
            "the webapp and MySQL services up with a single command.")

REPLACE = {
    "This assignment has 3 main parts:":
        "This assignment has 4 main parts:",
    ("Use docker push to publish the tagged webapp and MySQL images to your "
     "Docker Hub repositories. Verify the images appear in Docker Hub."):
        ("Use docker push to publish the tagged webapp and MySQL images to your "
         "Docker Hub repositories. Verify the images appear in Docker Hub. Run "
         "docker images and confirm that the webapp image and the MySQL image "
         "show different IMAGE IDs. One wrong docker tag command publishes the "
         "same image two times."),
}


def paragraphs(xml):
    return re.findall(r"<w:p\b.*?</w:p>|<w:p\b[^>]*/>", xml, re.S)


def text_of(para):
    return "".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", para, re.S))


def set_text(para, new_text):
    """Replace the single run text of a paragraph."""
    escaped = (new_text.replace("&", "&amp;")
                       .replace("<", "&lt;")
                       .replace(">", "&gt;"))
    return re.sub(r"(<w:t[^>]*>).*?(</w:t>)",
                  lambda m: m.group(1) + escaped + m.group(2),
                  para, count=1, flags=re.S)


def build():
    if not os.path.exists(SRC):
        raise SystemExit("missing source: %s" % SRC)

    with zipfile.ZipFile(SRC) as archive:
        names = archive.namelist()
        blobs = {name: archive.read(name) for name in names}

    xml = blobs[PART].decode("utf-8")
    report = []

    # 1. Delete the misplaced pull.
    target = None
    for para in paragraphs(xml):
        if text_of(para).strip() == DELETE_PARA:
            target = para
            break
    if target is None:
        raise SystemExit("repair 1: the misplaced pull is not in the file")
    xml = xml.replace(target, "", 1)
    report.append("deleted the misplaced Pull step of the Recording list")

    # 2 and 4. Plain text replacements.
    for old, new in REPLACE.items():
        hit = None
        for para in paragraphs(xml):
            if text_of(para).strip() == old:
                hit = para
                break
        if hit is None:
            raise SystemExit("repair: not found -> %s" % old[:60])
        xml = xml.replace(hit, set_text(hit, new), 1)
        report.append("rewrote: %s..." % old[:52])

    # 3. Add the fourth part, as a clone of the third.
    model = None
    for para in paragraphs(xml):
        if text_of(para).strip() == CLONE_AFTER:
            model = para
            break
    if model is None:
        raise SystemExit("repair 3: the third part is not in the file")
    clone = set_text(model, NEW_PARA)
    clone = re.sub(r'\sw14:paraId="[^"]*"', "", clone)
    clone = re.sub(r'\sw14:textId="[^"]*"', "", clone)
    xml = xml.replace(model, model + clone, 1)
    report.append("added the Docker Compose part to the outline")

    blobs[PART] = xml.encode("utf-8")

    if os.path.exists(DST):
        os.remove(DST)
    with zipfile.ZipFile(SRC) as source:
        with zipfile.ZipFile(DST, "w", zipfile.ZIP_DEFLATED) as out:
            for item in source.infolist():
                out.writestr(item, blobs[item.filename])

    return report


if __name__ == "__main__":
    for line in build():
        print(" -", line)
    print("wrote %s  %.1f KB" % (DST, os.path.getsize(DST) / 1024.0))
