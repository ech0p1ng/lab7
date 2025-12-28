async function getAnalytics() {
    try {
        const response = await $.ajax({
            type: 'GET',
            url: '/api/analytics/',
            contentType: 'application/json',
        });
        $('main').empty();
        $('main').append(table(response.table.name, response.table.data))
        response.confussion_matrixes.forEach(c => {
            $('main').append(table(c.method, c.matrix))
        })
    }
    catch (xhr) {
        $('main .code-format').html('Ошибка загрузки данных');
        show_errors(xhr.responseJSON.detail);
    }
}

$(function () {
    getAnalytics();
});
