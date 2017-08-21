/* Javascript for BadgerXBlock. */
function BadgerXBlock(runtime, element, data) {

    var my_url = '/api/grades/v0/course_grade/course-v1:edX+DemoX+Demo_Course/users/'
    var user = data.user
    var badger_api = 'http://badgr.proversity.org/v1/issuer/issuers/proversity/badges/congeniality/assertions'
    var section_title = data.section_title;
    var pass_mark = data.pass_mark;
    var award_message = data.award_message;
    var motivation_message = data.motivation_message;

    var handlerUrl = runtime.handlerUrl(element, 'new_award_badge')

    function getGrades(data) {
        var b = JSON.stringify(data);
        var section_scores = data['section_scores'];
        var this_section = section_scores[String(section_title)];
        console.log(section_scores);
        console.log(this_section);
        if ( parseFloat(this_section) == pass_mark) {
            $.ajax({
            type: "POST",
            url: badger_api,
            data: JSON.stringify(),
            success: getGrades
        });

        }
        else {
            alert(motivation_message)
        }
    }



    $('a', element).click(function(eventObject) {
        $.ajax({
            type: "GET",
            url: my_url,
            data: JSON.stringify({"hello": "world"}),
            success: getGrades
        });
    });

    $(function ($) {
        /* Here's where you'd do things on page load. */
    });
}
