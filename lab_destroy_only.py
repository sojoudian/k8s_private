# -*- coding: utf-8 -*-
"""CLO835 - labs with no cleanup script (the user, 2026-11-11).

terraform destroy removes the three machines, and with them every Kubernetes object and every file
of the lab. So a lab has no cleanup_labNN.sh, and its last step holds only terraform destroy.

destroy_step()    : the "Clean up" step of a slide list becomes the "Destroy the cluster" step.
destroy_section() : section 7 of a Blackboard text in the long form asks only for terraform destroy.

It is guarded, so importing it writes nothing.
"""
TITLE = "Destroy the cluster"
ALSO = "# This also deletes every Kubernetes object and every file of the lab."
SECTION_OLD = "## 7. Clean Up and Destroy the Cluster"
SECTION_NEW = "## 7. Destroy the Cluster"
INTRO_NEW = ("At the end of the lab, destroy all three EC2 instances. This also deletes every Kubernetes "
             "object and every file of the lab.")


def destroy_step(slides):
    """Drop the master part of the "Clean up" step: its comments, the cleanup script and the check.
    The lines of your own machine stay, and ALSO follows the "# ON YOUR OWN MACHINE" line."""
    out, n = [], 0
    for s in slides:
        if s[0] == "step" and s[1] == "Clean up":
            lines = list(s[3])
            last = max(k for k, l in enumerate(lines) if l.startswith("$ "))
            rest = lines[last + 1:]
            while rest and not rest[0].strip():
                rest.pop(0)
            k = next(i for i, l in enumerate(rest) if l.startswith("# ON YOUR OWN MACHINE"))
            rest.insert(k + 1, ALSO)
            assert not any(l.startswith("$ ") for l in rest), rest
            assert not any("clean" in l.lower() for l in rest), rest
            assert any(l.startswith("L$ terraform destroy") for l in rest), rest
            out.append((s[0], TITLE, s[2], rest) + tuple(s[4:]))
            n += 1
        else:
            out.append(s)
    assert n == 1, "one Clean up step expected, found %d" % n
    return out


def destroy_section(text, intro_old, removed):
    """Section 7 of a long-form Blackboard text: a new title and intro, and no cleanup items.
    intro_old: the old intro line. removed: the old item lines to drop (each must occur once)."""
    for old, new in ((SECTION_OLD, SECTION_NEW), (intro_old, INTRO_NEW)):
        assert text.count(old) == 1, old
        text = text.replace(old, new)
    for line in removed:
        assert text.count(line + "\n") == 1, line
        text = text.replace(line + "\n", "")
    low = text.lower()
    assert "cleanup" not in low and "clean-up" not in low and "clean up" not in low, "cleanup text is left"
    return text
