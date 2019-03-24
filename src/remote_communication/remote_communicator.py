import logging
import os
from scp import SCPClient
import paramiko
from time import sleep


HOST = '10.108.7.62'
IMAGES_DIR = '/home/pi/Desktop/snimki-20-40-sm/'
MOVER_SCRIPT = 'python3 /home/pi/Desktop/fmi-wall-e/camera/movements_layer.py {} {}'

def get_ssh_connection():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # TODO: use env variables instead of this disaster.
        ssh.connect(HOST,
                    username='pi',
                    password='raspberry',
                    allow_agent=False,
                    look_for_keys=False)
        return ssh
    except Exception as e:
        sleep(300)
        # Trying forever
        print('SSH-ing not successful, trying again...')
        return get_ssh_connection()

    return ssh


def get_most_recent_image_dir(ssh):
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('ls {}'.format(IMAGES_DIR))
    images = list(ssh_stdout)
    image_name = sorted(images, reverse=True)[0].strip()
    return os.path.join(IMAGES_DIR, image_name), image_name


def get_image_dir():
    return '/home/desi/Downloads/1553347394.jpeg'
    # The ssh key of the computer should be added to the raspberry already!
    # use ssh-copy-id beforehand.
    ssh = get_ssh_connection()

    most_recent_image_dir, image_name = get_most_recent_image_dir(ssh)
    
    with SCPClient(ssh.get_transport()) as scp:
        scp.get(most_recent_image_dir)
    
    image_dir = os.path.join(os.getcwd(), image_name)
    logging.info('Storing image to: {}'.format(image_name))
    return image_dir


def move_remote(command, arg, ssh=None):
    if ssh is None or not ssh.get_transport().is_active():
        print('SSHING')
        ssh = get_ssh_connection()
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(MOVER_SCRIPT.format(command, arg))    
    print('\n'.join(ssh_stdout))
    logging.warn('\n'.join(ssh_stderr))
    return ssh

if __name__ == "__main__":
    # move_remote('MOVE_BODY_FORWARD', 'FORWARD_DISTANCE_LONG')

    # left
    # move_remote('MOVE_HORIZONTAL', 20)

    # right
    # move_remote('MOVE_HORIZONTAL', -20)

    # left
    # move_remote('MOVE_VERTICAL', 20)

    # right
    # move_remote('MOVE_VERTICAL', -20)

    # claw
    # move_remote('MOVE_CLAW', 'OPEN')
    # move_remote('MOVE_CLAW', 'CLOSE')

    # clas orient
    # move_remote('ORIENT_CLAW', 20)
