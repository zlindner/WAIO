$(document).ready(function () {
    get_json();

    $('#refresh').click(function () {
        console.log('refresh');
    });
});

function get_json() {
    let d = new $.Deferred();

    $.ajax({
        type: 'get',
        dataType: 'json',
        url: '/get_json',
        success: function (json) {
            d.resolve(json);
        },
        fail: function (error) {
            console.log(error);
        }
    });

    return d;
}

get_json().done(function (json) {
    get_subjects(json);

    $('#subject').on('change', function () {
        get_sections(json, this.value);
    });
});

function get_subjects(json) {
    for (subject in json) {
        $("#subject").append(new Option(subject, subject));
    }
}

function get_sections(json, subj_name) {
    subject = json[subj_name];

    for (c in subject) {
        course = subject[c];

        lec = 'n/a';
        lab = 'n/a';
        sem = 'n/a';

        for (s in course.sessions) {
            session = course.sessions[s];
            ses = '';

            for (day in session.days) {
                ses += session.days[day];

                if (day != session.days.length - 1) {
                    ses += ', ';
                }
            }

            ses += '<br>' + session.time + '<br>' + session.room;

            if (session.type == 'LEC') {
                lec = ses;
            } else if (session.type == 'LAB') {
                lab = ses;
            } else {
                sem = ses;
            }
        }

        let href = 'https://www.uoguelph.ca/registrar/calendars/undergraduate/2018-2019/courses/' + course.name.split('*')[0].toLowerCase() + course.name.split('*')[1] +  '.shtml';

        $('#courses > tbody:last-child').append(
            '<tr>' +
            '<td><a href=' + href + ' target="_blank">' + course.name + '</a></td>' +
            '<td><p>' + lec + '</p></td>' +
            '<td><p>' + lab + '</p></td>' +
            '<td><p>' + sem + '</p></td>' +
            '<td><p>' + course.available + ' / ' + course.capacity + '</p></td>' +
            '</tr>'
        );

        if (course.status == 'Closed') {
            $('#courses a:last').addClass('closed');
        }
    }
}