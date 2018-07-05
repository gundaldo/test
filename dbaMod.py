#!/usr/bin/python3

import subprocess
import sys
import logging


def OutputStream(loutput):
    # Poll process for new output until finished
    while True:
        nextline = loutput.stdout.readline()
        if nextline == '' and loutput.poll() is not None:
            break
        sys.stdout.write(nextline.decode('utf-8'))
        sys.stdout.flush()
        return


def SubMProc(*cmds):
    count = 1
    for cmd in cmds:
        if count == 1:
            loutput = 'output' + '_' + str(count)
            loutput = subprocess.Popen(cmd,
                                       shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
        else:
            noutput = 'output' + '_' + str(count)
            noutput = subprocess.Popen(cmd,
                                       shell=True,
                                       stdin=loutput.stdout,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            loutput = noutput
        count = count + 1
    out, err = loutput.communicate()
    return(out, err, loutput.returncode)


def initialize_logging(logfile):
    """
       Define Logging - set up logging to file
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s: %(filename)s: %(levelname)s: %(message)s',
        datefmt='%m-%d-%y %H:%M:%S',
        filename=logfile,
        filemode='w')

    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

    # set a format which is simpler for console use
    formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(message)s')

    # tell the handler to use this format
    console.setFormatter(formatter)

    # add the handler to the root logger
    logging.getLogger('').addHandler(console)

    # Now, define a couple of other loggers which might represent areas in your
    # application:
    log = logging.getLogger(__name__)

    return log


def QVault(tier_name, secret, label):
    """
       QVault(tier_name, secret, label)

       All finance environment credentials are stored in Vault.
       Using this module helps to retrieve secrets from
       vault.

       Method executes actual code to pull secrets from vault
       - Returns a tuple of out & err

         Example: out,err,rcode = QVault('omegaapp','OMSDEV1_apps','password')

         Output is in binary format so using decode to convert to Unicode.
         apps_passwd = out.decode().strip()
    """

    v_addr = 'export' + ' VAULT_ADDR=' + 'https://templar.thefacebook.com;'
    v_cmd = '/usr/local/bin/vault'

    cmd = v_addr + v_cmd + ' read ' + '-field=' + label + \
        ' /secret/tier/' + tier_name + '/' + secret
    return (SubMProc(cmd))


class Tag:
    """
    Defines the tags for each message shown in the output.
    """
    bold = "\033[1m"

    green = "\033[32m"
    red = "\033[31m"
    yellow = "\033[33m"

    bold_green = bold + green
    bold_red = bold + red
    bold_yellow = bold + yellow

    end = "\033[0m"

    failed = "[{0}FAILED{1}]".format(bold_red, end)
    passed = "[{0}PASSED{1}]".format(green, end)
    exception = "[{0}EXCEPTION{1}]".format(bold_red, end)
    info = "[{0}INFO{1}]".format(green, end)
