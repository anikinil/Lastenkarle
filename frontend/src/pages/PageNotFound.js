import React from 'react';
import { useTranslation } from 'react-i18next';

const PageNotFound = () => {

    const { t } = useTranslation();

    return (
        <>
            <h1>{t('page_not_found')}</h1>
        </>
    );
};
  
export default PageNotFound;