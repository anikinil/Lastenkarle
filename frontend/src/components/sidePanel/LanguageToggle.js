
import i18n from "i18next";
import { getLangDataByCode, langData, defaultLang } from "../../utils/languageToggle";
import React, { useEffect, useState } from "react";
import "./SidePanel.css"

const LanguageToggle = () => {

    const langs = langData;
    const [currLang, setCurrLang] = useState(defaultLang)
    
    useEffect(() => {
        setCurrLang(getLangDataByCode(i18n.language));
    }, []);


    const switchLangauge = () => {
        const nextIdx = langs.indexOf(currLang) + 1;
        const nextLang = nextIdx < langs.length ? langs[nextIdx] : langs[0]
        setCurrLang(nextLang)
        i18n.changeLanguage(nextLang.code)
    }

    return (
        <button className='toggle language' onClick={switchLangauge}>{currLang.label}</button>
    );
}

export default LanguageToggle;