//得意先を検索後 担当者コードを変更
$(function() {
    $(document).on('click', '#customer-result', function(e){
        // 実行したい処理を記述 
        var re_customer = $('#customer-result').val().split('_');
        // 得意先コードが4桁の場合
        if (re_customer[0].match(/\d{4}/)) {
            e.preventDefault();
            $.ajax({
                data: {
                    rep_number: re_customer[0]
                },
                type: 'POST',
                url: '/db_rep_search',
                dataType: 'json',
            })
            .done(function(data) {
                console.log('担当者検索Ajax OK');
                $('#rep-number').val('');
                $('#rep-number').val(data.rep_number);
            })
            .fail(function(data) {
                console.log('担当者検索Ajax NG');
            });
        }
    });
});