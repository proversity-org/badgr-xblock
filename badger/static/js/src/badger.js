/* Javascript for BadgerXBlock. */
function BadgerXBlock(runtime, element) {

    function updateCount(result) {
        $('.count', element).text(result.count);
    }


    
    var handlerUrl = runtime.handlerUrl(element, 'increment_count');
    var my_url = 'http://0.0.0.0:8000/api/grades/v0/course_grade/course-v1:edX+DemoX+Demo_Course/users/?username=staff'

    $('p', element).click(function(eventObject) {
        console.log(handlerUrl);
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify({"hello": "world"}),
            success: updateCount
        });
    });

    $(function ($) {
        /* Here's where you'd do things on page load. */
    });
}
