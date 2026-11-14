# Report: Fix the simple-webapp-flask Repo Link in the Week 2 Slides
**Date**: 2026-09-16
**Sequence**: #02 for the day

## Summary
Slide 18 of the Week 2 lecture used the wrong repo link, `https://github.com/mmumshad/simple-webapp-flask`. The correct link is `https://github.com/sojoudian/simple-webapp-flask`. Claude changed the link in the build script, the style deck, its PDF, and the three copies of the source deck. Claude also compared the Lab 2 slides with the correct repo and fixed three wrong port numbers. One text difference ("Welcome to CLO835!") needs a decision from the user.

## What Changed
- `build_week02.py` line 492: the old link is now the new link.
- `week02/Week02_lecture_style_v1.pptx`: rebuilt from the script. Only `ppt/slides/slide18.xml` changed.
- `week02/Week02_lecture_style_v1.pdf`: exported again with LibreOffice. Only the page 18 text changed.
- `week02/Week02.pptx`, `finalWork/Week02.pptx`, `../CLO835_Lectures/Week02.pptx`: slide 18 SmartArt link changed in `ppt/diagrams/data3.xml` and `ppt/diagrams/drawing3.xml`. The three files are identical again (MD5 `69419377af56f31958541b9cee92b27f`).
- `Lab02.pptx` and `finalWork/Lab02.pptx`:
  - Slide 5: `curl http://<container-ip>:8080` changed to `:18080`.
  - Slide 6: "answers on port 5000." changed to "answers on port 18080."
  - Slide 9: `# run and publish port 8080` changed to `# run and publish port 18080`.
- Backups of all original files are in the session scratchpad: `backup_2026-09-16/`.

## Technical Details
Facts from the correct repo (`sojoudian/simple-webapp-flask`, last commit `b778ada`, 2026-05-13):
- `app.py`: `/` returns `Welcome CLO835!`. The second route is `/how are you`.
- `Dockerfile`: `FROM ubuntu:22.04`, `pip3 install flask`, `EXPOSE 18080`, `ENTRYPOINT ["flask", "run", "--host=0.0.0.0", "--port=18080"]`.

Facts from the old repo (`mmumshad/simple-webapp-flask`):
- `/` returns `Welcome!`. The app uses port 5000.

Method:
1. Scan all `.pptx`, `.pdf`, `.md`, `.txt`, and `.py` files in `k8s_week3` and `CLO835_Lectures` for `mmumshad` and `simple-webapp`.
2. Rebuild the style deck with `build_deck()` to a scratch path. Compare all parts with the current deck. Only slide 18 was different.
3. Replace the exact strings inside the zip parts of the other decks. Keep all other bytes.
4. Parse all XML parts with lxml. Open each deck with python-pptx. Render the changed slides with LibreOffice and check them visually.

## Results
- The old flask link is not in any active file now.
- All changed decks have valid XML, and LibreOffice opens them.
- Slide 18 renders with the full new link on one line.
- No local server was used. No port was used.

## Issues / Notes
- **Decision needed:** Lab 2 slides 6 and 9 and `Labs/Lab01/Lab01.txt` expect `Welcome to CLO835!`. The repo `app.py` returns `Welcome CLO835!`. Claude did not change these. Either change `app.py` in the repo, or change the slides and `Lab01.txt`.
- **PowerPoint:** `week02/Week02_lecture_style_v1.pptx` is open in PowerPoint. If you save it from PowerPoint, the old link comes back. Close it without saving, and then open it again.
- **Script bug found and fixed:** The first Lab 2 run split each pair at `=>`. The slide 9 pair contained `<=>`, so the XML broke. The original file was not changed. Claude changed the separator to `|||` and ran the fix again. The Week 2 source deck pair had no `<` or `>`, and its XML is valid.
- **Not changed:**
  - `old/Week02.pptx` (archive) still has the old flask link (slides 18 and 27) and `mmumshad/simple-webapp-color` (slide 16).
  - `build_week12.py`, `Week12/*.pptx`, and `old/Week10.pptx` use `mmumshad/simple-webapp-mysql`. `sojoudian/simple-webapp-mysql` does not exist on GitHub (HTTP 404).
- **Repo README:** The README uses ports 5000 and 8080, and shows `docker run -p 8080:8080`. The Dockerfile uses port 18080. This is a repo problem, not a slide problem.
