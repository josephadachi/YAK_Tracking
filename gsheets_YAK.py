
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    # Don't know what this does really
    #flags.noauth_local_webserver = True
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret_YAK.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:    # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


class active_sheet(object):
    def __init__(self, sheet='YAK'):
        """Creates a Sheets API service object @YAK Default:
        https://docs.google.com/spreadsheets/d/1tUh8i75r99q_glFg-XqDwJB6K1PHDRDOjkFGL-GCUto/edit
        """
        self.credentials = get_credentials()
        self.http = self.credentials.authorize(httplib2.Http())
        self.discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        self.service = discovery.build('sheets', 'v4', http=self.http,
                                  discoveryServiceUrl=self.discoveryUrl)
        # YAK @: 1tUh8i75r99q_glFg-XqDwJB6K1PHDRDOjkFGL-GCUto
        # Test @: 1NoyLeO-y34M_v2iUNqVZIa4K6EDcA9sF_wdowFkjCrg
        if sheet == 'YAK':
            self.spreadsheetId = '1tUh8i75r99q_glFg-XqDwJB6K1PHDRDOjkFGL-GCUto'
        elif sheet == 'Test':
            self.spreadsheetId = '1NoyLeO-y34M_v2iUNqVZIa4K6EDcA9sF_wdowFkjCrg'
        else:
            raise NameError('Hi, that is not a sheet!')



############################################################################
####### Generalized Read Operation #########################################
############################################################################
    def read_sheet(self, rangeName='Sheet1!A1:D'):
        print('Now attempting to read a range of values!')
        #self.rangeName = rangeName            I don't think I need this line
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheetId, range=rangeName).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            print('Column B, Column C:')
            for row in values:
                # Print columns B and C, which correspond to indices 1 and 2.
                print('%s, %s' % (row[1], row[2]))
            return values

############################################################################
####### Generalized Append Operation ########################################
############################################################################
    def append_sheet(self, rangeName='Sheet1!A1', values=[['one', 'two', 'three', 'four'], ['five', 'six', 'seven', 'eight']]):
        print('Now attempting to append a value!')

        #self.rangeName = rangeName        I don't think I need this line
        #values = [['one', 'two', 'three', 'four'], ['five', 'six', 'seven', 'eight']]
        body = {'values': values}
        result = self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheetId, range=rangeName,
            valueInputOption='RAW', body=body).execute()
        print('append thingy done!')

############################################################################
####### Generalized Write Operation ########################################
############################################################################
    def write_sheet(self, rangeName='Sheet1!A8', values=[['1', '2', '3', '4'], ['5', '6', '7', '8']]):
        print('Now attempting to write a value!')

        #rangeName = 'Sheet1!A8'
        #values = [['joe', 5, 'henry'], [32, '', 'x']]
        body = {'values': values}
        result = self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheetId, range=rangeName,
            valueInputOption='RAW', body=body).execute()
        print('write thingy done!')


def main():
    print('main() was executed!')
    return


if __name__ == '__main__':
    main()
