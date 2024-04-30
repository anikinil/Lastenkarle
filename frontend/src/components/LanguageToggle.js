
import i18n from "i18next";
import { getLangDataByCode, langData } from "../utils/languageToggle";
import React, { useState } from "react";

const LanguageToggle = () => {

    const langs = langData;
    const [currLang, setCurrLang] = useState(getLangDataByCode(i18n.language))

    const switchLangauge = () => {
        const nextIdx = langs.indexOf(currLang) + 1;
        const nextLang = nextIdx < langs.length ? langs[nextIdx] : langs[0]
        setCurrLang(nextLang)
        i18n.changeLanguage(nextLang.code)
    }

    return (
        <button className='language-toggle' onClick={switchLangauge}>{currLang.label}</button>
    );
}

export default LanguageToggle;