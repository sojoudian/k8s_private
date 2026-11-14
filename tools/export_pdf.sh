#!/bin/bash
# Export a .pptx to .pdf through PowerPoint (real Calibri and Consolas). $1 = pptx path, $2 = pdf path.
set -e
C=~/Library/Containers/com.microsoft.Powerpoint/Data/Documents/clo835export
mkdir -p "$C"
base=$(basename "$1" .pptx)
cp "$1" "$C/$base.pptx"
osascript <<OSA
tell application "Microsoft PowerPoint"
  open (POSIX file "$C/$base.pptx")
  set p to active presentation
  save p in (POSIX file "$C/$base.pdf") as save as PDF
  close p saving no
end tell
OSA
cp "$C/$base.pdf" "$2"
rm -rf "$C"
