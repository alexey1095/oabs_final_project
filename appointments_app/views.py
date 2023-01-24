from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.


def appointment_view(request):
    return render(request, 'calendar_test.html')


#@login_required
def api_calendar(request, doctor_id, year, week_number):
    ''' returns calendar'''

    html_table = '''<table class='table' id='table_calendar'>
            <thead>
                <tr>
            <th class='text-center' colspan='7'>'''

    html_table += "December 2020"

    html_table += '''</th>
        </tr>
        <tr>
            <th scope="col">Mon</th>
            <th scope="col">Tue</th>
            <th scope="col">Wed</th>
            <th scope="col">Thu</th>
            <th scope="col">Fri</th>
            <th scope="col">Sat</th>
            <th scope="col">Sun</th>
        </tr>
    </thead>'''

    html_table += '''<tbody class='table-group-divider'>
            <tr>
                <td>1
                    <table class="table table-hover" id="mon_table">
                        <tbody>
                            <tr>
                                <td class="table-secondary">7:00</td>
                            </tr>
                            <tr>
                                <td class="table-success">7:20</td>
                            </tr>
                            <tr>
                                <td class="table-success">7:40</td>
                            </tr>
                            <tr>
                                <td class="table-success">
                                    8:00
                                    <!-- <button class="btn btn-outline-primary btn-xs">Book</button> -->

                                </td>
                            </tr>
                            <tr>
                                <td class="table-danger">8:20</td>
                            </tr>
                            <tr>
                                <td class="table-danger">8:40</td>
                            </tr>
                            <tr>
                                <td class="table-success">9:00</td>
                            </tr>
                            <tr>
                                <td class="table-success">9:20</td>
                            </tr>
                            <tr>
                                <td class="table-success">9:40</td>
                            </tr>
                            <tr>
                                <td class="table-success">10:00</td>
                            </tr>
                            <tr>
                                <td class="table-success">10:20</td>
                            </tr>
                            <tr>
                                <td class="table-success">10:40</td>
                            </tr>
                            <tr>
                                <td>11:00</td>
                            </tr>
                            <tr>
                                <td>11:20</td>
                            </tr>
                            <tr>
                                <td>11:40</td>
                            </tr>
                            <tr>
                                <td>12:00</td>
                            </tr>
                            <tr>
                                <td>12:20</td>
                            </tr>
                            <tr>
                                <td>12:40</td>
                            </tr>
                            <tr>
                                <td>13:00</td>
                            </tr>
                            <tr>
                                <td>13:20</td>
                            </tr>
                            <tr>
                                <td>13:40</td>
                            </tr>
                            <tr>
                                <td>14:00</td>
                            </tr>
                            <tr>
                                <td>14:20</td>
                            </tr>
                            <tr>
                                <td>14:40</td>
                            </tr>
                            <tr>
                                <td>15:00</td>
                            </tr>
                            <tr>
                                <td>15:20</td>
                            </tr>
                            <tr>
                                <td>15:40</td>
                            </tr>
                            <tr>
                                <td>16:00</td>
                            </tr>
                            <tr>
                                <td>16:20</td>
                            </tr>
                            <tr>
                                <td>16:40</td>
                            </tr>
                            <tr>
                                <td>17:00</td>
                            </tr>
                            <tr>
                                <td>17:20</td>
                            </tr>
                            <tr>
                                <td>17:40</td>
                            </tr>
                        </tbody>
                    </table>
                </td>

                <td>2
                    <table class="table table-hover" id="tue_table">
                        <tbody>
                            <tr>
                                <td class="table-secondary">7:00</td>
                            </tr>
                            <tr>
                                <td class="table-success">7:20</td>
                            </tr>
                            <tr>
                                <td class="table-success">7:40</td>
                            </tr>
                            <tr>
                                <td class="table-success">
                                    8:00
                                    <!-- <button class="btn btn-outline-primary btn-xs">Book</button> -->

                                </td>
                            </tr>
                            <tr>
                                <td class="table-danger">8:20</td>
                            </tr>
                            <tr>
                                <td class="table-danger">8:40</td>
                            </tr>
                            <tr>
                                <td class="table-success">9:00</td>
                            </tr>
                            <tr>
                                <td class="table-success">9:20</td>
                            </tr>
                            <tr>
                                <td class="table-success">9:40</td>
                            </tr>
                            <tr>
                                <td class="table-success">10:00</td>
                            </tr>
                            <tr>
                                <td class="table-success">10:20</td>
                            </tr>
                            <tr>
                                <td class="table-success">10:40</td>
                            </tr>
                            <tr>
                                <td>11:00</td>
                            </tr>
                            <tr>
                                <td>11:20</td>
                            </tr>
                            <tr>
                                <td>11:40</td>
                            </tr>
                            <tr>
                                <td>12:00</td>
                            </tr>
                            <tr>
                                <td>12:20</td>
                            </tr>
                            <tr>
                                <td>12:40</td>
                            </tr>
                            <tr>
                                <td>13:00</td>
                            </tr>
                            <tr>
                                <td>13:20</td>
                            </tr>
                            <tr>
                                <td>13:40</td>
                            </tr>
                            <tr>
                                <td>14:00</td>
                            </tr>
                            <tr>
                                <td>14:20</td>
                            </tr>
                            <tr>
                                <td>14:40</td>
                            </tr>
                            <tr>
                                <td>15:00</td>
                            </tr>
                            <tr>
                                <td>15:20</td>
                            </tr>
                            <tr>
                                <td>15:40</td>
                            </tr>
                            <tr>
                                <td>16:00</td>
                            </tr>
                            <tr>
                                <td>16:20</td>
                            </tr>
                            <tr>
                                <td>16:40</td>
                            </tr>
                            <tr>
                                <td>17:00</td>
                            </tr>
                            <tr>
                                <td>17:20</td>
                            </tr>
                            <tr>
                                <td>17:40</td>
                            </tr>
                        </tbody>
                    </table>


                </td>
                <td>3</td>
                <td>4</td>
                <td>5</td>
                <td>6</td>
                <td>7</td>
            </tr>


        </tbody>
    </table> '''

    return HttpResponse(html_table, content_type="text/html", status=200)
