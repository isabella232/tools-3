import sys

if len(sys.argv) < 2:
        print "Usage: sys.argv[0] <container_id>"
        sys.exit(1)

container_id = sys.argv[1]

try: 
        container_status = subprocess.check_output(["runc", "state", container_id])
except subprocess.CalledProcessError:
        print "container not found; probably exited"
        sys.exit(0)

status_json = json.loads(container_status)
if status_json['status'] == "stopped":
        print "container already stopped"
        sys.exit(0)

rootfs_path = status_json['rootfs']
dir_path = os.path.dirname(rootfs_path)
top_layer_id = os.path.basename(dir_path)
container_mount_output = subprocess.check_output("mount | grep " + top_layer_id, shell=True)

if container_mount_output == "":
        print "container not found; probably exited"
        sys.exit(0)

m = re.search('lowerdir=(.*),upperdir', container_mount_output)
if m:
        lowerdirs = m.group(1).split(':')
        for l in lowerdirs:
                print l
else:
        print "Unable to find lowerdir in mount output: ", container_mount_output
        sys.exit(1)

m = re.search('upperdir=(.*),workdir', container_mount_output)
if m:
        upperdir = m.group(1)
        print upperdir
else:
        print "Unable to find upperdir in mount output: ", container_mount_output
        sys.exit(1)
