# -*- coding: utf-8 -*-
"""CLO835 Week 04 - no cleanup script (the user, 2026-11-11).

terraform destroy removes the three machines and every object and file of the lab. The Week 04
deck shows no clean-up, and master-init never wrote cleanup_lab04.sh to the master, so
"./cleanup_lab04.sh" in Step 6 failed on the master anyway. This script changes only the course
repository folder Week04: Step 6 of localMachine.sh holds only terraform destroy, and
cleanup_lab04.sh is deleted.

It is guarded, so importing it writes nothing. It stops if the folder is not in its old form.
"""
import os
import sys

import lab_destroy_only as D
import lab_kubeadm as L

WEEK = os.path.join(L.REPO, "Week04")
OLD = ("# Step 6 - clean up\n"
       "########################################################\n"
       "./cleanup_lab04.sh\n")
NEW = ("# Step 6 - Destroy the cluster\n"
       "########################################################\n"
       "# ON YOUR OWN MACHINE - remove the three EC2 machines.\n"
       "%s\n"
       "# ON YOUR OWN MACHINE:  terraform destroy\n"
       "#\n"
       "# Always destroy. The Learner Lab budget is small.\n") % D.ALSO

if __name__ == "__main__":
    path = os.path.join(WEEK, "localMachine.sh")
    text = open(path, encoding="utf8").read()
    if text.count(OLD) != 1 or not text.endswith(OLD):
        sys.exit("Week04/localMachine.sh is not in its old form; nothing changed.")
    open(path, "w", encoding="utf8").write(text.replace(OLD, NEW))
    old = os.path.join(WEEK, "cleanup_lab04.sh")
    if os.path.exists(old):
        os.remove(old)
    left = [f for f in os.listdir(WEEK) if "cleanup" in open(os.path.join(WEEK, f), encoding="utf8").read()]
    assert not left, left
    print("repo folder : %s (%d files)" % (WEEK, len(os.listdir(WEEK))))
