# Python Standard Library
import logging
import csv
import re

# other packages
import dateutil.parser
import icalendar


# logging
formatter = logging.Formatter('%(asctime)s|%(levelname)s|%(filename)s:%(lineno)d|%(message)s')
logFileHandler = logging.FileHandler(filename='output/log.txt', mode='w')
logFileHandler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logFileHandler)
logger.info("logging initialized")

try:
    # open source.csv
    logMessage = "opening source.csv file"
    with open('source.csv', 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        # create output file
        logMessage = "creating calendar.ics file"
        with open('output/calendar.ics', 'wb') as o:
            cal = icalendar.Calendar()
            cal.add('prodid', '-//MyCustomCalendar//')
            cal.add('version', '2.0')
            logger.info(logMessage + "... DONE")

            # loop over each row in source file
            logMessage = "iterating source file"
            for rowNo, row in enumerate(reader):
                event = icalendar.Event()

                # parse DTSTART
                logMessage = "parsing DTSTART {} on line no {}".format(row['DTSTART'], rowNo + 1)
                dtstart = dateutil.parser.parse(row['DTSTART'])
                logger.info(logMessage + "... DONE (parsed as {})".format(dtstart))

                # parse DTEND
                logMessage = "parsing DTEND {} on line no {}".format(row['DTSTART'], rowNo + 1)
                if row['DTEND'] == '' and dtstart.hour == 0 and dtstart.minute == 0 and dtstart.second == 0:
                    # If DTEND is blank and DTSTART doesn't have a time or is midnight, assume it's an all-day event
                    # all-day events are entered as DTSTART;VALUE=DATE:yyyymmdd with no DTEND
                    logger.info(logMessage + "SKIPPED: DTEND is blank and DTSTART has blank/midnight time (probable all-day event)")
                    logMessage = "adding DTSTART to all-day event (DTSTART;VALUE=DATE:yyyymmdd with no DTEND)"
                    event.add('dtstart', dtstart.date())
                    logger.info(logMessage + "... DONE")
                else:
                    dtend = dateutil.parser.parse(row['DTEND'])
                    logger.info(logMessage + "... DONE (parsed as {})".format(dtend))

                    logMessage = "adding DTSTART to event"
                    event.add('dtstart', dtstart)
                    logger.info(logMessage + "... DONE")

                    logMessage = "adding DTEND to event"
                    event.add('dtend', dtend)
                    logger.info(logMessage + "... DONE")
                
                logMessage = "adding descriptions to event, capping line length at 75 characters"
                event.add('description', re.sub("(.{75})", "\\1\r\n ", row['DESCRIPTION'], 0, re.DOTALL) )
                logger.info(logMessage + "... DONE")

                logMessage = "adding summary to event"
                event.add('summary', row['SUMMARY'])
                logger.info(logMessage + "... DONE")

                logMessage = "adding event to calendar"
                cal.add_component(event)
                logger.info(logMessage + "... DONE")

            logMessage = "writing calendar to ics file"
            o.write(cal.to_ical())
            logger.info(logMessage + "... DONE")

    logger.info("Script executed successfully")

except Exception as e:
    logger.exception("An exception occurred while {}\n{}".format(logMessage, e))
