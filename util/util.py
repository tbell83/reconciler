from re import search
from os.path import expanduser


def get_aws_creds(profile):
    AWS_CONFIG_FILE = '{}/.aws/config'.format(expanduser('~'))
    with open(AWS_CONFIG_FILE, 'r') as aws_config_file:
        aws_config = aws_config_file.readlines()

    profiles = {}
    profile_name = ''
    for line in aws_config:
        if search('\[profile', line):
            profile_name = line.strip('\n').strip('[').strip(']') \
                        .replace('profile ', '')
            profiles[profile_name] = {}
        elif not search('^\n', line) and profile_name != '':
            key, value = line.strip('\n').replace(' ', '').split('=')
            profiles[profile_name][key] = value
        else:
            profile_name = ''

    AWS_ACCESS_KEY_ID = profiles[profile]['aws_access_key_id']
    AWS_SECRET_ACCESS_KEY = profiles[profile]['aws_secret_access_key']
    REGION = profiles[profile]['region']

    print 'Farts'
    print REGION

    return {'AWS_ACCESS_KEY_ID': AWS_ACCESS_KEY_ID,
            'AWS_SECRET_ACCESS_KEY': AWS_SECRET_ACCESS_KEY,
            'REGION': REGION}


def get_knife_creds():
    KNIFE_PATH = '{}/.chef'.format(expanduser('~'))
    KNIFE_CONFIG_FILE = '{}/knife.rb'.format(KNIFE_PATH)
    with open(KNIFE_CONFIG_FILE, 'r') as knife_config_file:
        knife_config = knife_config_file.readlines()
    knifig = {}
    for line in knife_config:
        if not search('^#', line) \
                and not search('^\n', line) \
                and not search('^current_dir', line):
            try:
                key, value = line.strip('\n').split()
                knifig[key] = value.replace(
                    '#{current_dir}',
                    KNIFE_PATH
                ).replace('"', '').replace("'", '')
            except:
                continue

    return knifig
