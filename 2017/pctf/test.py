from subprocess import call

l = "\"`ls`\""
call(["sh","-c", "echo " + " -n a.wav \"" + l + "\""])

