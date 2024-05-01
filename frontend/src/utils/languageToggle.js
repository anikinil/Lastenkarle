export const langData = [
    {
        code: 'de',
        label: 'DE',
    },
    {
        code: 'en',
        label: 'EN',
    },
]

const defaultLang = { code: 'en', label: 'EN' } // in case lang code not recognized, use english as default

export const getLangDataByCode = (code) => {

    const lang = langData.find(lang => {
        return lang.code === code
    });

    return lang !== 'undefined' ? lang : defaultLang;
}