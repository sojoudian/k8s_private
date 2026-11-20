#!/bin/bash
# $1 = folder (Week07), $2 = stem, $3 = PDF title. Export, set the PDF info, run the deck gate, make sheets.
P=/Users/maziar/Documents/c/r/k8s_private
S=${SHEETS:?"set SHEETS to a scratch folder for the page sheets"}
/Users/maziar/Documents/c/r/k8s_private/tools/export_pdf.sh $P/$1/$2.pptx $P/$1/$2.pdf
$P/.venv/bin/python -c "import sys; sys.path.insert(0,'$P'); import build_week07_lecture_v7 as K; K.set_pdf_info('$P/$1/$2.pdf', sys.argv[1])" "$3"
pdfinfo $P/$1/$2.pdf | grep -E "Title|Author|Pages"
$P/.venv/bin/python /Users/maziar/Documents/c/r/k8s_private/tools/rungate.py $1/ $2 ${4:-lecture} | grep -v "^PASS"
$P/.venv/bin/python /Users/maziar/Documents/c/r/k8s_private/tools/sheet.py $P/$1/$2.pdf $S/$2 >/dev/null
