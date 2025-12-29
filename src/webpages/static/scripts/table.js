function table(table_name, data) {
    let $wrapper = $(`
        <div style="margin-bottom: 20px;">
            <h4>${table_name}</h4>
            <table border="1">
                <thead></thead>
                <tbody></tbody>
            </table>
        </div>
    `);

    const $table = $wrapper.find("table");

    /* ===============================
       CASE 1: metrics table (есть model)
       =============================== */
    if (data.model) {
        const metrics = Object.keys(data).filter(k => k !== "model");
        const rows = Object.keys(data.model);

        // header
        const $theadRow = $("<tr>");
        $theadRow.append("<th>Model</th>");
        metrics.forEach(m => $theadRow.append(`<th>${m}</th>`));
        $table.find("thead").append($theadRow);

        // body
        rows.forEach(i => {
            const $row = $("<tr>");
            $row.append(`<td>${data.model[i]}</td>`);

            metrics.forEach(metric => {
                const value = data[metric][i];
                $row.append(`<td>${Number(value).toFixed(4)}</td>`);
            });

            $table.find("tbody").append($row);
        });

        return $wrapper;
    }

    /* ==================================
       CASE 2: confusion matrix
       ================================== */
    const columns = Object.keys(data);
    const rows = Object.keys(data[columns[0]]);

    // header
    const $theadRow = $("<tr>");
    $theadRow.append("<th></th>");
    columns.forEach(col => $theadRow.append(`<th>${col}</th>`));
    $table.find("thead").append($theadRow);

    // body
    rows.forEach(rowName => {
        const $row = $("<tr>");
        $row.append(`<td>${rowName}</td>`);

        columns.forEach(col => {
            $row.append(`<td>${data[col][rowName]}</td>`);
        });

        $table.find("tbody").append($row);
    });

    return $wrapper;
}