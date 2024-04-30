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

export const getLangDataByCode = (code) => {

    return langData.find(lang => {
        return lang.code === code
    })
}