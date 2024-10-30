// Array containing language data with code and label
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

// Default language object to use if the provided language code is not recognized
export const defaultLang = { code: 'en', label: 'EN' } // in case lang code not recognized, use English as default

// Function to get language data by code
export const getLangDataByCode = (code) => {

    // Find the language object that matches the provided code
    const lang = langData.find(lang => {
        return lang.code === code
    });

    // Return the found language object or the default language if not found
    return lang !== undefined ? lang : defaultLang;
}