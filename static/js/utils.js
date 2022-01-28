// Utils for various stuff.

const getErrorString = (errors) => {
    let errorStr = '';
    $.each(errors, (index, entry) => {
        const {label: name, errors: errorList} = entry;
        errorStr += `<p><b>${name}</b>:</p>${errorList.map(error => `<p>${error}</p>`).join('')}`;
    });
    return errorStr;
}

