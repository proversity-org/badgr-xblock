/* Javascript for BadgerXBlock. */
function BadgerXBlock(runtime, element, data) {

    var my_url = '/api/grades/v0/course_grade/course-v1:edX+DemoX+Demo_Course/users/'
    var user = data.user
    var section_title = data.section_title;
    var pass_mark = data.pass_mark;
    var award_message = data.award_message;
    var motivation_message = data.motivation_message;

    var handlerUrl = runtime.handlerUrl(element, 'new_award_badge')

    function getGrades(data) {
        var section_scores = data['section_scores'];
        var this_section = section_scores[String(section_title)];
        if ( parseFloat(this_section) >= pass_mark) {
            $.ajax({
            type: "POST",
            url: handlerUrl,
            data:JSON.stringify({"name": "badger"}),
            success: function(json) {
                var $badge = $('<p class="badger-award"> You have received a badge. <a href="' + 
                                json['asertion_url'] +
                                '">View the verified badge here.</a> </p> <img id="image-url" src="' +
                                json['image_url'] + 
                                '" style="width:250px;height:250px;">');
                $('.badger_block').append($badge);
                $('#check-for-badge').remove();
            }
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

}
