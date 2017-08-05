import subprocess


def wifi_light(interface='wlan0'):
#    logger.info('Starting APLT server wifi scan')
#    p = subprocess.Popen(
#        'sudo iw {0} scan | egrep \'Cell |Encryption|Quality|Last beacon|ESSID|Frequency\''.format(
#        interface), shell=True, stdin=subprocess.PIPE,
#        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p = subprocess.Popen(
        'sudo iw {0} scan | egrep \'SSID:\''.format(
        interface), shell=True, stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    test = p.communicate()
    print(test[0])
    return parse_wifi_survey(test[0])

def parse_wifi_survey(survey):
        """survay should be the raw stdout from p.communicate()

        """
        foo = survey.splitlines()
        survey_dict = dict()
        foo_dict = dict()
        x = 0
        ct = 0
        # print foo
        while x < len(foo):
            foo[x] = foo[x].lstrip()
            # print foo[x]
            if b'SSID' in foo[x]:
                pho = foo[x].lstrip(b'SSID:')
                survey_dict.update([(1, pho)])
#                survey_dict.update([(footils.strip_colons(foo_dict[ct]), pho)])
            if b'Cell' in foo[x]:
                foo2 = foo[x].split(' ')
                foo_dict.update([(ct, foo2[4])])
            if b'ESSID' in foo[x]:
                pho = foo[x].lstrip(b'ESSID:')
                pho = pho.strip(b'"')
                survey_dict.update([(footils.strip_colons(foo_dict[ct]), pho)])
                # survey_dict.update([(footils.strip_colons(foo_dict[ct]), foo[x].lstrip('ESSID:'))])
                ct += 1
            x += 1

        return survey_dict

survey_list = wifi_light('wlp3s0')
print(survey_list)
