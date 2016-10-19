
from multiprocessing import Process, Queue
from time import asctime, sleep
import sys
from gsheets_YAK import active_sheet


def google_update(queue):
    #print('\nRunning Update Started!')
    update_rate = 1

    while True:
        sleep(10*update_rate)
        new_arrivals = []
        while not queue.empty():
            new_arrivals.append(queue.get())

            try:    #Logging into Google Sheets
                sheet = active_sheet(sheet='YAK')
            except:
                print("\nError logging into Google Docs!:", sys.exc_info()[0])
                # Write this to devices logfile
            else:
                print('\nLogged into Google Docs!')

            try:    # Appending last
                sheet.append_sheet(rangeName='Sheet1!A2', values=new_arrivals)
            except:
                print("Error Appending to Google Docs!:", sys.exc_info()[0])
            else:
                print('Everyone signed in!')


def main():
    # Add: record startup date/time in device logfile
    queue = Queue()
    update = Process(target=google_update, args=(queue,))
    update.start()
    print('Initialization Complete!')

    cond = True
    while cond==True:
        try:
            data_in = raw_input("Waiting for a name:")    # raw in python<V3
            check, first, last = data_in.split()
            print check
            if check == 'yak':
                print('Verified! \nTelling worker #2...')
                queue.put([first, last, asctime()], block=True, timeout=2)
            elif check == 'no':
                print('Okie!')
                cond = False
            else:
                print('Verification Failed!')
                raise ValueError
        except ValueError:
            print('Wrong Data format')
        except:
            print("Unexpected error:", sys.exc_info()[0])
        else:    # runs if no exceptions were raised
            print 'Okay %s %s, I told him to check you in.' % (first, last)
        finally:
            sleep(0.5)

    # Cleanup
    update.terminate()



if __name__ == '__main__':
    main()