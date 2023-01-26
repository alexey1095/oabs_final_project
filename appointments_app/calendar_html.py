from datetime import timedelta
from datetime import datetime

class Calendar:

    def __init__(
        self,
        appointment_length_minutes,
        opening_hours_from,
        opening_hours_till
    ):

        # length of appointments in minutes
        self.appointment_length_minutes = appointment_length_minutes

        # opening hours from
        self.opening_hours_from = opening_hours_from
        self.opening_hours_till = opening_hours_till

        

    def _addCell(self, appointment_time, color):

        td = "<tr>"

        if color == "green":
            td += "<td class='table-success'>"
        elif color == "grey":
            td += "<td class='table-secondary'>"
        elif color == "red":
            td += "<td class='table-danger'>"
        else:
            td += "<td>"

        td += str(appointment_time) + "</td>" + "</tr>"

        return td

    def _generateOneDayColumn(self, day):

        tbl = "<td>"

        tbl += str(day)

        tbl += "<table class='table table-hover'><tbody>"

        appointment_time = self.opening_hours_from + self.appointment_length_minutes

        while appointment_time < self.opening_hours_till and self.opening_hours_till - appointment_time >= self.appointment_length_minutes:

            tbl += self._addCell(appointment_time, 'green')

        tbl += " </tbody></table></td>"


if __name__ == "__main__":
    calendar = Calendar(
        appointment_length_minutes=timedelta(hours=0, minutes=20, seconds=0),
        opening_hours_from=time(7,0,0), 
        opening_hours_till=time(17,0,0)
        )

    calendar._generateOneDayColumn('17')
