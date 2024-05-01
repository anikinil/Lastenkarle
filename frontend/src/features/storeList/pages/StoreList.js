import React from "react";
import { useTranslation } from "react-i18next";



const StoreList = () => {

    const { t } = useTranslation();

    return (
        <h1>{t('store_list')}</h1>
    );
};
  
export default StoreList;