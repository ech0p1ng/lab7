let TRAIN_DATA_OFFSET = 0;
let TRAIN_DATA_LIMIT = 100;

function item_with_header(item_id, header, item) {
    return $(`
        <div id="${item_id}">
            <h4>${header}</h4>
            <span class="code-format item">${item}</span>
        </div>
    `);
}

function textFormat(text) {
    return text.replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/\n/g, "<br><br>");
}

async function getItem(item_name, header, format_as = 'text', query_params_str = "") {
    try {
        $('main').append(item_with_header(
            item_name,
            header,
            'Загрузка...'
        ));
        const response = await $.ajax({
            type: 'GET',
            url: `/api/info/${item_name}` + query_params_str,
            contentType: 'application/json',
        });
        var value = '';
        if (format_as == 'text') {
            value = textFormat(response);
        }
        else if (format_as == 'table') {
            value = table('', response);
        }
        $('#' + item_name + ' .item').html(value);
        TRAIN_DATA_OFFSET += TRAIN_DATA_LIMIT;
    }
    catch (xhr) {
        show_errors(xhr.responseJSON);
    }
}


$(function () {
    getItem('subject_area', 'Предметная область');
    getItem('target_attribute', 'Целевой признак');
    getItem(
        'train_data',
        'Обучающая выборка',
        'table',
        `?limit=${TRAIN_DATA_LIMIT}&offset=${TRAIN_DATA_OFFSET}`
    );
});