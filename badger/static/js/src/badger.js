/* Javascript for BadgerXBlock. */
function BadgerXBlock(runtime, element, data) {

    function updateCount(result) {
        $('.count', element).text(result.count);
        console.log(result.count);
    }

    var my_url = '/api/grades/v0/course_grade/course-v1:edX+DemoX+Demo_Course/users/?username=staff'
    var section_title = data.section_title;
    var pass_mark = data.pass_mark;
    var award_message = data.award_message;
    var motivation_message = data.motivation_message;
    $('p', element).click(function(eventObject) {
        console.log('click');
        console.log(section_title, pass_mark);
        $.ajax({
            type: "GET",
            url: my_url,
            data: JSON.stringify({"hello": "world"}),
            success: function(data) {
                var b = JSON.stringify(data);
                var section_scores = data['section_scores'];
                console.log(section_scores);
                var this_section = section_scores[String(section_title)];
                console.log(this_section);
                if (this_section >= pass_mark) {
                    alert(award_messag)
                }
                else {
                    alert(motivation_message)
                }
                
            }
        });
    });

    $(function ($) {
        /* Here's where you'd do things on page load. */
    });
}
