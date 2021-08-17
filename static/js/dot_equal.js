// 点々問題の処理
$('[id^=select-item-]').on('click', function(e) {
    var temp = $(this).attr('id');
    var number = parseInt(temp.match(/\d{1,2}/));
    // 選択しているリスト
    var ai_item_select = $('#select-item-' + String(number)).val();

    // 1行目処理
    if (number === 1) {
        // 品番コードが10桁の場合
        if (ai_item_select.match(/\d{10}/)) {
            e.preventDefault();
            $.ajax({
                data: {
                    select_change_number: number,
                    ai_item_select: ai_item_select
                },
                type: 'POST',
                url: '/db_item_check',
                dataType: 'json',
            })
            .done(function(data) {
                console.log(data);
                $('#item-code-' + data.number).val('');
                $('#item-code-' + data.number).val(data.item_code + '_' + data.item_name + '_' + data.item_standard);
                
            })
            .fail(function(data) {
                console.log('1行目Ajax処理エラー');
            });
        }
    // 2行目以降の処理
    } else {
        // 選択している1つ上の商品コード
        var item_on_line_one = $('#item-code-' + String(number - 1)).val().slice(0, 10);
        // 品番コードが10桁の場合
        if (ai_item_select.match(/\d{10}/)) {
            e.preventDefault();
            $.ajax({
                data: {
                    select_change_number: number,
                    ai_item_select: ai_item_select
                },
                type: 'POST',
                url: '/db_item_check',
                dataType: 'json',
            })
            .done(function(data) {
                console.log(data);
                $('#item-code-' + data.number).val('');
                $('#item-code-' + data.number).val(data.item_code + '_' + data.item_name + '_' + data.item_standard);
            })
            .fail(function(data) {
                console.log('2行目Ajax処理エラー');
            });
        // 品番コードが10桁以外で選択された行の商品コードが10桁の場合
        } else if (!ai_item_select.match(/\d{10}/) && item_on_line_one.match(/\d{10}/)) {
            e.preventDefault();
            $.ajax({
                data: {
                    select_change_number: number,
                    ai_item_select: ai_item_select,
                    item_on_line_one: item_on_line_one
                },
                type: 'POST',
                url: '/db_item_on_line_one',
                dataType: 'json',
            })
            .done(function(data) {
                console.log(data);
                $('#item-code-' + data.number).val('');
                $('#item-code-' + data.number).val(data.item_code);
                
            })
            .fail(function(data) {
                console.log('2行目以降点々問題Ajax処理エラー');
            });
        }
    
    }
});