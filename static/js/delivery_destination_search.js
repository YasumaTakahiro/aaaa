//納入先の検索ボックスから納入先を検索
$('#delivery-destination-search').keypress(function(e) {
    if (e.which == 13) {
        e.preventDefault();
        $('#delivery-destination-search').click();
    }
});


//納入先の検索処理を実施
$('#delivery-destination-search').on('click', function(e) {
    var customer_number = $('#customer-id').val();
    var delivery_des_keywords = $('#delivery-destination-search').val();

    if (!delivery_des_keywords.match(/\S/g)) {
        console.log('キーワードが入力されていないため、納入先検索のAjax処理を実行しません。');
    } else {
        e.preventDefault();
        $.ajax({
            data: {
                customer_number: customer_number,
                delivery_des_keywords: delivery_des_keywords
            },
            type: 'POST',
            url: '/db_delivery_des_search',
            dataType: 'json'
        })
        .done(function(data) {
            console.log('納入先検索Ajax OK');
            $(data.db_result_delivery_des_area).html(data.db_result_delivery_des_html);
        })
        .fail(function(data) {
            console.log('納入先検索Ajax NG')
        });
    }
});


//納入先を検索後 納入先コードおよび納入先正式名を変更
$(function() {
    $(document).on('click', '#delivery-destination-result', function() {
        var re_delivery_des = $('#delivery-destination-result').val().split('_');
        $('#delivery-destination-id').val(re_delivery_des[0].substr(4,8));
        $('#delivery-destination-name').val(re_delivery_des[1]);
    });
});