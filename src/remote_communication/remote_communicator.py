import logging
import os
from scp import SCPClient
import paramiko

HOST = '10.108.7.52'
IMAGES_DIR = '/home/pi/Desktop/snimki-20-40-sm/'

def get_most_recent_image_dir(ssh):
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('ls {}'.format(IMAGES_DIR))
    images = list(ssh_stdout)
    image_name = sorted(images, reverse=True)[0].strip()
    return os.path.join(IMAGES_DIR, image_name), image_name


def get_image_dir():
    return '/home/desi/Downloads/1553347394.jpeg'
    # The ssh key of the computer should be added to the raspberry already!
    # use ssh-copy-id beforehand.
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # TODO: use env variables instead of this disaster.
    ssh.connect(HOST,
                username='pi',
                password='raspberry',
                allow_agent=False,
                look_for_keys=False)

    most_recent_image_dir, image_name = get_most_recent_image_dir(ssh)
    
    with SCPClient(ssh.get_transport()) as scp:
        scp.get(most_recent_image_dir)
    
    image_dir = os.path.join(os.getcwd(), image_name)
    logging.info('Storing image to: {}'.format(image_name))
    return image_dir
    
if __name__ == "__main__":
    get_image_dir()