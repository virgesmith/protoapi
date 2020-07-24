#!/usr/bin/env python3

import pytest
import json
import os
# git-python seems buggy (repo got corrupted) and hard to use

version_file = "./static/swagger.json"

# wrap os.system 
def shell(cmd):
  print(cmd)
  ret = os.system(cmd)
  if ret != 0:
    raise SystemError("'%s' returned %d" % (cmd, ret))


# # 0. warn if local modifications
# ...: print("WARNING: local modifications detected")

# 1. ensure tests run ok
assert pytest.main() == pytest.ExitCode.OK

# 2. get current version from swagger
with open(version_file) as fp:
  swagger = json.load(fp)
  version_string = swagger["info"]["version"]

# 3. tag/push
print("Tagging %s" % version_string)
shell("git tag %s" % version_string)
print("Pushing tag to origin")
shell("git push origin %s" % version_string)

# 5. bump patch version, and commit to ensure 
version_numbers = [int(s) for s in version_string.split(".")]
version_numbers[2] = version_numbers[2] + 1
new_version_string = ".".join([str(n) for n in version_numbers])
print("Bumping version to %s" % new_version_string)
swagger["info"]["version"] = new_version_string
with open(version_file, "w") as fp:
  json.dump(swagger, fp, indent=2)
print("Committing version update")
shell("git add %s" % version_file)
shell("git commit -m\"[autorelease] %s\"" % version_string)

# 6. push commit and tag
print("Pushing bumped version to origin")
shell("git push origin")