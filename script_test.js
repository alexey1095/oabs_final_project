const calendarUpdater = {

    // get_stored_values: function () {

    //     // getting stored values and convert into integer
    //     year = parseInt(sessionStorage.getItem("year"), 10);
    //     week_number = parseInt(sessionStorage.getItem("week_number"), 10);

    //     return {
    //         'year': year,
    //         'week_number': week_number
    //     };
    // },


    update_calendar: function (doctor_id, year, week_number) {
        const request = new XMLHttpRequest();
        request.open('GET', '/appointment/api/calendar/' + doctor_id + '/' + year + '/' + week_number + '/');
        request.send();

        request.onload = function () {
            if (request.status == 200) {
                let table = document.getElementById('table_calendar');
                table.innerHTML = request.response;
            }
        };
        return true;
    },

    get_number_of_weeks: function (year) {

        // check if the incremented week number exists in the given year
        const year_js = moment().year(year);
        return year_js.weeksInYear();
    },

        increment_week_number: function () {

            year = parseInt(sessionStorage.getItem("year"), 10);
            week_number = parseInt(sessionStorage.getItem("week_number"), 10);


            week_number += 1;

            // check if the incremented week number exists in the given year
            // const year_js = moment().year(self.year);
            // const number_of_weeks = year_js.weeksInYear();

            const number_of_weeks = this.get_number_of_weeks(year);

            if (week_number > number_of_weeks) {

                // if the incremented week does not exist in the current year then we need to switch
                // to the next year with week number of 1.

                year += 1;
                sessionStorage.setItem("year", year);

                week_number = 1;

            }

            sessionStorage.setItem("week_number", week_number);

            self.update_calendar(1, year, week_number);

    return true;

        },

    decrement_week_number: function () {

        year = parseInt(sessionStorage.getItem("year"), 10);
        week_number = parseInt(sessionStorage.getItem("week_number"), 10);


        // special care needs to be taken when the current week is one and we are going to decrement this
        if (week_number == 1) {

            // we need to decrement the year as week 0 does not exist
            year -= 1;

            //we need to check how many weeks are in the decremented year
            let number_of_weeks = this.get_number_of_weeks(year);


            // and assign this number to the week counter
            week_number = number_of_weeks;

        } else {

            // just decrement when we are no in the edge
            week_number -= 1;

        }

        sessionStorage.setItem("year", year);
        sessionStorage.setItem("week_number", week_number);

        self.update_calendar(1, year, week_number);

        return true;
    },
};