# Python Standard Library
import logging
import csv
import textwrap

# other packages
import dateutil.parser


# logging
formatter = logging.Formatter('%(asctime)s|%(levelname)s|%(filename)s:%(lineno)d|%(message)s')
logFileHandler = logging.FileHandler(filename='output/log.txt', mode='w')
logFileHandler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logFileHandler)
logger.info("logging initialized")

try:
    logMessage = "opening source.csv file"
    with open('source.csv', 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        logMessage = "creating calendar.ics file and writing header"
        with open('output/calendar.ics', 'w') as o:
            
            o.write("BEGIN:VCALENDAR\n")
            o.write("VERSION:2.0\n")
            o.write("PRODID:-//MyCalendar//\n")
            logger.info(logMessage + "... DONE")

            logMessage = "iterating source file"
            for rowNo, row in enumerate(reader):
                logMessage = "writing event header"
                o.write("BEGIN:VEVENT\n")

                logMessage = "adding summary to event"
                summary = "\r\n ".join(textwrap.wrap(text=row['SUMMARY'], width=75, initial_indent='SUMMARY:', drop_whitespace=True, break_on_hyphens=True, break_long_words=True))
                o.write("{}\n".format(summary))
                logger.info(logMessage + "... DONE")

                # parse DTSTART
                logMessage = "parsing DTSTART {} on line no {}".format(row['DTSTART'], rowNo + 1)
                dtstart = dateutil.parser.parse(row['DTSTART'])
                logger.info(logMessage + "... DONE (parsed as {})".format(dtstart))

                # parse DTEND
                logMessage = "parsing DTEND {} on line no {}".format(row['DTSTART'], rowNo + 1)
                if row['DTEND'] == '' and dtstart.hour == 0 and dtstart.minute == 0 and dtstart.second == 0:
                    # If DTEND is blank and DTSTART doesn't have a time (or is midnight), assume it's an all-day event
                    # all-day events are entered as DTSTART;VALUE=DATE:yyyymmdd with no DTEND
                    logger.info(logMessage + "SKIPPED: DTEND is blank and DTSTART has blank/midnight time (probable all-day event)")
                    logMessage = "adding DTSTART to all-day event (DTSTART;VALUE=DATE:yyyymmdd with no DTEND)"
                    o.writelines("DTSTART;VALUE=DATE:{}\n".format(dtstart.strftime('%Y%m%d')))
                    logger.info(logMessage + "... DONE")
                else:
                    dtend = dateutil.parser.parse(row['DTEND'])
                    logger.info(logMessage + "... DONE (parsed as {})".format(dtend))
                    logMessage = "adding DTSTART to event"
                    o.write("DTSTART:{}\n".format(dtstart.strftime("%Y%m%dT%H%M%S")))
                    logger.info(logMessage + "... DONE")

                    logMessage = "adding DTEND to event"
                    o.write("DTEND:{}\n".format(dtend.strftime("%Y%m%dT%H%M%S")))
                    logger.info(logMessage + "... DONE")
                
                if row['DESCRIPTION']:
                    logMessage = "adding description to ics file"
                    description = "\r\n ".join(textwrap.wrap(text=row['DESCRIPTION'], width=75, initial_indent='DESCRIPTION:', drop_whitespace=True, break_on_hyphens=True, break_long_words=True))
                    o.write("{}\n".format(description))
                    logger.info(logMessage + "... DONE")
                else:
                    logger.info("skipping missing description")

                logMessage = "adding END:EVENT to ics file"
                o.write("END:VEVENT\n")
                logger.info(logMessage + "... DONE")               

            logMessage = "adding END:CALENDAR to ics file"
            o.write("END:VCALENDAR\n")
            logger.info(logMessage + "... DONE")
                
    logger.info("Script executed successfully")

except Exception as e:
    logger.exception("An exception occurred while {}\n{}".format(logMessage, e))
