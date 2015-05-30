(function($) {
    $(function() {
        var datetime_format = django.get_format('DATETIME_FORMAT');

        $("#comment_form").ajaxForm(function(comment) {
            var updated_at = new Date(comment.updated_at).format(datetime_format);
            $("#comment_form")[0].reset();
            $("#comment_list tbody").prepend($('<tr><td>' + comment.message + ' at ' + updated_at + '</td></tr>'));
            $.toaster({
                priority: 'info',
                message: '댓글을 등록했습니다.'
            });
        });

        $(".delete-confirm").click(function() {
            var url = $(this).attr("href");
            var target = $(this).parent().parent();

            if ( confirm("삭제하시겠습니까?") ) {
                $.ajax({
                    url: url,
                    method: "POST",
                }).done(function() {
                    target.remove();
                    $.toaster({
                        priority: 'info',
                        message: '댓글을 삭제했습니다.'
                    });
                }).fail(function() {
                    $.toaster({
                        priority: 'danger',
                        message: '댓글 삭제 실패 ㅠ_ㅠ'
                    });
                });
            }
            return false;
        });
    });
})(jQuery);

