"""Turn a student script (localMachine.sh) into a runner that shows each command and its exit code.

Two forms:
  python3 instrument.py <localMachine.sh> <out.sh> <delay>
      writes <out.sh> with "### [n] step s: cmd" and "### [n] exit N" lines (the Week 10 form).
  python3 instrument.py <localMachine.sh> <url>
      shows the runner on stdout in the form of gate_week12.py: echo "@@STEP s" (one time for each step),
      echo "@@CMD Lnn: cmd", then echo "@@RC $?". The url is accepted and not used. Set DELAY=3 in the
      environment of the runner for 3 s between commands; the runner text stays the same.

A command is one line, a line that ends with a backslash together with the lines that follow it,
or a heredoc block (a line with <<'EOF', or a line that ends with <<EOF, up to the line EOF). The unquoted
form is the CSR file of Week 13 and Week 14, where the shell must expand $(...). Comment lines and blank
lines are skipped.
"""
import sys


def commands(path, last=99):
    lines = open(path).read().split("\n")
    out, i, step = [], 0, -1
    while i < len(lines):
        l = lines[i]
        if l.startswith("# Step "):
            step = int(l.split()[2])
        if step > last:
            break
        if not l.strip() or l.lstrip().startswith("#") or l.startswith("#!"):
            i += 1
            continue
        start = i + 1
        if "<<'EOF'" in l or l.rstrip().endswith("<<EOF"):
            j = lines.index("EOF", i)
            out.append((step, start, "\n".join(lines[i:j + 1])))
            i = j + 1
            continue
        block = [l]
        while block[-1].rstrip().endswith("\\") and i + 1 < len(lines):
            i += 1
            block.append(lines[i])
        out.append((step, start, "\n".join(block)))
        i += 1
    return out


def dq(text):
    """Text that is safe inside a double-quoted echo."""
    for a, b in (("\\", "\\\\"), ('"', '\\"'), ("$", "\\$"), ("`", "\\`")):
        text = text.replace(a, b)
    return text


def gate_runner(path):
    body, last = ["#!/bin/bash", "cd ~", "DELAY=${DELAY:-0}"], None
    for step, line, cmd in commands(path):
        if step != last:
            body.append('echo "@@STEP %d"' % step)
            last = step
        body.append('echo "@@CMD L%d: %s"' % (line, dq(cmd.split("\n")[0])))
        body.append(cmd)
        body.append('echo "@@RC $?"')
        body.append("sleep $DELAY")
    return "\n".join(body) + "\n"


def hash_runner(path, delay, last=99):
    cmds = commands(path, last)
    body = ["#!/bin/bash", "cd ~"]
    for n, (s, _, c) in enumerate(cmds, 1):
        head = c.split("\n")[0].replace("'", "'\"'\"'")
        body.append("echo '### [%d] step %d: %s'" % (n, s, head))
        body.append(c)
        body.append('echo "### [%d] exit $?"' % n)
        if delay != "0":
            body.append("sleep %s" % delay)
    return "\n".join(body) + "\n", cmds


if __name__ == "__main__":
    src = sys.argv[1]
    if len(sys.argv) == 3 and sys.argv[2].startswith("http"):
        sys.stdout.write(gate_runner(src))
    else:
        out, delay = sys.argv[2], sys.argv[3]
        last = int(sys.argv[4]) if len(sys.argv) > 4 else 99
        text, cmds = hash_runner(src, delay, last)
        open(out, "w").write(text)
        print("commands: %d" % len(cmds))
        for s in sorted(set(x for x, _, _ in cmds)):
            print("  step %d: %d" % (s, sum(1 for x, _, _ in cmds if x == s)))
