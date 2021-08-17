// 得意先の検索ボックスから得意先を検索
$('#customer-search').keypress(function(e) {
    if (e.which == 13) {
        e.preventDefault();
        $('#customer-search').click();
    }
});


// 得意先の検索処理を実施
$('#customer-search').on('click', function(e) {
    var customer_keywords = $('#customer-search').val();
    
    if (!customer_keywords.match(/\S/g)) {
        console.log('キーワードが入力されていないため、得意先検索のAjax処理を実行しません。');
    } else {
        e.preventDefault();
        $.ajax({
            data: {
                customer_keywords: customer_keywords
            },
            type: 'POST',
            url: '/db_customer_search',
            dataType: 'json',
        })
        .done(function(data) {
            console.log('得意先検索処理Ajax OK');
            $(data.db_result_customer_area).html(data.db_result_customer_html);
        })
        .fail(function(data) {
            console.log('得意先検索のAjax NG');
        });
    }
});


//得意先を検索後 得意先コード及び得意先正式名を変更
$(function() {
    $(document).on('click', '#customer-result', function(){
        var re_customer = $('#customer-result').val().split('_');
        $('#customer-id').val(re_customer[0]);
        $('#customer-name').val(re_customer[1]);
    });
});